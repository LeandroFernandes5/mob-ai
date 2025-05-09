import importlib
import logging
import os
import requests
import httpx
import src.log_config
from .config_manager import ConfigManager
import time
import json
from typing import Dict, Any

class ConfigurationError(Exception):
    """Raised when there's an error in the configuration."""
    pass

def validate_model_config(model_config: Dict[str, Any], model_provider: str, interface_id: str) -> None:
    """
    Validate the model configuration.
    
    Args:
        model_config: The model configuration dictionary
        model_provider: The name of the model provider
        interface_id: The interface ID
    
    Raises:
        ConfigurationError: If the configuration is invalid
    """
    if not model_config:
        raise ConfigurationError(f"No configuration found for model provider '{model_provider}' in interface '{interface_id}'")
    
    required_fields = {
        'openai': ['model', 'api_key', 'system_prompt'],
        'local_model': ['model_type', 'base_url', 'model', 'system_prompt']
    }
    
    missing_fields = [field for field in required_fields.get(model_provider, []) 
                     if field not in model_config]
    
    if missing_fields:
        raise ConfigurationError(
            f"Missing required fields for {model_provider} in interface '{interface_id}': {', '.join(missing_fields)}"
        )
    
    if model_provider == 'local_model' and model_config.get('model_type') != 'ollama':
        raise ConfigurationError(
            f"Unsupported local model type '{model_config.get('model_type')}' in interface '{interface_id}'. "
            "Currently only 'ollama' is supported."
        )

def load_model_client(model_provider: str, api_key: str):
    """
    Dynamically load and initialize a client for the specified model provider.
    
    Args:
        model_provider (str): Name of the model provider (e.g., 'openai', 'anthropic')
        api_key (str): API key for the model provider
    
    Returns:
        An initialized client for the specified model provider
    """
    try:
        # Dynamically import the module based on the model provider
        module = importlib.import_module(model_provider)
        client_class = getattr(module, 'OpenAI')  # Assumes a standard naming convention
        
        # Check if secure connection should be disabled
        disable_verify = os.environ.get('MOBAI_DISABLE_SSL_VERIFY', 'false').lower() == 'true'
        if disable_verify:
            http_client = httpx.Client(verify=False)
            return client_class(api_key=api_key, http_client=http_client)
        else:
            return client_class(api_key=api_key)
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Could not load client for {model_provider}: {e}")

def fetch_external_data(context: dict) -> str:
    """
    Fetches data from an external AI model API based on user context or input.
    
    Args:
        context: A dictionary containing configuration and query information.
                Expected to have:
                - 'model_provider': Name of the AI model provider
                - 'question': Query to send to the AI
    
    Returns:
        String containing the response from the AI model.
    """
    # Generate correlation ID
    correlation_id = f"{int(time.time())}_{context.get('interface_id', 'unknown')}"
    
    # Load configuration
    config_manager = ConfigManager()
    
    # Require interface_id, model_provider, and question in context
    interface_id = context.get('interface_id')
    if not interface_id:
        return "Error: 'interface_id' must be provided in context."
    model_provider = context.get('model_provider')
    if not model_provider:
        return "Error: 'model_provider' must be provided in context."
    question = context.get('question')
    if not question:
        return "Error: 'question' must be provided in context."
    
    # Get model configuration from the new config structure
    try:
        interface_config = config_manager.get_configuration(interface_id)
    except KeyError:
        return f"Error: No configuration found for interface: {interface_id}"
    
    model_providers = interface_config.get('model_providers', {})
    model_config = model_providers.get(model_provider)

    try:
        # Validate model configuration
        validate_model_config(model_config, model_provider, interface_id)
    except ConfigurationError as e:
        return f"Configuration Error: {str(e)}"
    
    # Extract system prompt
    system_prompt = model_config.get('system_prompt')
    
    # Check if this is a local model
    if model_provider == 'local_model':
        try:
            return call_local_model(model_config, system_prompt, question)
        except requests.exceptions.ConnectionError:
            return f"Error: Could not connect to local model service at {model_config.get('base_url')}. Please ensure the service is running."
        except requests.exceptions.Timeout:
            return f"Error: Request to local model service timed out. The service might be overloaded."
        except Exception as e:
            return f"Error fetching data from local model: {str(e)}"
    else:
        # Extract API key from environment variable
        api_key_env = model_config.get('api_key')
        api_key = os.environ.get(api_key_env)
        if not api_key:
            return f"Error: Environment variable '{api_key_env}' for {model_provider} API key is not set."
        
        try:
            # Load and initialize the client dynamically
            client = load_model_client(model_provider, api_key)

            # Log request information
            log_data = {
                "correlation_id": correlation_id,
                "event": "api_request",
                "model_provider": model_provider,
                "interface_id": interface_id,
                "model": model_config.get('model'),
                "question": question
            }
            logging.info(json.dumps(log_data))

            # Call the API
            response = client.chat.completions.create(
                model=model_config.get('model'),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ]
            )

            # Extract and return the response text
            if response.choices and len(response.choices) > 0:
                response_content = response.choices[0].message.content
                # Log the response
                log_data = {
                    "correlation_id": correlation_id,
                    "event": "api_response",
                    "model_provider": model_provider,
                    "interface_id": interface_id,
                    "model": model_config.get('model'),
                    "response": response_content
                }
                logging.info(json.dumps(log_data))
                return response_content
            else:
                return f"Error: No response content received from {model_provider}."

        except ImportError:
            return f"Error: Could not import {model_provider} client. Please ensure the package is installed."
        except ValueError as e:
            return f"Error initializing {model_provider} client: {str(e)}"
        except Exception as e:
            return f"Error fetching data from {model_provider}: {str(e)}"

def call_local_model(model_config: dict, system_prompt: str, question: str) -> str:
    """
    Calls a local model service (like Ollama) with the given parameters.
    
    Args:
        model_config: Configuration for the local model from config.yaml
        system_prompt: System prompt to use
        question: User's question
        
    Returns:
        String containing the response from the local model
    """
    model_type = model_config.get('model_type')
    if model_type != 'ollama':  # Currently only supporting Ollama
        return f"Error: Unsupported local model type: {model_type}"
    
    base_url = model_config.get('base_url', 'http://localhost:11434')
    model_name = model_config.get('model', 'llama3.2')
    
    # Generate a correlation ID
    correlation_id = f"{int(time.time())}_local_{model_name}"
    
    # Log the request using structured format
    log_data = {
        "correlation_id": correlation_id,
        "event": "local_model_request",
        "model_type": model_type,
        "base_url": base_url,
        "model": model_name,
        "question": question
    }
    logging.info(json.dumps(log_data))
    
    # Ollama API endpoint for chat completions
    api_url = f"{base_url}/api/chat"
    
    # Prepare the payload
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        "stream": False  # We want the complete response, not streaming
    }
    
    # Make the request
    response = requests.post(api_url, json=payload)
    
    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        
        # The expected format from Ollama is {"message": {"content": "..."}}
        if "message" in response_data and "content" in response_data["message"]:
            response_content = response_data["message"]["content"]
            
            # Log the response using structured format
            log_data = {
                "correlation_id": correlation_id,
                "event": "local_model_response",
                "model_type": model_type,
                "model": model_name,
                "response": response_content
            }
            logging.info(json.dumps(log_data))
            
            return response_content
        else:
            return f"Invalid response format from local model: {response_data}"
    else:
        return f"Error calling local model (status {response.status_code}): {response.text}"

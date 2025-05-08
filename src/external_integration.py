import importlib
import logging
import os
import requests
import httpx
import src.log_config
from .config_manager import ConfigManager

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

    if not model_config:
        return f"Error: No configuration found for model provider: {model_provider} in interface: {interface_id}"
    
    # Extract system prompt, must be present in config.yaml
    system_prompt = model_config.get('system_prompt')
    if not system_prompt:
        return f"Error: No system prompt found for {model_provider} in config.yaml"
    
    # Check if this is a local model
    if model_provider == 'local_model':
        try:
            return call_local_model(model_config, system_prompt, question)
        except Exception as e:
            return f"Error fetching data from local model: {str(e)}"
    else:
        # Extract API key from environment variable specified in config
        api_key_env = model_config.get('api_key')
        if not api_key_env:
            return f"Error: No 'api_key_env' specified for {model_provider} in config.yaml"
        
        api_key = os.environ.get(api_key_env)
        if not api_key:
            return f"Error: Environment variable '{api_key_env}' for {model_provider} API key is not set."
        
        try:
            # Load and initialize the client dynamically
            client = load_model_client(model_provider, api_key)

            # Log all relevant information before sending the API request
            logging.info(
                "Preparing to send API request to %s | interface_id=%s | model=%s | system_prompt_preview=%s | question=%s | apikey=%s",
                model_provider,
                interface_id,
                model_config.get('model'),
                (system_prompt[:60] + '...') if system_prompt and len(system_prompt) > 60 else system_prompt,
                question,
                api_key
            )

            # Call the API (using OpenAI-like interface as an example)
            response = client.chat.completions.create(
                model=model_config.get('model', 'gpt-3.5-turbo'),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ]
            )

            # Extract and return the response text
            if response.choices and len(response.choices) > 0:
                response_content = response.choices[0].message.content
                # Log the response
                logging.info(
                    "Received response from OpenAI | interface_id=%s | model=%s | response=%s",
                    interface_id,
                    model_config.get('model'),
                    response_content
                )
                return response_content
            else:
                return f"No response received from {model_provider}."

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
    
    # Log the request
    logging.info(
        "Preparing to send request to local model | type=%s | url=%s | model=%s | system_prompt_preview=%s | message=%s",
        model_type,
        base_url,
        model_name,
        (system_prompt[:60] + '...') if system_prompt and len(system_prompt) > 60 else system_prompt,
        question
    )
    
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
            return f"{response_data['message']['content']}"
        else:
            return f"Invalid response format from local model: {response_data}"
    else:
        return f"Error calling local model (status {response.status_code}): {response.text}"

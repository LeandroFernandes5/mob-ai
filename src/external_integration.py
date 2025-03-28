import os
import importlib
from typing import Dict, Any
from config_manager import ConfigManager

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
    
    # Extract model provider from context, default to 'openai'
    model_provider = context.get('model_provider', 'openai')
    
    # Get model configuration
    model_config = config_manager.get_model_config(model_provider)
    
    # Extract API key
    api_key = model_config.get('api_key')
    if not api_key:
        return f"Error: No API key found for {model_provider}"
    
    # Extract system prompt, default if not provided
    system_prompt = model_config.get('system_prompt', 
        "You are a helpful assistant providing concise, accurate information.")
    
    # Extract the question from context, or use a default
    question = context.get('question', 'Please provide some general information.')
    
    try:
        # Load and initialize the client dynamically
        client = load_model_client(model_provider, api_key)
        
        # Call the API (using OpenAI-like interface as an example)
        response = client.chat.completions.create(
            model=model_config.get('model', 'gpt-3.5-turbo'),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=model_config.get('max_tokens', 150)
        )
        
        # Extract and return the response text
        if response.choices and len(response.choices) > 0:
            return f"{model_provider.capitalize()} response: {response.choices[0].message.content}"
        else:
            return f"No response received from {model_provider}."
            
    except Exception as e:
        # Handle errors gracefully
        return f"Error fetching data from {model_provider}: {str(e)}"

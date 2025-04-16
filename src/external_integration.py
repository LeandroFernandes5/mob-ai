import importlib
import logging
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
    
    # Extract API key from environment variable specified in config
    api_key_env = model_config.get('api_key')
    if not api_key_env:
        return f"Error: No 'api_key_env' specified for {model_provider} in config.yaml"
    import os
    api_key = os.environ.get(api_key_env)
    if not api_key:
        return f"Error: Environment variable '{api_key_env}' for {model_provider} API key is not set."
    
    # Extract system prompt, must be present in config.yaml
    system_prompt = model_config.get('system_prompt')
    if not system_prompt:
        return f"Error: No system prompt found for {model_provider} in config.yaml"
    
    try:
        # Load and initialize the client dynamically
        client = load_model_client(model_provider, api_key)

        # Log all relevant information before sending the API request
        logging.info(
            "Preparing to send API request to %s | interface_id=%s | model=%s | max_tokens=%s | system_prompt_preview=%s | question=%s | apikey=%s",
            model_provider,
            interface_id,
            model_config.get('model', 'gpt-3.5-turbo'),
            model_config.get('max_tokens', 150),
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
            ],
            max_tokens=model_config.get('max_tokens', 150)
        )

        # Extract and return the response text
        if response.choices and len(response.choices) > 0:
            return f"{model_provider.capitalize()} response: {response.choices[0].message.content}"
        else:
            return f"No response received from {model_provider}."

    except Exception as e:
        return f"Error fetching data from {model_provider}: {str(e)}"

import os
import yaml
from typing import Dict, Any
from dotenv import load_dotenv

class ConfigManager:
    def __init__(self, config_path: str = 'config.yaml'):
        """
        Initialize ConfigManager with optional config file path.
        
        Args:
            config_path (str): Path to the YAML configuration file. 
                               Defaults to 'config.yaml' in the project root.
        """
        load_dotenv()
        self.config = self._load_config(config_path)
        
        # Preserve the existing interface configurations
        self.INTERFACE_CONFIGS = {
            "cs_support": {
                "system_prompt": "You are a helpful customer support assistant. Always answer politely and comprehensively.",
                "model_id": "chatgpt-4",
                "parameters": {"temperature": 0.7, "max_tokens": 512}
            },
            "mkt_generator": {
                "system_prompt": "You are a creative marketing copywriter. Provide catchy, concise marketing copy.",
                "model_id": "gemini-1.0",
                "parameters": {"temperature": 0.9, "max_tokens": 1024}
            },
            "dev_copilot": {
                "system_prompt": "You are a coding assistant. Write clean, well-documented code.",
                "model_id": "local-llm",
                "parameters": {"temperature": 0.2, "max_tokens": 2048}
            }
        }

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from a YAML file.
        
        Args:
            config_path (str): Path to the configuration file
        
        Returns:
            Dict[str, Any]: Loaded configuration dictionary
        """
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            print(f"Warning: Configuration file {config_path} not found. Using default settings.")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing configuration file: {e}")
            return {}

    def get_model_config(self, model_provider: str) -> Dict[str, Any]:
        """
        Retrieve configuration for a specific model provider.
        
        Args:
            model_provider (str): Name of the model provider (e.g., 'openai', 'anthropic')
        
        Returns:
            Dict[str, Any]: Configuration dictionary for the model provider
        """
        return self.config.get('model_providers', {}).get(model_provider, {})

    def get_configuration(self, interface_id: str) -> Dict[str, Any]:
        """
        Retrieves the system prompt and model configuration for the given interface ID.
        Falls back to predefined interface configurations if not found in YAML.
        
        Args:
            interface_id (str): Identifier for the interface configuration
        
        Returns:
            Dict[str, Any]: Configuration for the specified interface
        """
        # First, try to get configuration from YAML
        interface_config = self.config.get('interfaces', {}).get(interface_id)
        
        # If not found in YAML, fall back to predefined configurations
        if not interface_config:
            interface_config = self.INTERFACE_CONFIGS.get(interface_id)
        
        if not interface_config:
            raise KeyError(f"No configuration found for interface: {interface_id}")
        
        return interface_config

    def get_api_key(self, model_provider: str) -> str:
        """
        Get API key for a specific model provider.
        Checks both the configuration file and environment variables.
        
        Args:
            model_provider (str): Name of the model provider
        
        Returns:
            str: API key for the model provider
        """
        # First, check the configuration file
        provider_config = self.get_model_config(model_provider)
        api_key = provider_config.get('api_key')
        
        # If not found in config, check environment variables
        if not api_key:
            api_key = os.getenv(f'{model_provider.upper()}_API_KEY')
        
        return api_key

def get_configuration(interface_id: str) -> Dict[str, Any]:
    """
    Convenience function to retrieve configuration for a given interface.
    
    Args:
        interface_id (str): Identifier for the interface configuration
    
    Returns:
        Dict[str, Any]: Configuration for the specified interface
    """
    manager = ConfigManager()
    return manager.get_configuration(interface_id)

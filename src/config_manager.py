import yaml
import os
from typing import Dict, Any
from pathlib import Path

class ConfigManager:
    """
    Manages configuration for different interfaces in the AI platform.
    
    This class implements a directory-based configuration system where each interface
    has its own directory containing a config.yaml file. The configuration is cached
    in memory for improved performance.
    
    Directory Structure:
        interfaces/
        ├── interface1/
        │   └── config.yaml
        ├── interface2/
        │   └── config.yaml
        └── ...
    
    Example config.yaml format:
        model_providers:
          openai:
            model: gpt-3.5-turbo
            api_key: OPENAI_API_KEY
            system_prompt: |
              Your system prompt here
    """
    
    def __init__(self, interfaces_dir: str = 'interfaces'):
        """
        Initialize the ConfigManager.
        
        Args:
            interfaces_dir (str): Path to the directory containing interface configurations.
                                Defaults to 'interfaces'.
        """
        self.interfaces_dir = interfaces_dir
        self.config_cache = {}

    def get_configuration(self, interface_id: str) -> Dict[str, Any]:
        """
        Retrieve the configuration for a specific interface.
        
        This method first checks the cache for the configuration. If not found,
        it loads the configuration from the interface's config.yaml file and caches it.
        
        Args:
            interface_id (str): The ID of the interface to get configuration for.
                              This should match the directory name in interfaces/.
        
        Returns:
            Dict[str, Any]: The configuration dictionary for the specified interface.
            
        Raises:
            KeyError: If no configuration is found for the specified interface,
                     or if there's an error loading the configuration file.
        """
        # Check cache first
        if interface_id in self.config_cache:
            return self.config_cache[interface_id]

        # Build the path to the interface's config file
        config_path = os.path.join(self.interfaces_dir, interface_id, 'config.yaml')
        
        if not os.path.exists(config_path):
            raise KeyError(f"No configuration found for interface: {interface_id}")
        
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file) or {}
                # Cache the configuration
                self.config_cache[interface_id] = config
                return config
        except Exception as e:
            raise KeyError(f"Error loading configuration for interface {interface_id}: {str(e)}")

def get_configuration(interface_id: str) -> Dict[str, Any]:
    """
    Convenience function to get configuration for an interface.
    
    This is a shortcut that creates a ConfigManager instance and calls
    get_configuration() on it.
    
    Args:
        interface_id (str): The ID of the interface to get configuration for.
        
    Returns:
        Dict[str, Any]: The configuration dictionary for the specified interface.
    """
    manager = ConfigManager()
    return manager.get_configuration(interface_id)

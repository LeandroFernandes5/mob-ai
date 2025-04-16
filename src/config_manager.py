import yaml
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_path: str = 'config.yaml'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file) or {}

    def get_configuration(self, interface_id: str) -> Dict[str, Any]:
        interface_config = self.config.get('interfaces', {}).get(interface_id)
        if not interface_config:
            raise KeyError(f"No configuration found for interface: {interface_id}")
        return interface_config

def get_configuration(interface_id: str) -> Dict[str, Any]:
    manager = ConfigManager()
    return manager.get_configuration(interface_id)

from typing import Dict, Any

# A simple in-memory “registry” for demonstration.
# In a real-world scenario, store these in a secure config management system.
INTERFACE_CONFIGS = {
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

def get_configuration(interface_id: str) -> Dict[str, Any]:
    """
    Retrieves the system prompt and model configuration for the given interface ID.
    Raises KeyError if interface_id is not found.
    """
    return INTERFACE_CONFIGS[interface_id]

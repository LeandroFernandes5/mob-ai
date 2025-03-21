from typing import Dict

def build_prompt(system_prompt: str, user_input: str, user_context: Dict) -> str:
    """
    Merges the system prompt, user input, and any relevant user context.
    Handles external data from third-party APIs if available.
    """
    # Build context string
    context_parts = []
    
    # Extract external data if available
    external_data = user_context.get('external_data')
    if external_data:
        context_parts.append(f"External API Data: {external_data}")
    
    # Add other context information
    other_context = {k: v for k, v in user_context.items() if k not in ['external_data', 'question']}
    if other_context:
        context_parts.append(f"User Context: {other_context}")
    
    # Combine all context parts
    context_str = ""
    if context_parts:
        context_str = "\n[" + "\n".join(context_parts) + "]"
    
    final_prompt = f"{system_prompt}\n{context_str}\nUser: {user_input}\nAI:"
    return final_prompt

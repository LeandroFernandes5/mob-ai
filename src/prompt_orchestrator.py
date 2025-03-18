from typing import Dict

def build_prompt(system_prompt: str, user_input: str, user_context: Dict) -> str:
    """
    Merges the system prompt, user input, and any relevant user context.
    For demonstration, we simply concatenate them.
    In a real scenario, you might need a more structured approach (e.g., chat format).
    """
    context_str = ""
    if user_context:
        # Example: flatten or otherwise format the user context
        context_str = f"\n[Context: {user_context}]"
    
    final_prompt = f"{system_prompt}\n{context_str}\nUser: {user_input}\nAI:"
    return final_prompt

import os
import openai
from typing import Optional

# In a production environment, this should be securely stored
# and accessed via environment variables or a secure vault
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-api-key-here")

def fetch_external_data(context: dict) -> str:
    """
    Fetches data from OpenAI API based on user context or input.
    
    Args:
        context: A dictionary containing user context information.
                Expected to have a 'question' key with the query to send to OpenAI.
    
    Returns:
        String containing the response from OpenAI.
    """
    # Initialize the OpenAI client
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    # Extract the question from context, or use a default
    question = context.get('question', 'Please provide some general information.')
    
    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Can be configured based on needs
            messages=[
                {"role": "system", "content": "You are a helpful assistant providing concise, accurate information."},
                {"role": "user", "content": question}
            ],
            max_tokens=150  # Limit response length
        )
        
        # Extract and return the response text
        if response.choices and len(response.choices) > 0:
            return f"OpenAI response: {response.choices[0].message.content}"
        else:
            return "No response received from OpenAI."
            
    except Exception as e:
        # Handle errors gracefully
        return f"Error fetching data from OpenAI: {str(e)}"

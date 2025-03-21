import requests
import json

# URL of your FastAPI server
BASE_URL = "http://localhost:8000"  # Adjust if your server runs on a different port

def test_openai_integration():
    """
    Test the OpenAI integration by sending a request with a question
    to be forwarded to the OpenAI API.
    """
    # Endpoint for queries
    endpoint = f"{BASE_URL}/v1/query"
    
    # Prepare the request payload
    payload = {
        "interface_id": "cs_support",  # Using the customer support interface
        "user_input": "Tell me about cloud computing services.",
        "user_context": {
            "user_id": "test_user_123",
            "session_id": "test_session_456",
            "question": "What are the main types of cloud computing services and their differences?"
        }
    }
    
    # Set headers for JSON content
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Send the POST request
        response = requests.post(endpoint, json=payload, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            print("Success! Response:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

if __name__ == "__main__":
    test_openai_integration()

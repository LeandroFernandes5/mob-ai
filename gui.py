import streamlit as st
import requests
import os
from typing import List, Dict
import yaml

# Constants
API_URL = "http://localhost:8000"  # Update this if your API is running on a different URL
INTERFACES_DIR = "interfaces"

def get_available_interfaces() -> List[str]:
    """
    Get a list of available interfaces from the interfaces directory.
    
    Returns:
        List[str]: List of interface names (directory names)
    """
    try:
        return [d for d in os.listdir(INTERFACES_DIR) 
                if os.path.isdir(os.path.join(INTERFACES_DIR, d))]
    except FileNotFoundError:
        st.error(f"Interfaces directory '{INTERFACES_DIR}' not found!")
        return []

def get_interface_config(interface_id: str) -> Dict:
    """
    Get the configuration for a specific interface.
    
    Args:
        interface_id (str): The ID of the interface to get configuration for.
        
    Returns:
        Dict: The configuration dictionary for the specified interface.
    """
    config_path = os.path.join(INTERFACES_DIR, interface_id, "config.yaml")
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        st.error(f"Error loading configuration for interface {interface_id}: {str(e)}")
        return {}

def send_request(interface_id: str, question: str) -> str:
    """
    Send a request to the backend API.
    
    Args:
        interface_id (str): The ID of the interface to use.
        question (str): The user's question/input.
        
    Returns:
        str: The response from the API.
    """
    try:
        response = requests.post(
            f"{API_URL}/v1/query",
            json={
                "interface_id": interface_id,
                "model_provider": "openai",  # Default to OpenAI, could be made configurable
                "message": question
            }
        )
        response.raise_for_status()
        return response.json().get("response", "No response received")
    except requests.exceptions.RequestException as e:
        st.error(f"Error sending request to API: {str(e)}")
        return ""

# Set page config
st.set_page_config(
    page_title="AI Platform Interface",
    page_icon="🤖",
    layout="wide"
)

# Title
#st.title("AI Platform Interface")

# Sidebar
st.sidebar.title("Use Cases")
available_interfaces = get_available_interfaces()

if not available_interfaces:
    st.sidebar.error("No interfaces found! Please check your interfaces directory.")
else:
    # Interface selection using radio buttons
    selected_interface = st.sidebar.radio(
        "Select a Use Case",
        available_interfaces,
        label_visibility="collapsed"  # Hide the "Select a Use Case" label since we have the title
    )

# Main content area
if selected_interface:
    # Display interface description in main content
    interface_config = get_interface_config(selected_interface)
    if interface_config and "description" in interface_config:
        st.markdown(" **Description:** " + interface_config["description"])
        #st.markdown(interface_config["description"])
    
    # Text input
    user_input = st.text_area(
        "Enter your question or input:",
        height=200,
        placeholder="Type your message here..."
    )
    
    # Submit button
    if st.button("Submit"):
        if user_input.strip():
            with st.spinner("Processing your request..."):
                response = send_request(selected_interface, user_input)
                st.markdown("### Response:")
                st.markdown(response)
        else:
            st.warning("Please enter some text before submitting.") 
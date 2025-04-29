import requests
import unittest

BASE_URL = "http://localhost:8000"

class TestModelIntegration(unittest.TestCase):

    def test_at_risk_interface(self):
        endpoint = f"{BASE_URL}/v1/query"
        payload = {
            "interface_id": "at_risk_interface",
            "message": "I've had so many dropped calls and slow internet lately. If this doesn't improve soon, I'll be switching providers."
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(endpoint, json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
    
    def test_local_model_integration(self):
        endpoint = f"{BASE_URL}/v1/custom_query"
        payload = {
            "interface_id": "at_risk_interface",
            "model_provider": "local_model",
            "message": "I'm switching to T-Mobile next week due to these hidden fees"
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(endpoint, json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        # Check if response contains the expected local model indicator
        self.assertIn("Local model response", response.json().get("response", ""))

if __name__ == "__main__":
    unittest.main() 
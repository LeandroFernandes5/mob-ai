import requests
import unittest

BASE_URL = "http://localhost:8000"

class TestOpenAIIntegration(unittest.TestCase):

    def test_at_risk_interface(self):
        endpoint = f"{BASE_URL}/v1/query"
        payload = {
            "interface_id": "at_risk_interface",
            "message": "I've had so many dropped calls and slow internet lately. If this doesn't improve soon, I'll be switching providers."
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(endpoint, json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()

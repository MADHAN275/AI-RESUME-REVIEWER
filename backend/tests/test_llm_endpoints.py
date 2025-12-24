import unittest
import sys
import os
import json
from unittest.mock import MagicMock, patch

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.app.main import create_app

class TestLLMEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_analyze_with_llm(self):
        # We need to mock the LLMAgent inside the app context, but since it's instantiated in create_app,
        # we might need to rely on the fallback mechanism or mock the instance.
        # Since we just tested the unit logic of LLMAgent, here we test that the endpoint
        # calls it and returns the 'llm_insights' key.
        
        payload = {
            "resume_data": {"sections": {"skills": "Python"}},
            "target_role": "Backend Developer"
        }
        
        response = self.client.post('/api/analyze', json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("llm_insights", data)
        # Check if fallback (or real if configured) returns expected structure
        self.assertIn("ats_score", data["llm_insights"])

    def test_chat_endpoint(self):
        payload = {
            "message": "Hello, mentor!"
        }
        response = self.client.post('/api/chat', json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("reply", data)
        # Without key, it says "offline mode"
        self.assertIn("offline mode", data["reply"])

if __name__ == '__main__':
    unittest.main()

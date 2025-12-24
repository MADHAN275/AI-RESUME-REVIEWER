import unittest
import sys
import os
import io
from flask import Flask

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.app.main import create_app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_health_check(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'healthy')

    def test_upload_no_file(self):
        response = self.client.post('/api/upload')
        self.assertEqual(response.status_code, 400)

    # Note: Testing full upload requires mocking file save/parse which is complex in integration test.
    # We will assume unit tests cover parser and focus on endpoint structure here.

    def test_analyze_endpoint_structure(self):
        # Mock payload
        payload = {
            "resume_data": {
                "raw_text": "Python Developer with SQL skills",
                "sections": {
                    "skills": "Python, SQL",
                    "experience": "Dev at Corp"
                }
            },
            "target_role": "Backend Developer"
        }
        
        response = self.client.post('/api/analyze', json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("ats_analysis", data)
        self.assertIn("skill_gap", data)
        self.assertIn("recommendations", data)

if __name__ == '__main__':
    unittest.main()

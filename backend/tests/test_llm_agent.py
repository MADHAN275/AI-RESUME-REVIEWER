import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import json

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.app.services.llm_agent import LLMAgent

class TestLLMAgent(unittest.TestCase):
    def setUp(self):
        # By default, no API key, so it should be in fallback mode
        self.agent = LLMAgent()

    def test_mock_analysis_fallback(self):
        # Ensure it returns the mock structure when no LLM is present
        result = self.agent.analyze_resume({}, "Software Engineer", [])
        self.assertEqual(result["ats_score"]["score"], 75)
        self.assertIn("missing_skills", result)

    def test_chat_offline_message(self):
        response = self.agent.chat_with_mentor("Hello")
        self.assertIn("offline mode", response)

    @patch("backend.app.services.llm_agent.ChatOpenAI")
    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake-key"})
    def test_llm_analysis_parsing(self, mock_chat_openai):
        # Setup mock LLM
        mock_llm_instance = MagicMock()
        mock_chat_openai.return_value = mock_llm_instance
        
        # Define expected JSON output from LLM
        expected_json = {
            "ats_score": {"score": 85, "explanation": "Good job"},
            "missing_skills": ["Rust"],
            "project_recommendations": [],
            "learning_roadmap": [],
            "resume_improvements": []
        }
        
        # Mock the invoke response
        mock_response = MagicMock()
        mock_response.content = json.dumps(expected_json)
        mock_llm_instance.invoke.return_value = mock_response

        # Re-init agent to pick up the patched environment and class
        agent_with_key = LLMAgent()
        
        result = agent_with_key.analyze_resume({}, "Dev", [])
        
        self.assertEqual(result["ats_score"]["score"], 85)
        self.assertEqual(result["missing_skills"][0], "Rust")

if __name__ == '__main__':
    unittest.main()

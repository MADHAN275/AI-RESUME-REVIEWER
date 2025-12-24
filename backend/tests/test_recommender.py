import unittest
import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.app.services.recommender import Recommender

class TestRecommender(unittest.TestCase):
    def setUp(self):
        self.recommender = Recommender()

    def test_recommendations_from_skills(self):
        missing_skills = ["Docker", "React"]
        result = self.recommender.generate_recommendations(missing_skills, "Full Stack Developer")
        
        self.assertTrue(len(result["recommended_projects"]) > 0)
        
        # Check if project titles match expected templates
        titles = [p["title"] for p in result["recommended_projects"]]
        # One of these should be there at least
        self.assertTrue(any("Dashboard" in t or "Microservices" in t for t in titles))

    def test_fallback_recommendations(self):
        # When no skills match templates
        result = self.recommender.generate_recommendations(["SomethingRandom"], "Developer")
        self.assertTrue(len(result["recommended_projects"]) > 0)
        self.assertIn("general_tips", result)

if __name__ == '__main__':
    unittest.main()

import unittest
import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.app.services.ats_score import ATSScorer

class TestATSScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = ATSScorer()
        self.sample_resume = {
            "raw_text": "Python Developer. Expert in Django, React, and PostgreSQL. Experienced in AWS.",
            "sections": {
                "skills": "Python, Django, React, PostgreSQL, AWS",
                "experience": "Software Engineer at Google. Developed scalable web applications.",
                "projects": "Personal E-commerce site built with React and Django.",
                "certifications": "AWS Certified Developer",
                "education": "BS in Computer Science"
            }
        }
        self.sample_jd = "Looking for a Software Engineer with Python, Django, and AWS experience. Experience with SQL is required."

    def test_calculate_score(self):
        result = self.scorer.calculate_score(self.sample_resume, self.sample_jd)
        
        self.assertIn("overall_score", result)
        self.assertGreater(result["overall_score"], 0)
        self.assertIn("breakdown", result)
        self.assertIn("suggestions", result)
        
        # Check specific parts
        self.assertIn("keywords", result["breakdown"])
        self.assertTrue(result["breakdown"]["keywords"]["score"] > 0)

    def test_missing_sections_penalty(self):
        incomplete_resume = {
            "raw_text": "Just some text",
            "sections": {
                "skills": "Python"
                # missing experience and education
            }
        }
        result = self.scorer.calculate_score(incomplete_resume, self.sample_jd)
        self.assertLess(result["breakdown"]["formatting"]["score"], 100)
        self.assertIn("experience", result["breakdown"]["formatting"]["missing_sections"])

if __name__ == '__main__':
    unittest.main()

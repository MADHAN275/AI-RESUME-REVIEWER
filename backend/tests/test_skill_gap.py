import unittest
import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.app.services.skill_gap import SkillGapAnalyzer

class TestSkillGapAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = SkillGapAnalyzer()

    def test_basic_matching(self):
        resume_skills = ["Python", "JavaScript", "React"]
        required_skills = ["Python", "React", "Docker"]
        
        result = self.analyzer.analyze(resume_skills, required_skills)
        
        self.assertIn("python", result["strong_matches"])
        self.assertIn("react", result["strong_matches"])
        self.assertIn("docker", result["missing_skills"])
        self.assertGreater(result["match_percentage"], 0)

    def test_semantic_matching(self):
        # "React.js" should match "React"
        resume_skills = ["React.js"]
        required_skills = ["React"]
        
        result = self.analyzer.analyze(resume_skills, required_skills)
        
        # Depending on threshold, it might be strong or weak
        # React.js and React are very similar
        all_matches = result["strong_matches"] + [m["skill"] for m in result["weak_matches"]]
        self.assertIn("react", all_matches)

if __name__ == '__main__':
    unittest.main()

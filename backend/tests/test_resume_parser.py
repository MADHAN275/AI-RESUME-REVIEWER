import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock pdfplumber before import
sys.modules['pdfplumber'] = MagicMock()

# Add backend/app/services to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.app.services.resume_parser import ResumeParser

class TestResumeParser(unittest.TestCase):
    def setUp(self):
        self.parser = ResumeParser()
        self.sample_text = """
        John Doe
        john.doe@example.com
        (123) 456-7890
        linkedin.com/in/johndoe

        EDUCATION
        B.S. Computer Science, University of Tech
        2018 - 2022

        EXPERIENCE
        Software Engineer, Tech Corp
        2022 - Present
        - Built amazing things.

        SKILLS
        Python, JavaScript, SQL
        """

    def test_extract_contact_info(self):
        info = self.parser.extract_contact_info(self.sample_text)
        self.assertEqual(info['email'], 'john.doe@example.com')
        self.assertEqual(info['phone'], '(123) 456-7890')
        self.assertIn('linkedin.com/in/johndoe', info['links'][0])

    def test_segment_sections(self):
        sections = self.parser.segment_sections(self.sample_text)
        
        # Check if sections were identified
        self.assertIn('education', sections)
        self.assertIn('experience', sections)
        self.assertIn('skills', sections)
        
        # Check content (heuristic trimming might leave newlines, so we strip)
        self.assertIn("B.S. Computer Science", sections['education'])
        self.assertIn("Software Engineer", sections['experience'])
        self.assertIn("Python, JavaScript", sections['skills'])

if __name__ == '__main__':
    unittest.main()

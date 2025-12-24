import re
import json
import pdfplumber
import logging
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ResumeParser:
    """
    A rule-based resume parser to extract structured data from PDF resumes.
    It uses pdfplumber for text extraction and Regex for section segmentation.
    """

    def __init__(self):
        # Regex patterns for different sections
        self.sections_patterns = {
            "education": [
                r"\bEDUCATION\b", r"\bACADEMIC BACKGROUND\b", r"\bQUALIFICATIONS\b",
                r"\bEducation\b", r"\bAcademic Background\b"
            ],
            "experience": [
                r"\bEXPERIENCE\b", r"\bWORK EXPERIENCE\b", r"\bPROFESSIONAL EXPERIENCE\b",
                r"\bEMPLOYMENT HISTORY\b", r"\bExperience\b", r"\bWork Experience\b"
            ],
            "skills": [
                r"\bSKILLS\b", r"\bTECHNICAL SKILLS\b", r"\bCORE COMPETENCIES\b",
                r"\bTECHNOLOGIES\b", r"\bSkills\b", r"\bTechnical Skills\b"
            ],
            "projects": [
                r"\bPROJECTS\b", r"\bACADEMIC PROJECTS\b", r"\bPERSONAL PROJECTS\b",
                r"\bProjects\b", r"\bKey Projects\b"
            ],
            "certifications": [
                r"\bCERTIFICATIONS\b", r"\bCERTIFICATES\b", r"\bCOURSES\b",
                r"\bCertifications\b", r"\bCertificates\b"
            ]
        }

        # Regex for contact info
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+?\d{1,3}[\-.\s]?)?(\(?\d{3}\)?[\-.\s]?)?\d{3}[\-.\s]?\d{4}'
        self.url_pattern = r'\b(?:https?://|www\.|[a-zA-Z0-9-]+\.[a-z]{2,})[^\s]*\b'

    def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extracts raw text from a PDF file using pdfplumber.
        """
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    # Extract text preserving layout to some extent
                    page_text = page.extract_text(x_tolerance=1, y_tolerance=1)
                    if page_text:
                        text += page_text + "\n"
            logger.info(f"Successfully extracted text from {file_path}")
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise
        return text

    def clean_text(self, text: str) -> str:
        """
        Cleans the extracted text: removes extra whitespace, special characters, etc.
        """
        # Remove non-ascii characters usually found in bullets
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        # Replace multiple newlines with a single newline (optional, depending on structure needed)
        # We keep newlines to distinguish lines, but collapse multiple empty lines
        text = re.sub(r'\n\s*\n', '\n', text)
        return text.strip()

    def extract_contact_info(self, text: str) -> Dict[str, Any]:
        """
        Extracts email, phone, and potential links from the resume text.
        """
        email = re.search(self.email_pattern, text)
        phone = re.search(self.phone_pattern, text)
        links = re.findall(self.url_pattern, text)

        email_str = email.group(0) if email else None
        
        # Filter out email from links if it was wrongly detected as a URL
        if email_str:
            links = [link for link in links if link != email_str]

        return {
            "email": email_str,
            "phone": phone.group(0) if phone else None,
            "links": links if links else []
        }

    def segment_sections(self, text: str) -> Dict[str, str]:
        """
        Splits the text into logical sections based on headers.
        """
        sections = {
            "education": "",
            "experience": "",
            "skills": "",
            "projects": "",
            "certifications": "",
            "others": ""
        }

        # Create a map of positions for each section header found
        header_indices = []
        
        for section_name, patterns in self.sections_patterns.items():
            for pattern in patterns:
                # We look for headers usually at the start of a line or uppercase
                # Using search to find the *first* occurrence roughly
                matches = list(re.finditer(pattern, text))
                for match in matches:
                    # simplistic check: heuristic to ensure it's a header (short line, usually)
                    # Get the line containing the match
                    start, end = match.span()
                    line_start = text.rfind('\n', 0, start) + 1
                    line_end = text.find('\n', end)
                    if line_end == -1: line_end = len(text)
                    
                    line = text[line_start:line_end].strip()
                    
                    # If the line is short (mostly just the header), accept it
                    if len(line) < 50: 
                        header_indices.append((start, section_name))
                        break # Found one header for this section, stop looking for synonyms

        header_indices.sort()
        
        # If no headers found, return raw text in 'others'
        if not header_indices:
            sections["others"] = text
            return sections

        # Slice text based on sorted indices
        for i, (start_idx, section_name) in enumerate(header_indices):
            end_idx = header_indices[i+1][0] if i + 1 < len(header_indices) else len(text)
            # Extracted content for this section
            content = text[start_idx:end_idx].strip()
            # Remove the header itself from the content (roughly)
            # Find the first newline to skip the header line
            first_newline = content.find('\n')
            if first_newline != -1:
                content = content[first_newline:].strip()
            
            sections[section_name] = content

        return sections

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Main entry point to parse a resume PDF into structured JSON.
        """
        raw_text = self.extract_text_from_pdf(file_path)
        clean_text_data = self.clean_text(raw_text)
        
        contact_info = self.extract_contact_info(clean_text_data)
        sections = self.segment_sections(clean_text_data)

        # Construct final JSON structure
        resume_data = {
            "metadata": {
                "file_path": file_path,
                "parsed_date": "2025-12-24" # In a real app, use datetime.now()
            },
            "contact_info": contact_info,
            "sections": sections,
            "raw_text": raw_text # useful for debugging or LLM pass later
        }

        return resume_data

# --- Sample Usage / Testing ---
if __name__ == "__main__":
    import sys
    import os

    # Create a dummy PDF if none exists for testing
    # Note: pdfplumber needs a real PDF. We will just check if file provided.
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            parser = ResumeParser()
            try:
                data = parser.parse(file_path)
                print(json.dumps(data, indent=2))
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("File not found.")
    else:
        print("Usage: python resume_parser.py <path_to_resume.pdf>")

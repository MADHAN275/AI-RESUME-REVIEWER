import re
import logging
from typing import Dict, List, Any, Optional, Set
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ATSScorer:
    """
    Calculates ATS compatibility score based on keyword density, experience relevance,
    projects, certifications, and formatting.
    """

    def __init__(self):
        self.weights = {
            "keywords": 0.40,
            "experience": 0.30,
            "projects": 0.15,
            "certifications": 0.10,
            "formatting": 0.05
        }

    def _extract_keywords(self, text: str) -> Set[str]:
        """Simple keyword extraction using regex (removes stop words and short words)."""
        # This can be improved with NLTK/Spacy in later phases
        words = re.findall(r'\b\w{3,}\b', text.lower())
        return set(words)

    def calculate_score(self, resume_data: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """
        Main scoring function.
        :param resume_data: Structured JSON from ResumeParser
        :param job_description: Raw text of the target job description
        """
        sections = resume_data.get("sections", {})
        raw_text = resume_data.get("raw_text", "").lower()
        
        # 1. Keyword Score (40%)
        keyword_results = self._score_keywords(resume_data, job_description)
        
        # 2. Experience Score (30%)
        experience_results = self._score_experience(sections.get("experience", ""), job_description)
        
        # 3. Project Score (15%)
        project_results = self._score_projects(sections.get("projects", ""))
        
        # 4. Certifications Score (10%)
        cert_results = self._score_certifications(sections.get("certifications", ""))
        
        # 5. Formatting Score (5%)
        format_results = self._score_formatting(sections)

        # Calculate weighted total
        total_score = (
            (keyword_results["score"] * self.weights["keywords"]) +
            (experience_results["score"] * self.weights["experience"]) +
            (project_results["score"] * self.weights["projects"]) +
            (cert_results["score"] * self.weights["certifications"]) +
            (format_results["score"] * self.weights["formatting"])
        )

        return {
            "overall_score": round(total_score, 2),
            "breakdown": {
                "keywords": keyword_results,
                "experience": experience_results,
                "projects": project_results,
                "certifications": cert_results,
                "formatting": format_results
            },
            "suggestions": self._generate_suggestions(
                keyword_results, experience_results, project_results, cert_results, format_results
            )
        }

    def _score_keywords(self, resume_data: Dict[str, Any], jd: str) -> Dict[str, Any]:
        """Calculates keyword match percentage."""
        jd_keywords = self._extract_keywords(jd)
        resume_text = (resume_data.get("raw_text", "") + " " + resume_data.get("sections", {}).get("skills", "")).lower()
        resume_keywords = self._extract_keywords(resume_text)
        
        matches = jd_keywords.intersection(resume_keywords)
        missing = jd_keywords - resume_keywords
        
        match_ratio = len(matches) / len(jd_keywords) if jd_keywords else 0
        score = min(match_ratio * 100, 100)
        
        return {
            "score": score,
            "matching_keywords": list(matches)[:10], # top 10 for feedback
            "missing_keywords": list(missing)[:10]
        }

    def _score_experience(self, exp_text: str, jd: str) -> Dict[str, Any]:
        """Heuristic experience scoring based on keyword overlap in experience section."""
        if not exp_text.strip():
            return {"score": 0, "message": "No experience section found."}
        
        # Simple heuristic: density of JD keywords in experience section
        jd_keywords = self._extract_keywords(jd)
        exp_keywords = self._extract_keywords(exp_text)
        
        matches = jd_keywords.intersection(exp_keywords)
        # We expect a lower density here than in skills, so we scale it
        score = min((len(matches) / (len(jd_keywords) * 0.5 if jd_keywords else 1)) * 100, 100)
        
        return {
            "score": score,
            "relevant_terms_found": list(matches)[:5]
        }

    def _score_projects(self, project_text: str) -> Dict[str, Any]:
        """Scores projects based on presence and length."""
        if not project_text.strip():
            return {"score": 0, "message": "No projects section found."}
        
        # Heuristic: More content usually means more detail
        word_count = len(project_text.split())
        score = 0
        if word_count > 100: score = 100
        elif word_count > 50: score = 70
        else: score = 40
        
        return {"score": score, "word_count": word_count}

    def _score_certifications(self, cert_text: str) -> Dict[str, Any]:
        """Presence check for certifications."""
        score = 100 if cert_text.strip() else 0
        return {"score": score}

    def _score_formatting(self, sections: Dict[str, str]) -> Dict[str, Any]:
        """Checks if standard sections exist."""
        required = ["education", "experience", "skills"]
        found = [s for s in required if sections.get(s, "").strip()]
        
        score = (len(found) / len(required)) * 100
        return {
            "score": score,
            "missing_sections": [s for s in required if s not in found]
        }

    def _generate_suggestions(self, kw, exp, proj, cert, fmt) -> List[str]:
        suggestions = []
        if kw["score"] < 70:
            suggestions.append(f"Add more keywords from the job description, especially: {', '.join(kw['missing_keywords'][:3])}")
        if exp["score"] < 50:
            suggestions.append("Tailor your experience bullet points to better match the target role's requirements.")
        if proj["score"] == 0:
            suggestions.append("Add a projects section to demonstrate practical application of your skills.")
        if fmt["score"] < 100:
            suggestions.append(f"Ensure your resume has these standard sections: {', '.join(fmt['missing_sections'])}")
        
        return suggestions

    def _extract_keywords(self, text: str) -> Set[str]:
        # Filtered set of words
        try:
            from nltk.corpus import stopwords
            stop_words = set(stopwords.words('english'))
        except (ImportError, LookupError):
            # Fallback if nltk not installed or data not downloaded
            stop_words = {"this", "that", "with", "from", "and", "the", "for", "are", "also", "your", "have", "been", "was"}
            
        words = re.findall(r'\b\w{3,}\b', text.lower())
        return set([w for w in words if w not in stop_words])

if __name__ == "__main__":
    # Quick test
    scorer = ATSScorer()
    dummy_resume = {
        "raw_text": "Python developer with experience in Flask and SQL. Certified AWS Architect.",
        "sections": {
            "skills": "Python, Flask, SQL, AWS",
            "experience": "Worked as a developer at Tech Inc.",
            "projects": "Built a web app with Flask.",
            "certifications": "AWS Certified Solutions Architect",
            "education": "BS in CS"
        }
    }
    jd = "Seeking a Python developer who knows Flask, SQL, and Docker. AWS experience is a plus."
    
    result = scorer.calculate_score(dummy_resume, jd)
    import json
    print(json.dumps(result, indent=2))

import re
import logging
from typing import Dict, List, Any, Set
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SkillGapAnalyzer:
    """
    Analyzes the gap between resume skills and job requirements using 
    semantic similarity and keyword matching.
    """

    def __init__(self):
        # Heuristic threshold for "weak" vs "strong" match in semantic space
        self.similarity_threshold = 0.4

    def analyze(self, resume_skills: List[str], required_skills: List[str]) -> Dict[str, Any]:
        """
        Compares resume skills against required skills.
        :param resume_skills: List of skills extracted from resume
        :param required_skills: List of skills required for the target role
        """
        if not resume_skills:
            return {
                "strong_matches": [],
                "weak_matches": [],
                "missing_skills": required_skills,
                "match_percentage": 0
            }

        # Normalize skills
        resume_skills_norm = [s.lower().strip() for s in resume_skills if s.strip()]
        required_skills_norm = [s.lower().strip() for s in required_skills if s.strip()]

        strong_matches = []
        weak_matches = []
        missing_skills = []

        if SKLEARN_AVAILABLE and len(resume_skills_norm) > 0 and len(required_skills_norm) > 0:
            # Semantic matching using TF-IDF and Cosine Similarity
            for req_skill in required_skills_norm:
                similarities = self._calculate_similarities(req_skill, resume_skills_norm)
                max_sim = max(similarities) if similarities else 0
                
                if max_sim >= 0.9: # Exact or near-exact match
                    strong_matches.append(req_skill)
                elif max_sim >= self.similarity_threshold:
                    weak_matches.append({
                        "skill": req_skill,
                        "matched_with": resume_skills_norm[similarities.index(max_sim)],
                        "similarity": round(max_sim, 2)
                    })
                else:
                    missing_skills.append(req_skill)
        else:
            # Fallback to simple keyword matching if sklearn is missing
            logger.warning("Scikit-learn not available. Falling back to basic matching.")
            for req_skill in required_skills_norm:
                if req_skill in resume_skills_norm:
                    strong_matches.append(req_skill)
                else:
                    # Simple substring match fallback
                    found = False
                    for res_skill in resume_skills_norm:
                        if req_skill in res_skill or res_skill in req_skill:
                            weak_matches.append({"skill": req_skill, "matched_with": res_skill})
                            found = True
                            break
                    if not found:
                        missing_skills.append(req_skill)

        total_req = len(required_skills_norm)
        match_percentage = ((len(strong_matches) + len(weak_matches) * 0.5) / total_req * 100) if total_req > 0 else 0

        return {
            "match_percentage": round(match_percentage, 2),
            "strong_matches": strong_matches,
            "weak_matches": weak_matches,
            "missing_skills": missing_skills
        }

    def _calculate_similarities(self, target: str, source_list: List[str]) -> List[float]:
        """Calculates cosine similarity between a target string and a list of strings."""
        corpus = [target] + source_list
        vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4))
        try:
            tfidf = vectorizer.fit_transform(corpus)
            words_vector = tfidf[0:1]
            corpus_vectors = tfidf[1:]
            
            sims = cosine_similarity(words_vector, corpus_vectors).flatten()
            return sims.tolist()
        except:
            return [0.0] * len(source_list)

if __name__ == "__main__":
    analyzer = SkillGapAnalyzer()
    res_skills = ["Python", "Flask", "React.js", "PostgreSQL", "Machine Learning"]
    req_skills = ["Python", "FastAPI", "React", "SQL", "Deep Learning", "Docker"]
    
    report = analyzer.analyze(res_skills, req_skills)
    import json
    print(json.dumps(report, indent=2))

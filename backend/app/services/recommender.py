import logging
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Recommender:
    """
    Generates personalized project recommendations and resume improvements
    based on skill gaps and target roles.
    """

    def __init__(self):
        # Sample knowledge base for project recommendations
        # In Phase 2, this will be augmented by LLM/Vector Store
        self.project_templates = {
            "python": [
                {
                    "title": "Automated Trading Bot",
                    "tech_stack": ["Python", "Pandas", "API Integration"],
                    "difficulty": "Intermediate",
                    "description": "Develop a bot that fetches real-time market data and executes trades based on technical indicators.",
                    "bullets": [
                        "Architected a real-time data pipeline using Python and REST APIs to process market volatility.",
                        "Implemented technical analysis algorithms using Pandas, resulting in a 15% improvement in strategy backtesting efficiency."
                    ]
                },
                {
                    "title": "RESTful API with Flask/FastAPI",
                    "tech_stack": ["Python", "FastAPI", "PostgreSQL", "Docker"],
                    "difficulty": "Beginner",
                    "description": "Build a scalable backend API for a task management system with JWT authentication.",
                    "bullets": [
                        "Developed a high-performance RESTful API using FastAPI and PostgreSQL, handling 500+ requests per second.",
                        "Containerized the application using Docker, reducing deployment time by 40%."
                    ]
                }
            ],
            "react": [
                {
                    "title": "Interactive Dashboard",
                    "tech_stack": ["React", "Tailwind CSS", "Recharts"],
                    "difficulty": "Intermediate",
                    "description": "Create a data visualization dashboard for tracking personal finance or SaaS metrics.",
                    "bullets": [
                        "Built a responsive analytics dashboard using React and Tailwind CSS, improving user engagement by 25%.",
                        "Integrated Recharts for dynamic data visualization, enabling users to track complex metrics in real-time."
                    ]
                }
            ],
            "machine learning": [
                {
                    "title": "Sentiment Analysis Tool",
                    "tech_stack": ["Python", "Scikit-learn", "NLTK", "Flask"],
                    "difficulty": "Intermediate",
                    "description": "Build a tool that analyzes social media sentiment for specific brands or products.",
                    "bullets": [
                        "Developed a sentiment analysis engine using Scikit-learn and NLTK with an 85% accuracy rate on Twitter data.",
                        "Deployed the model as a web service using Flask, providing real-time insights via a REST API."
                    ]
                }
            ],
            "docker": [
                {
                    "title": "Microservices Orchestration",
                    "tech_stack": ["Docker", "Docker Compose", "Nginx", "Redis"],
                    "difficulty": "Advanced",
                    "description": "Set up a multi-container environment with load balancing and caching.",
                    "bullets": [
                        "Optimized system architecture by implementing Docker Compose for microservices orchestration.",
                        "Configured Nginx as a reverse proxy and Redis for caching, reducing latency by 30%."
                    ]
                }
            ]
        }

    def generate_recommendations(self, missing_skills: List[str], target_role: str) -> Dict[str, Any]:
        """
        Generates project ideas and resume improvements.
        """
        recommendations = []
        seen_projects = set()

        # Map missing skills to projects
        for skill in missing_skills:
            skill_lower = skill.lower()
            for key, projects in self.project_templates.items():
                if key in skill_lower or skill_lower in key:
                    for proj in projects:
                        if proj["title"] not in seen_projects:
                            recommendations.append(proj)
                            seen_projects.add(proj["title"])

        # If no specific skill matches, provide general role-based projects
        if not recommendations:
            # Fallback to general projects if the list is empty
            recommendations = self.project_templates.get("python", [])[:2]

        return {
            "target_role": target_role,
            "recommended_projects": recommendations[:3], # Return top 3
            "general_tips": [
                "Quantify your achievements using the Google X-Y-Z formula (Accomplished [X] as measured by [Y], by doing [Z]).",
                "Ensure your GitHub profile has a clean README for your top 3 projects.",
                "Include a 'Technical Skills' section categorized by Languages, Frameworks, and Tools."
            ]
        }

if __name__ == "__main__":
    recommender = Recommender()
    missing = ["Docker", "React"]
    results = recommender.generate_recommendations(missing, "Full Stack Developer")
    
    import json
    print(json.dumps(results, indent=2))

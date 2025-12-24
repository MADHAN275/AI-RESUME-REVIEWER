import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.app.services.vector_store import VectorStore

def seed_data():
    print("Seeding Vector Store with initial roles...")
    vs = VectorStore()
    
    roles = [
        {
            "title": "Frontend Developer",
            "skills": ["React", "JavaScript", "HTML", "CSS", "TypeScript", "Redux", "Tailwind CSS"],
            "description": "Responsible for building interactive user interfaces and web applications using modern frontend frameworks."
        },
        {
            "title": "Backend Developer",
            "skills": ["Python", "Flask", "Django", "SQL", "PostgreSQL", "Redis", "API Design", "Docker"],
            "description": "Focuses on server-side logic, database management, and API integration for web applications."
        },
        {
            "title": "Full Stack Developer",
            "skills": ["React", "Node.js", "Python", "SQL", "MongoDB", "AWS", "Git", "System Design"],
            "description": "Versatile developer capable of working on both client-side and server-side of the application."
        },
        {
            "title": "Machine Learning Engineer",
            "skills": ["Python", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "MLOps", "Model Deployment"],
            "description": "Designs and implements machine learning models and systems to solve complex data problems."
        },
        {
            "title": "DevOps Engineer",
            "skills": ["AWS", "Docker", "Kubernetes", "Jenkins", "CI/CD", "Terraform", "Linux", "Bash Scripting"],
            "description": "Manages infrastructure as code, automated deployment pipelines, and ensures system reliability."
        },
        {
            "title": "Data Scientist",
            "skills": ["Python", "R", "SQL", "Statistics", "Data Visualization", "Machine Learning", "Jupyter"],
            "description": "Analyzes large datasets to extract actionable insights and build predictive models."
        }
    ]
    
    vs.add_roles(roles)
    print("Seeding complete.")

if __name__ == "__main__":
    seed_data()

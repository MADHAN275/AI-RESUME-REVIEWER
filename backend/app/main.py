import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import tempfile

# Import services
from .services.resume_parser import ResumeParser
from .services.ats_score import ATSScorer
from .services.skill_gap import SkillGapAnalyzer
from .services.recommender import Recommender
from .services.vector_store import VectorStore
from .services.llm_agent import LLMAgent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for frontend communication

    # Initialize Services
    parser = ResumeParser()
    ats_scorer = ATSScorer()
    skill_gap_analyzer = SkillGapAnalyzer()
    recommender = Recommender()
    vector_store = VectorStore()
    llm_agent = LLMAgent()

    # Configuration
    UPLOAD_FOLDER = tempfile.gettempdir()
    ALLOWED_EXTENSIONS = {'pdf'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "service": "AI Resume Reviewer"}), 200

    @app.route('/api/upload', methods=['POST'])
    def upload_resume():
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
            
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                
                # Parse the resume
                resume_data = parser.parse(file_path)
                
                # Clean up file
                os.remove(file_path)
                
                return jsonify({
                    "message": "Resume parsed successfully",
                    "data": resume_data
                }), 200
            except Exception as e:
                logger.error(f"Error processing file: {e}")
                return jsonify({"error": str(e)}), 500
        else:
            return jsonify({"error": "Invalid file type. Only PDF allowed."}), 400

    @app.route('/api/analyze', methods=['POST'])
    def analyze_resume():
        """
        Expects JSON body:
        {
            "resume_data": { ... }, # Output from /upload
            "target_role": "Full Stack Developer", 
            "job_description": "Optional raw text JD..." 
        }
        """
        data = request.json
        if not data or 'resume_data' not in data or 'target_role' not in data:
            return jsonify({"error": "Missing resume_data or target_role"}), 400

        resume_data = data['resume_data']
        target_role = data['target_role']
        job_description = data.get('job_description', "")

        try:
            # 1. Get Job Requirements (from VectorStore if JD not provided)
            # For now, if JD is empty, we search for the role description
            if not job_description and vector_store:
                roles = vector_store.search_similar_roles(target_role, k=1)
                if roles:
                    # Construct a pseudo-JD from the found role
                    found_role = roles[0]
                    job_description = f"{found_role['title']} {found_role['description']} {' '.join(found_role.get('skills', []))}"
                    required_skills = found_role.get('skills', [])
                else:
                    # Fallback defaults
                    required_skills = ["Python", "JavaScript", "SQL", "Git"] # Generic fallback
            else:
                # If JD provided, we'd ideally extract skills from it. 
                # For this phase, we assume basic keywords extraction or client sends req skills.
                # Simplification: assume client might send 'required_skills' or we use ATS keyword extraction
                required_skills = list(ats_scorer._extract_keywords(job_description))

            # 2. Hybrid Analysis: Rule-based + LLM
            
            # Rule-based (Fast, Cheap, Deterministic)
            ats_results = ats_scorer.calculate_score(resume_data, job_description)
            
            # Extract skills from resume (using the parsed section)
            resume_skills_text = resume_data['sections'].get('skills', "")
            resume_skills_list = [s.strip() for s in resume_skills_text.split(',') if s.strip()]
            
            gap_results = skill_gap_analyzer.analyze(resume_skills_list, required_skills)
            
            rec_results = recommender.generate_recommendations(
                gap_results['missing_skills'], 
                target_role
            )
            
            # LLM-based (Deep, Insightful, but optional/expensive)
            llm_results = llm_agent.analyze_resume(resume_data, target_role, required_skills)
            
            # Merge or Return structured response
            # We will prioritize LLM suggestions but keep rule-based scores as baseline
            
            response_payload = {
                "ats_analysis": ats_results,
                "skill_gap": gap_results,
                "recommendations": rec_results,
                "llm_insights": llm_results,
                "target_role_data": {
                    "role": target_role,
                    "description_used": job_description[:200] + "..." if job_description else "Generic"
                }
            }

            return jsonify(response_payload), 200

        except Exception as e:
            logger.error(f"Error analyzing resume: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @app.route('/api/chat', methods=['POST'])
    def chat_agent():
        """
        Chat with the mentor agent.
        Body: { "message": "How do I learn Docker?", "context": "optional resume context" }
        """
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"error": "Message required"}), 400
        
        message = data['message']
        context = data.get('context')
        
        response = llm_agent.chat_with_mentor(message, context)
        
        return jsonify({"reply": response}), 200

    @app.route('/api/roles', methods=['GET'])
    def get_roles():
        """Returns list of common roles to populate frontend selector."""
        # In a real app, this might query the DB. Here we return seed data + whatever is in vector store.
        # For simplicity, we just return a static list for now or search empty to get some?
        # Let's just return a static list of popular tech roles.
        common_roles = [
            "Frontend Developer", "Backend Developer", "Full Stack Developer", 
            "Data Scientist", "Machine Learning Engineer", "DevOps Engineer",
            "Product Manager", "UI/UX Designer"
        ]
        return jsonify(common_roles), 200

    return app

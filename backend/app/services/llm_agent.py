import os
import json
import logging
from typing import Dict, Any, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# from langchain.memory import ConversationBufferMemory 

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LLMAgent:
    """
    Orchestrates LangChain agents for resume analysis and mentorship.
    """
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.llm = None
        # self.mentor_memory = ConversationBufferMemory(return_messages=True)
        
        if self.api_key:
            try:
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo", # Cost-effective model
                    temperature=0.7,
                    api_key=self.api_key
                )
                logger.info("LLM Agent initialized with OpenAI.")
            except Exception as e:
                logger.error(f"Failed to initialize ChatOpenAI: {e}")
        else:
            logger.warning("OPENAI_API_KEY not found. LLM features will be disabled/mocked.")

    def analyze_resume(self, resume_data: Dict[str, Any], target_role: str, job_requirements: List[str]) -> Dict[str, Any]:
        """
        Uses LLM to perform deep analysis of the resume against the target role.
        """
        if not self.llm:
            return self._mock_analysis(target_role)

        # parser = JsonOutputParser() # Requires pydantic object definition or robust prompting
        # We will use a strong system prompt to enforce JSON
        
        system_prompt = """
        You are an expert AI Career Coach and Resume Reviewer. 
        Your task is to analyze a candidate's resume against a specific target role.
        
        Output MUST be a valid JSON object with the following structure:
        {
            "ats_score": {
                "score": <0-100>,
                "explanation": "<string>"
            },
            "missing_skills": ["<skill1>", "<skill2>", "<skill3>"],
            "project_recommendations": [
                {
                    "title": "<title>",
                    "tech_stack": ["<tech1>", "<tech2>"],
                    "impact": "<description>"
                }
            ],
            "learning_roadmap": ["<month1_goal>", "<month2_goal>", "<month3_goal>"],
            "resume_improvements": ["<tip1>", "<tip2>"]
        }
        """

        human_prompt = f"""
        RESUME DATA:
        {json.dumps(resume_data, default=str)}

        TARGET ROLE:
        {target_role}

        JOB REQUIREMENTS:
        {', '.join(job_requirements)}
        
        Analyze and provide the JSON output.
        """

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            response = self.llm.invoke(messages)
            content = response.content
            
            # Clean up potential markdown formatting (```json ... ```)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].strip()

            return json.loads(content)
        except Exception as e:
            logger.error(f"LLM Analysis failed: {e}")
            return self._mock_analysis(target_role)

    def chat_with_mentor(self, message: str, context: Optional[str] = None) -> str:
        """
        Conversational interface for career mentoring.
        """
        if not self.llm:
            return "I am currently in offline mode. Please configure my OpenAI API key to enable chat."

        system_instruction = """You are a helpful and encouraging Career Mentor. 
        Answer questions briefly and professionally. 
        If context about the user's resume is available, use it to personalize advice."""
        
        if context:
            system_instruction += f"\n\nUSER CONTEXT:\n{context}"

        # In a real app, we'd persist history per session_id.
        # Here we just use a simple memory instance for demonstration or stateless for API.
        # For an API, typically we pass history in the request. 
        # For simplicity, we'll just treat it as a single turn + system prompt.
        
        messages = [
            SystemMessage(content=system_instruction),
            HumanMessage(content=message)
        ]
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Chat failed: {e}")
            return "I'm having trouble thinking right now. Please try again later."

    def _mock_analysis(self, target_role: str) -> Dict[str, Any]:
        """Fallback mock response when LLM is unavailable."""
        logger.info("Returning mock analysis data.")
        return {
            "ats_score": {
                "score": 75,
                "explanation": "Mock Score: Good keyword density but missing some advanced terms."
            },
            "missing_skills": ["Advanced Pattern Matching", "System Design", "Cloud Native"],
            "project_recommendations": [
                {
                    "title": f"Advanced {target_role} System",
                    "tech_stack": ["Relevant Tech 1", "Relevant Tech 2"],
                    "impact": "Build a scalable system to demonstrate architecture skills."
                }
            ],
            "learning_roadmap": [
                "Month 1: Master fundamentals and missing skills.",
                "Month 2: Build a capstone project.",
                "Month 3: Mock interviews and system design."
            ],
            "resume_improvements": [
                "Quantify your bullet points more.",
                "Add a summary section specific to this role."
            ]
        }

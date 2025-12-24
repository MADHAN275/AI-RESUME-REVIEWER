# AI Resume Reviewer & Career Mentor

An AI-powered web application that analyzes resumes, calculates ATS compatibility scores, identifies skill gaps, and provides personalized career recommendations and interactive mentorship.

## 🚀 Features

- **Intelligent PDF Parsing**: Extracts structured data (Skills, Experience, Education) from PDF resumes.
- **ATS Scoring**: Calculates a compatibility score (0-100) based on keyword density, formatting, and relevance.
- **Skill Gap Analysis**: Uses semantic similarity (TF-IDF + Cosine Similarity) to identify missing or weak skills compared to target roles.
- **Project Recommendations**: Suggests technical projects with tech stacks and resume-ready bullet points to bridge skill gaps.
- **AI Career Mentor**: Interactive chatbot powered by LangChain and OpenAI for personalized career advice.
- **Job Role Database**: Vector-based search (FAISS) for various tech roles (Frontend, Backend, ML, DevOps, etc.).

## 🛠️ Technical Stack

- **Backend**: Flask (Python)
- **Frontend**: React (TypeScript) + Tailwind CSS + Framer Motion
- **AI/ML**: LangChain, OpenAI API, FAISS, Sentence-Transformers (all-MiniLM-L6-v2)
- **Data Visualization**: Recharts

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- OpenAI API Key (Optional, but recommended for advanced AI features)

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AI-RESUME-REVIEWER
```

### 2. Backend Setup
```bash
cd backend
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set Environment Variables
# Create a .env file in the backend directory
echo "OPENAI_API_KEY=your_key_here" > .env

# Seed the Job Role Database
python scripts/seed_roles.py

# Run the server
python run.py
```
The backend will run on `http://localhost:5000`.

### 3. Frontend Setup
```bash
cd frontend
# Install dependencies
npm install

# Run the development server
npm run dev
```
The frontend will run on `http://localhost:5173`.

## 📂 Folder Structure

```text
/
├── backend/
│   ├── app/
│   │   ├── services/       # Core logic (Parser, Scorer, LLM, etc.)
│   │   └── main.py         # Flask API routes
│   ├── scripts/            # Database seeding scripts
│   ├── tests/              # Unit and integration tests
│   └── run.py              # Application entry point
├── frontend/
│   ├── src/
│   │   ├── components/     # UI components (Dashboard, Chat, etc.)
│   │   ├── services/       # API client
│   │   └── App.tsx         # Main application flow
│   └── tailwind.config.js  # Styling configuration
└── README.md
```

## 🧪 Running Tests
```bash
cd backend
python -m unittest discover tests
```

## 🌐 Deployment (Recommended)

- **Backend**: Deploy to [Render](https://render.com/) or [Heroku].
  - Ensure `FAISS_INDEX_PATH` points to a writable directory if using persistence.
- **Frontend**: Deploy to [Vercel](https://vercel.com/) or [Netlify].
  - Update `API_URL` in `frontend/src/services/api.ts` to your production backend URL.

## 📄 License
MIT

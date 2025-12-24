import logging
import os
import json
import pickle
from typing import List, Dict, Any, Optional
import numpy as np

try:
    import faiss
    from sentence_transformers import SentenceTransformer
    VECTOR_SEARCH_AVAILABLE = True
except ImportError:
    VECTOR_SEARCH_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VectorStore:
    """
    Manages the FAISS vector database for job roles.
    Uses sentence-transformers for generating embeddings.
    """

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', index_path: str = "backend/data/faiss_index.bin"):
        self.index_path = index_path
        self.metadata_path = index_path.replace(".bin", "_meta.pkl")
        self.roles_metadata: List[Dict[str, Any]] = []
        self.index = None
        
        if VECTOR_SEARCH_AVAILABLE:
            try:
                self.model = SentenceTransformer(model_name)
                logger.info(f"Loaded embedding model: {model_name}")
                self._load_index()
            except Exception as e:
                logger.error(f"Failed to initialize embedding model: {e}")
                self.model = None

    def _load_index(self):
        """Loads FAISS index and metadata from disk if they exist."""
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            try:
                self.index = faiss.read_index(self.index_path)
                with open(self.metadata_path, 'rb') as f:
                    self.roles_metadata = pickle.load(f)
                logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors.")
            except Exception as e:
                logger.error(f"Error loading FAISS index: {e}")
                self._create_new_index()
        else:
            self._create_new_index()

    def _create_new_index(self):
        """Initializes a new FAISS index."""
        if self.model:
            # Dimension of all-MiniLM-L6-v2 is 384
            d = self.model.get_sentence_embedding_dimension()
            self.index = faiss.IndexFlatL2(d)
            self.roles_metadata = []
            logger.info(f"Created new FAISS index with dimension {d}.")

    def add_roles(self, roles: List[Dict[str, Any]]):
        """
        Adds new job roles to the vector store.
        :param roles: List of dicts containing 'title', 'skills', 'description'
        """
        if not VECTOR_SEARCH_AVAILABLE or not self.model:
            logger.warning("Vector search not available. Cannot add roles.")
            return

        texts = [f"{r['title']} {r.get('description', '')} {' '.join(r.get('skills', []))}" for r in roles]
        embeddings = self.model.encode(texts)
        
        if self.index is None:
            self._create_new_index()
            
        self.index.add(np.array(embeddings).astype('float32'))
        self.roles_metadata.extend(roles)
        logger.info(f"Added {len(roles)} roles to index.")
        
        # Auto-save
        self.save_index()

    def search_similar_roles(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Searches for roles similar to the query string (e.g., resume text or job title).
        """
        if not VECTOR_SEARCH_AVAILABLE or not self.index or self.index.ntotal == 0:
            logger.warning("Vector search unavailable or index empty.")
            return []

        query_vector = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_vector).astype('float32'), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.roles_metadata):
                role = self.roles_metadata[idx]
                # Add distance score for reference (lower is better in L2)
                role_copy = role.copy()
                role_copy["similarity_score"] = float(distances[0][i])
                results.append(role_copy)
                
        return results

    def save_index(self):
        """Persists the index and metadata to disk."""
        if not self.index: return
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        
        try:
            faiss.write_index(self.index, self.index_path)
            with open(self.metadata_path, 'wb') as f:
                pickle.dump(self.roles_metadata, f)
            logger.info("Saved FAISS index to disk.")
        except Exception as e:
            logger.error(f"Failed to save index: {e}")

if __name__ == "__main__":
    # Initialize and populate with some dummy data if empty
    vs = VectorStore()
    
    sample_roles = [
        {
            "title": "Python Backend Developer",
            "skills": ["Python", "Flask", "SQL", "Redis"],
            "description": "Build scalable backend APIs."
        },
        {
            "title": "Frontend Engineer",
            "skills": ["React", "JavaScript", "CSS", "Redux"],
            "description": "Create responsive user interfaces."
        },
        {
            "title": "Machine Learning Engineer",
            "skills": ["Python", "PyTorch", "TensorFlow", "Pandas"],
            "description": "Train and deploy ML models."
        }
    ]
    
    if VECTOR_SEARCH_AVAILABLE:
        vs.add_roles(sample_roles)
        results = vs.search_similar_roles("I love building APIs with Python")
        import json
        print(json.dumps(results, indent=2))
    else:
        print("Vector search libraries (faiss, sentence-transformers) not installed.")

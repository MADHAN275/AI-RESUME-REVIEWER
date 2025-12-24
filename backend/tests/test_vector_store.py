import unittest
import sys
import os
import shutil

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.app.services.vector_store import VectorStore, VECTOR_SEARCH_AVAILABLE

class TestVectorStore(unittest.TestCase):
    def setUp(self):
        # Use a temp path for testing to avoid overwriting real data
        self.test_index_path = "backend/tests/temp_data/test_index.bin"
        self.vs = VectorStore(index_path=self.test_index_path)
        
        self.sample_roles = [
            {"title": "DevOps Engineer", "skills": ["Docker", "Kubernetes", "AWS"], "description": "Infra as code."},
            {"title": "Data Scientist", "skills": ["Python", "Statistics", "Jupyter"], "description": "Analyze data."}
        ]

    def tearDown(self):
        # Cleanup
        if os.path.exists(os.path.dirname(self.test_index_path)):
            shutil.rmtree(os.path.dirname(self.test_index_path))

    def test_add_and_search(self):
        if not VECTOR_SEARCH_AVAILABLE:
            print("Skipping vector store test (libraries missing)")
            return

        self.vs.add_roles(self.sample_roles)
        
        # Search for something related to DevOps
        results = self.vs.search_similar_roles("Kubernetes and cloud infrastructure")
        
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]["title"], "DevOps Engineer")

    def test_persistence(self):
        if not VECTOR_SEARCH_AVAILABLE:
            return

        self.vs.add_roles(self.sample_roles)
        
        # Create a new instance pointing to the same path
        vs2 = VectorStore(index_path=self.test_index_path)
        self.assertEqual(len(vs2.roles_metadata), 2)
        self.assertEqual(vs2.index.ntotal, 2)

if __name__ == '__main__':
    unittest.main()

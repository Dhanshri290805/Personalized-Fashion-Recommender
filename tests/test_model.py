import os
import sys
import unittest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.fashion_recommender import FashionRecommendationModel
from backend.main import app

class TestFashionRecommendation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = FashionRecommendationModel()
        cls.model.load_model('saved_models/model.pkl')
        cls.client = TestClient(app)

    def test_01_dataset_loading(self):
        self.assertIsNotNone(self.model.items_df)
        self.assertGreater(len(self.model.items_df), 0)

    def test_02_feature_generation(self):
        self.assertIsNotNone(self.model.tfidf_matrix)

    def test_03_similarity_calculation(self):
        self.assertIsNotNone(self.model.content_similarity_matrix)

    def test_04_recommendation_generation(self):
        recs = self.model.recommend_items({"category": "T-shirt", "color": "Black"}, top_n=5)
        self.assertEqual(len(recs), 5)

    def test_05_outfit_generation(self):
        outfit = self.model.generate_outfit({"style": "Casual"})
        self.assertIn('top', outfit)
        self.assertIn('bottom', outfit)
        self.assertIn('shoes', outfit)
        self.assertIn('compatibility_score', outfit)

    def test_06_api_health(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "model": "fashion-recommender"})

if __name__ == '__main__':
    unittest.main()

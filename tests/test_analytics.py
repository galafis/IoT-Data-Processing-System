import unittest
import pandas as pd
from src.analytics import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = DataAnalyzer()
        # Forcing a specific dataset for reproducible tests
        self.sample_data = pd.DataFrame({
            'feature1': [1.0, 2.0, 3.0, 4.0, 5.0],
            'feature2': [5.0, 4.0, 3.0, 2.0, 1.0],
            'feature3': [1.0, 1.0, 0.0, 0.0, 1.0],
            'target': [0, 1, 0, 1, 0]
        })
        self.analyzer.load_data(self.sample_data)

    def test_load_data(self):
        self.assertIsNotNone(self.analyzer.data)
        self.assertEqual(self.analyzer.data.shape, (5, 4))

    def test_analyze(self):
        results = self.analyzer.analyze()
        self.assertIn('statistics', results)
        self.assertIn('classification_report', results)
        self.assertIsNotNone(self.analyzer.model)

    def test_visualize(self):
        # This test primarily checks if the visualize method runs without errors
        # and creates a file. Actual image content validation is complex.
        try:
            self.analyzer.visualize(repo_name="test_repo")
            # Check if the file was created
            import os
            self.assertTrue(os.path.exists("test_repo_analysis.png"))
            os.remove("test_repo_analysis.png") # Clean up
        except Exception as e:
            self.fail(f"Visualização falhou com erro: {e}")

if __name__ == '__main__':
    unittest.main()


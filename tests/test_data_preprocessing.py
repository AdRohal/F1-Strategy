# tests/test_data_preprocessing.py

import unittest
import pandas as pd
from src.data_preprocessing.preprocess_weather import preprocess_weather_data
from src.data_preprocessing.preprocess_tire_data import preprocess_tire_data

class TestDataPreprocessing(unittest.TestCase):

    def test_preprocess_weather_data(self):
        sample_data = {
            'timestamp': ['2024-08-01 00:00:00', '2024-08-01 01:00:00'],
            'temperature': [22, 21],
            'humidity': [60, 65],
            'wind_speed': [5, 3],
            'precipitation': [0, 0.2]
        }
        df = pd.DataFrame(sample_data)
        processed_df = preprocess_weather_data(df)
        self.assertEqual(len(processed_df), 2)
        self.assertIn('temperature', processed_df.columns)
        self.assertIn('humidity', processed_df.columns)
        self.assertIn('wind_speed', processed_df.columns)
        self.assertIn('precipitation', processed_df.columns)

    def test_preprocess_tire_data(self):
        sample_data = {
            'timestamp': ['2024-08-01 00:00:00', '2024-08-01 01:00:00'],
            'tire_type': ['soft', 'medium'],
            'track_condition': ['dry', 'wet'],
            'duration': [90, 85]
        }
        df = pd.DataFrame(sample_data)
        processed_df = preprocess_tire_data(df)
        self.assertEqual(len(processed_df), 2)
        self.assertIn('tire_type', processed_df.columns)
        self.assertIn('track_condition', processed_df.columns)
        self.assertIn('duration', processed_df.columns)

if __name__ == '__main__':
    unittest.main()

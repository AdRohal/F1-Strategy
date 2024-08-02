# tests/test_ai_models.py

import unittest
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from src.ai_models.train_weather_model import train_weather_model
from src.ai_models.train_tire_model import train_tire_model

class TestAIModels(unittest.TestCase):

    def test_train_weather_model(self):
        sample_data = {
            'temperature': [22, 21],
            'humidity': [60, 65],
            'wind_speed': [5, 3],
            'precipitation': [0, 0.2]
        }
        df = pd.DataFrame(sample_data)
        model = train_weather_model(df)
        self.assertIsInstance(model, LinearRegression)

    def test_train_tire_model(self):
        sample_data = {
            'tire_type': ['soft', 'medium'],
            'track_condition': ['dry', 'wet'],
            'duration': [90, 85]
        }
        df = pd.DataFrame(sample_data)
        model = train_tire_model(df)
        self.assertIsInstance(model, RandomForestRegressor)

if __name__ == '__main__':
    unittest.main()

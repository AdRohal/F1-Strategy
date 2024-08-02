# tests/test_utils.py

import unittest
from unittest.mock import patch
from src.utils.fetch_weather_data import fetch_weather_data
from src.utils.calculate_strategy import calculate_tire_strategy

class TestUtils(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_current_weather(self, mock_get):
        # Mocked response data for testing
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'main': {
                'temp': 22,
                'humidity': 60
            },
            'wind': {
                'speed': 5
            },
            'weather': [
                {
                    'description': 'light rain'
                }
            ]
        }

        city_name = "London"
        weather_data = fetch_weather_data(city_name)

        self.assertIn('main', weather_data)
        self.assertIn('temp', weather_data['main'])
        self.assertIn('humidity', weather_data['main'])
        self.assertIn('wind', weather_data)
        self.assertIn('speed', weather_data['wind'])
        self.assertIn('weather', weather_data)
        self.assertGreater(len(weather_data['weather']), 0)

    def test_calculate_tire_strategy(self):
        current_weather = {
            'main': {
                'temp': 22,
                'humidity': 60
            },
            'wind': {
                'speed': 5
            },
            'weather': [
                {
                    'description': 'light rain'
                }
            ]
        }
        strategy = calculate_tire_strategy(current_weather)
        self.assertIn(strategy, ['soft', 'medium', 'hard', 'wet'])

if __name__ == '__main__':
    unittest.main()

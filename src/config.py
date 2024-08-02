# Configuration file for the F1 Strategy AI project

# API configurations

WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/"
WEATHER_API_KEY = "ad596998848da7dff630da3808b00665"
CURRENT_WEATHER_ENDPOINT = "weather?lat={}&lon={}&appid={}&units=metric"

# File paths
HISTORICAL_WEATHER_DATA_FILE = '../../data/historical/weather_data.csv'
HISTORICAL_TIRE_DATA_FILE = '../../data/historical/tire_performance.csv'
PREPROCESSED_WEATHER_DATA_FILE = '../../data/historical/preprocessed_weather_data.csv'
PREPROCESSED_TIRE_DATA_FILE = '../../data/historical/preprocessed_tire_data.csv'

MODEL_WEATHER_FILE = '../../models/weather_model.pkl'
MODEL_TIRE_FILE = '../../models/tire_model.pkl'

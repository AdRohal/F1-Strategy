import joblib
import pandas as pd

def load_models():
    weather_model = joblib.load('../../models/weather_model.pkl')
    tire_model = joblib.load('../../models/tire_model.pkl')
    return weather_model, tire_model

def predict_tire_strategy(weather_data, tire_model):
    tire_data = pd.get_dummies(weather_data, columns=['tire_type', 'track_condition'])
    tire_prediction = tire_model.predict(tire_data)
    return tire_prediction

def main():
    weather_model, tire_model = load_models()
    
    # Example current weather data for prediction
    current_weather = {
        'temperature': 26,
        'humidity': 78,
        'wind_speed': 3,
        'precipitation': 1.0,
        'tire_type': 'intermediate',
        'track_condition': 'wet'
    }
    
    current_weather_df = pd.DataFrame([current_weather])
    tire_strategy = predict_tire_strategy(current_weather_df, tire_model)
    
    print("Recommended tire strategy:", tire_strategy)

if __name__ == '__main__':
    main()

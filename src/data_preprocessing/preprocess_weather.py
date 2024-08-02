import pandas as pd

def preprocess_weather_data(input_file, output_file):
    weather_data = pd.read_csv(input_file)
    
    # Example preprocessing steps
    weather_data['timestamp'] = pd.to_datetime(weather_data['timestamp'])
    weather_data = weather_data.set_index('timestamp')
    
    weather_data.to_csv(output_file)

if __name__ == '__main__':
    preprocess_weather_data('../../data/historical/weather_data.csv', '../../data/historical/preprocessed_weather_data.csv')
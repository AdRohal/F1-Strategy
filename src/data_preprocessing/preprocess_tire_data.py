import pandas as pd

def preprocess_tire_data(input_file, output_file):
    tire_data = pd.read_csv(input_file)
    
    # Example preprocessing steps
    tire_data['timestamp'] = pd.to_datetime(tire_data['timestamp'])
    tire_data = tire_data.set_index('timestamp')
    
    tire_data.to_csv(output_file)

if __name__ == '__main__':
    preprocess_tire_data('../../data/historical/tire_performance.csv', '../../data/historical/preprocessed_tire_data.csv')
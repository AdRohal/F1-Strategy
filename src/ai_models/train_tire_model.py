import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load the data
tire_data = pd.read_csv('../../data/historical/tire_performance.csv')

# Example feature engineering
# Assuming tire_type and track_condition are categorical features
tire_data = pd.get_dummies(tire_data, columns=['tire_type', 'track_condition'])

X_train = tire_data.drop(columns=['duration'])
y_train = tire_data['duration']

# Train the model
tire_model = RandomForestRegressor()
tire_model.fit(X_train, y_train)

# Save the model
joblib.dump(tire_model, '../../models/tire_model.pkl')
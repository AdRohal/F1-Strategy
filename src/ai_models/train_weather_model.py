import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Load the data
weather_data = pd.read_csv('../../data/historical/weather_data.csv')

# Example feature engineering
X_train = weather_data[['temperature', 'humidity', 'wind_speed']]
y_train = weather_data['precipitation']

# Train the model
weather_model = LinearRegression()
weather_model.fit(X_train, y_train)

# Save the model
joblib.dump(weather_model, '../../models/weather_model.pkl')
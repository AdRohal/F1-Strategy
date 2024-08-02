# src/utils/calculate_strategy.py

def calculate_tire_strategy(weather_data):
    """
    Determine the best tire strategy based on current weather conditions.
    """
    temperature = weather_data.get('temperature', 0)
    humidity = weather_data.get('humidity', 0)
    wind_speed = weather_data.get('wind_speed', 0)
    precipitation = weather_data.get('precipitation', 0)

    def is_road_wet(precipitation):
        """Check if the road is wet based on precipitation."""
        return precipitation > 0.5
    
    def is_cold_temperature(temperature):
        """Check if the temperature is low enough to require hard tires."""
        return temperature < 10
    
    def is_moderate_temperature(temperature):
        """Check if the temperature is moderate for medium tires."""
        return 10 <= temperature < 20
    
    def is_hot_temperature(temperature):
        """Check if the temperature is high enough for soft tires."""
        return temperature >= 20
    
    # Determine tire strategy based on conditions
    if is_road_wet(precipitation):
        if precipitation > 5.0:
            return "Use Wet tires" 
        else:
            return "Use Intermediate tires"
    elif is_cold_temperature(temperature):
        return "Use Hard tires" 
    elif is_moderate_temperature(temperature):
        return "Use Medium tires"
    else:
        return "Use Soft tires"

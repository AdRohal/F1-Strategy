import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from utils.fetch_weather_data import fetch_current_weather
from utils.calculate_strategy import calculate_tire_strategy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

def plot_weather_data(ax, temperature, humidity, precipitation):
    ax.clear()
    ax.set_xlabel('Weather Parameters')
    ax.set_ylabel('Values')

    # Plot temperature
    ax.bar(['Temperature'], [temperature], color='tab:blue', label='Temperature (°C)')

    # Create a second y-axis for humidity and precipitation
    ax2 = ax.twinx()
    ax2.plot(['Humidity', 'Precipitation'], [humidity, precipitation], color='tab:orange', marker='o',
             label='Humidity (%) and Precipitation (mm)')
    ax2.set_ylabel('Humidity (%) and Precipitation (mm)')

    ax.set_title('Current Weather Data')

    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')

def plot_tire_strategy(ax, strategies):
    ax.clear()
    ax.bar(strategies.keys(), strategies.values(), color='tab:green')
    ax.set_xlabel('Tire Type')
    ax.set_ylabel('Suitability')
    ax.set_title('Tire Strategy Suitability')

def get_weather_data_for_location(circuit):
    circuits = {
        'Bahrain': ('26.0325', '50.5106'),
        'Saudi Arabia': ('21.5433', '39.1728'),
        'Australia': ('-37.814', '144.9633'),
        'Japan': ('34.8431', '136.5454'),
        'China': ('31.2304', '121.4737'),
        'Miami': ('25.7617', '-80.1918'),
        'Emilia Romagna': ('44.5462', '11.1474'),
        'Monaco': ('43.7333', '7.4167'),
        'Canada': ('45.4215', '-75.6972'),
        'Spain': ('41.3851', '2.1734'),
        'Austria': ('47.4333', '14.9167'),
        'Great Britain': ('52.0515', '-1.0164'),
        'Hungary': ('47.4979', '19.0402'),
        'Belgium': ('50.4372', '5.9716'),
        'Netherlands': ('52.3874', '4.6448'),
        'Italy': ('45.4642', '9.1900'),
        'Azerbaijan': ('40.4093', '49.8671'),
        'Singapore': ('1.3521', '103.8198'),
        'United States': ('30.2672', '-97.7431'),
        'Mexico': ('19.4326', '-99.1332'),
        'Brazil': ('-23.5505', '-46.6333'),
        'Las Vegas': ('36.1699', '-115.1398')
    }

    if circuit not in circuits:
        print("Circuit not found. Please choose from the list.")
        return None

    lat, lon = circuits[circuit]
    print(f"Fetching data for {circuit} with coordinates: lat={lat}, lon={lon}")

    return fetch_current_weather(lat, lon)

def update_tire_image(strategy, image_label):
    script_dir = os.path.dirname(__file__)
    image_folder = os.path.join(script_dir, '..', 'img')
    image_files = {
        'Use Wet tires': 'blue.png',
        'Use Intermediate tires': 'green.png',
        'Use Hard tires': 'white.png',
        'Use Medium tires': 'yellow.png',
        'Use Soft tires': 'red.png'
    }

    # Set default image
    image_file = image_files.get(strategy, 'red.png')

    # Load the image
    image_path = os.path.join(image_folder, image_file)
    try:
        img = Image.open(image_path)
        img = img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)

        # Update the label with the new image
        image_label.config(image=img_tk)
        image_label.image = img_tk
    except FileNotFoundError:
        print(f"File not found: {image_path}")
        image_label.config(image='')

def main():
    def on_submit():
        circuit = circuit_entry.get().strip()
        attack_type = attack_combobox.get()
        weather_data = get_weather_data_for_location(circuit)

        if weather_data:
            print("Current weather data:", weather_data)

            try:
                temperature_kelvin = weather_data['main']['temp']
                temperature_celsius = temperature_kelvin - 273.15

                current_weather = {
                    'temperature': temperature_celsius,
                    'humidity': weather_data['main']['humidity'],
                    'wind_speed': weather_data['wind']['speed'],
                    'precipitation': weather_data.get('rain', {}).get('1h', 0)
                }

                print("Current weather:", current_weather)

                print("Calculating tire strategy...")
                base_strategy = calculate_tire_strategy(current_weather)

                # Strategy based on attack type and weather conditions
                if attack_type == 'Super Attack':
                    if base_strategy == 'Use Wet tires':
                        strategy = 'Use Intermediate tires'
                    elif base_strategy == 'Use Intermediate tires':
                        strategy = 'Use Wet tires'
                    elif base_strategy == 'Use Hard tires':
                        strategy = 'Use Soft tires'
                    else:
                        strategy = 'Use Soft tires'
                elif attack_type == 'Attack':
                    if base_strategy == 'Use Wet tires':
                        strategy = 'Use Intermediate tires'
                    elif base_strategy == 'Use Intermediate tires':
                        strategy = 'Use Hard tires'
                    elif base_strategy == 'Use Hard tires':
                        strategy = 'Use Medium tires'
                    else:
                        strategy = 'Use Soft tires'
                else:
                    if base_strategy == 'Use Wet tires':
                        strategy = 'Use Intermediate tires'
                    else:
                        strategy = base_strategy

                print(f"Recommended tire strategy: {strategy}")

                # Clear previous plots
                for widget in weather_frame.winfo_children():
                    widget.destroy()
                for widget in strategy_frame.winfo_children():
                    widget.destroy()

                # Update weather plot
                fig_weather, weather_ax = plt.subplots(figsize=(4, 2))
                plot_weather_data(weather_ax, temperature_celsius, current_weather['humidity'],
                                  current_weather['precipitation'])
                weather_canvas = FigureCanvasTkAgg(fig_weather, master=weather_frame)
                weather_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                weather_canvas.draw()

                # Update tire strategy plot
                fig_strategy, strategy_ax = plt.subplots(figsize=(4, 2))
                plot_tire_strategy(strategy_ax, {
                    'Wet': 3 if current_weather['precipitation'] > 5.0 else 0,
                    'Intermediate': 2 if 0.5 < current_weather['precipitation'] <= 5.0 else 0,
                    'Hard': 2 if current_weather['temperature'] < 10 else 0,
                    'Medium': 2 if 10 <= current_weather['temperature'] < 20 else 0,
                    'Soft': 2 if current_weather['temperature'] >= 20 else 0
                })
                strategy_canvas = FigureCanvasTkAgg(fig_strategy, master=strategy_frame)
                strategy_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                strategy_canvas.draw()

                # Show strategy
                strategy_label.config(text=f"Recommended tire strategy: {strategy}")

                # Update tire image
                update_tire_image(strategy, image_label)

            except KeyError as e:
                print(f"Missing expected key in weather data: {e}")
                print("Weather data structure:", weather_data)
        else:
            print("Failed to fetch current weather data")

    # The main window
    window = tk.Tk()
    window.title("F1 Strategy")
    window.attributes('-fullscreen', True)  # Fullscreen mode

    # Frame for user input and circuit selection
    top_frame = tk.Frame(window)
    top_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=20)

    # Label to display the list of cities
    cities = [
        'Bahrain', 'Saudi Arabia', 'Australia', 'Japan', 'China', 'Miami', 'Emilia Romagna',
        'Monaco', 'Canada', 'Spain', 'Austria', 'Great Britain', 'Hungary', 'Belgium',
        'Netherlands', 'Italy', 'Azerbaijan', 'Singapore', 'United States', 'Mexico',
        'Brazil', 'Las Vegas'
    ]

    cities_label = tk.Label(top_frame, text="Available Circuits:\n" + "\n".join(cities))
    cities_label.pack(pady=10)

    # Label and entry for circuit input
    label = tk.Label(top_frame, text="Enter the name of the circuit:")
    label.pack(pady=10)

    circuit_entry = tk.Entry(top_frame)
    circuit_entry.pack(pady=5)

    # Label and combobox for attack type
    attack_label = tk.Label(top_frame, text="Select Attack Type:")
    attack_label.pack(pady=5)
    attack_types = ['Normal', 'Attack', 'Super Attack']
    attack_combobox = ttk.Combobox(top_frame, values=attack_types, state='readonly')
    attack_combobox.current(0)
    attack_combobox.pack(pady=5)

    # Submit button
    submit_button = tk.Button(top_frame, text="Submit", command=on_submit)
    submit_button.pack(pady=20)

    # Labels for strategy and tire image
    strategy_label = tk.Label(top_frame, text="", font=("Arial", 14))
    strategy_label.pack(pady=10)

    image_label = tk.Label(top_frame)
    image_label.pack(pady=10)

    # Frames for weather data plot and tire strategy plot
    weather_frame = tk.Frame(window)
    weather_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

    strategy_frame = tk.Frame(window)
    strategy_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

    window.mainloop()

if __name__ == "__main__":
    main()

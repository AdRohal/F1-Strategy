import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from utils.fetch_weather_data import fetch_current_weather
from utils.calculate_strategy import calculate_tire_strategy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
from io import BytesIO
import os
import time

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

def plot_tire_performance(ax, tire_type, weather_data):
    is_raining = any(weather['description'] in ['rain', 'light rain', 'heavy rain'] for weather in weather_data.get('weather', []))
    is_wet = weather_data.get('precipitation', 0) > 0.5

    if is_raining or is_wet:
        performance_data = {
            'Wet tires': {'slow': 5, 'fast': 10},
            'Intermediate tires': {'slow': 4, 'fast': 9},
            'Hard tires': {'slow': 7, 'fast': 12},
            'Medium tires': {'slow': 8, 'fast': 13},
            'Soft tires': {'slow': 9, 'fast': 14}
        }
    else:
        performance_data = {
            'Wet tires': {'slow': 10, 'fast': 15},
            'Intermediate tires': {'slow': 9, 'fast': 14},
            'Hard tires': {'slow': 3, 'fast': 8},
            'Medium tires': {'slow': 2, 'fast': 7},
            'Soft tires': {'slow': 1, 'fast': 6}
        }

    if tire_type in performance_data:
        data = performance_data[tire_type]
        ax.clear()
        ax.bar(['Slow', 'Fast'], [data['slow'], data['fast']], color=['tab:red', 'tab:green'])
        ax.set_xlabel('Performance')
        ax.set_ylabel('Time (s)')
        ax.set_title(f'{tire_type} Performance')

def fetch_radar_weather_map(lat, lon, api_key):
    # Convert lat and lon to float
    lat = float(lat)
    lon = float(lon)

    # Define the parameters for the radar map API call
    z = 10  # Zoom level
    x = int((lon + 180) / 360 * (2 ** z))  # X tile coordinate
    y = int((1 - (lat + 90) / 180) * (2 ** z))  # Y tile coordinate
    tm = int(time.time())  # Current Unix time

    url = f"https://maps.openweathermap.org/maps/2.0/radar/{z}/{x}/{y}?appid={api_key}&tm={tm}"
    response = requests.get(url)
    if response.status_code == 200:
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        return image
    else:
        print(f"Failed to fetch radar map with status code: {response.status_code}")
        return None

def plot_radar_weather(ax, radar_image):
    ax.clear()
    ax.imshow(radar_image, cmap='Blues', interpolation='nearest')
    ax.set_title('Radar Weather Data')

def display_radar_weather(lat, lon, api_key, radar_frame):
    radar_image = fetch_radar_weather_map(lat, lon, api_key)
    if radar_image:
        fig, ax = plt.subplots(figsize=(7.5, 4.5))
        plot_radar_weather(ax, radar_image)
        radar_canvas = FigureCanvasTkAgg(fig, master=radar_frame)
        radar_canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
        radar_canvas.draw()

def update_tire_image(strategy, image_label):
    script_dir = os.path.dirname(__file__)
    image_folder = os.path.join(script_dir, '..', 'img')
    image_files = {
        'Wet tires': 'blue.png',
        'Intermediate tires': 'green.png',
        'Hard tires': 'white.png',
        'Medium tires': 'yellow.png',
        'Soft tires': 'red.png'
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

def main():
    def on_submit():
        circuit = circuit_combobox.get().strip()
        tire_type = attack_combobox.get()
        weather_data = get_weather_data_for_location(circuit)

        if weather_data:
            print("Current weather data:", weather_data)

            try:
                temperature = weather_data['main']['temp']
                temperature_celsius = temperature

                current_weather = {
                    'temperature': temperature_celsius,
                    'humidity': weather_data['main']['humidity'],
                    'precipitation': weather_data.get('rain', {}).get('1h', 0),
                    'weather': weather_data.get('weather', [])
                }

                print("Current weather:", current_weather)

                print("Calculating tire strategy...")
                base_strategy = calculate_tire_strategy(current_weather)

                for widget in plot_frame.winfo_children():
                    widget.destroy()

                fig_size = (7.5, 4.5)

                fig_weather, weather_ax = plt.subplots(figsize=fig_size)
                plot_weather_data(weather_ax, temperature_celsius, current_weather['humidity'],
                                  current_weather['precipitation'])
                weather_canvas = FigureCanvasTkAgg(fig_weather, master=plot_frame)
                weather_canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
                weather_canvas.draw()

                fig_strategy, strategy_ax = plt.subplots(figsize=fig_size)
                plot_tire_strategy(strategy_ax, {
                    'Wet': 3 if current_weather['precipitation'] > 5.0 else 0,
                    'Intermediate': 2 if 0.5 < current_weather['precipitation'] <= 5.0 else 0,
                    'Hard': 2 if current_weather['temperature'] < 10 else 0,
                    'Medium': 2 if 10 <= current_weather['temperature'] < 20 else 0,
                    'Soft': 2 if current_weather['temperature'] >= 20 else 0
                })
                strategy_canvas = FigureCanvasTkAgg(fig_strategy, master=plot_frame)
                strategy_canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)
                strategy_canvas.draw()

                fig_performance, performance_ax = plt.subplots(figsize=fig_size)
                plot_tire_performance(performance_ax, tire_type, current_weather)
                performance_canvas = FigureCanvasTkAgg(fig_performance, master=plot_frame)
                performance_canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10)
                performance_canvas.draw()

                fig_radar, radar_ax = plt.subplots(figsize=fig_size)
                radar_data = weather_data.get('radar', [[0] * 10] * 10)
                plot_radar_weather(radar_ax, radar_data)
                radar_canvas = FigureCanvasTkAgg(fig_radar, master=plot_frame)
                radar_canvas.get_tk_widget().grid(row=1, column=1, padx=10, pady=10)
                radar_canvas.draw()

                strategy_label.config(text=f"Recommended: {tire_type}")
                update_tire_image(tire_type, image_label)

            except KeyError as e:
                print(f"Missing expected key in weather data: {e}")
                print("Weather data structure:", weather_data)
        else:
            print("Failed to fetch current weather data")

    def close_app():
        window.destroy()

    # The main window
    window = tk.Tk()
    window.title("F1 Strategy")
    window.attributes('-fullscreen', True)

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

    # Label and combobox for circuit input
    label = tk.Label(top_frame, text="Select the circuit:")
    label.pack(pady=10)

    circuit_combobox = ttk.Combobox(top_frame, values=cities, state='readonly')
    circuit_combobox.pack(pady=5)

    # Label and combobox for tire type
    attack_label = tk.Label(top_frame, text="Select Tire Type:")
    attack_label.pack(pady=5)
    tire_types = ['Wet tires', 'Intermediate tires', 'Hard tires', 'Medium tires', 'Soft tires']
    attack_combobox = ttk.Combobox(top_frame, values=tire_types, state='readonly')
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

    # Close button with red background and white text
    close_button = tk.Button(top_frame, text="Close", command=close_app, bg='red', fg='white')
    close_button.pack(pady=10)
    
    # Scrollable frame for plots
    canvas = tk.Canvas(window)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Frame for weather data plot, tire strategy plot, tire performance plot, and radar weather plot
    plot_frame = tk.Frame(scrollable_frame)
    plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

    window.mainloop()

if __name__ == "__main__":
    main()
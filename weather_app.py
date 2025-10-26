import requests
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import json
import os

class WeatherApp:
    def __init__(self):
        self.api_key = "2ebeb0774c2dc900f4739ab00bf3bcdc"  # You'll replace this with your actual key
        self.base_url = "http://api.openweathermap.org/data/2.5/"
        
    def get_weather(self, city_name):
        """Get current weather and forecast for a city"""
        try:
            print(f"\n🔍 Fetching weather data for {city_name}...")
            
            # Get current weather
            current_data = self._fetch_current_weather(city_name)
            if not current_data:
                return False
                
            # Get forecast
            forecast_data = self._fetch_forecast(city_name)
            if not forecast_data:
                return False
            
            # Display results
            self.display_weather(current_data, forecast_data)
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def _fetch_current_weather(self, city):
        """Fetch current weather data from API"""
        url = f"{self.base_url}weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'  # For Celsius
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    
    def _fetch_forecast(self, city):
        """Fetch 5-day forecast data from API"""
        url = f"{self.base_url}forecast"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def display_weather(self, current_data, forecast_data):
        """Display weather information in a formatted way"""
        
        # Clear console (works on both Windows and other systems)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + "="*60)
        print("🌤️  WEATHER FORECAST APPLICATION")
        print("="*60)
        
        # Extract and display current weather data
        city = current_data['name']
        country = current_data['sys']['country']
        temp = current_data['main']['temp']
        feels_like = current_data['main']['feels_like']
        humidity = current_data['main']['humidity']
        pressure = current_data['main']['pressure']
        wind_speed = current_data['wind']['speed']
        description = current_data['weather'][0]['description'].title()
        
        print(f"\n📍 CURRENT WEATHER IN {city.upper()}, {country}")
        print("-" * 40)
        print(f"🌡️  Temperature:    {temp:.1f}°C")
        print(f"🤔 Feels like:      {feels_like:.1f}°C")
        print(f"📝 Conditions:      {description}")
        print(f"💧 Humidity:        {humidity}%")
        print(f"📊 Pressure:        {pressure} hPa")
        print(f"💨 Wind Speed:      {wind_speed} m/s")
        
        # Display 5-day forecast
        self.display_forecast(forecast_data)
        
        # Create visualization
        self.create_visualizations(forecast_data, city)
        
        # Save data
        self.save_weather_data(current_data, forecast_data, city)
    
    def display_forecast(self, forecast_data):
        """Display 5-day weather forecast"""
        print(f"\n📅 5-DAY WEATHER FORECAST")
        print("-" * 50)
        
        # Group forecast data by day
        daily_forecasts = {}
        for item in forecast_data['list']:
            date = item['dt_txt'].split(' ')[0]  # Extract date part
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            daily_forecasts[date].append(item)
        
        # Display next 5 days
        dates = sorted(daily_forecasts.keys())[:5]
        
        for i, date in enumerate(dates):
            day_data = daily_forecasts[date]
            
            # Calculate statistics for the day
            temps = [item['main']['temp'] for item in day_data]
            avg_temp = sum(temps) / len(temps)
            min_temp = min(item['main']['temp_min'] for item in day_data)
            max_temp = max(item['main']['temp_max'] for item in day_data)
            description = day_data[len(day_data)//2]['weather'][0]['description'].title()  # Mid-day description
            
            # Format date
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            display_date = date_obj.strftime('%a, %b %d')
            
            # Weather icon based on conditions
            icon = self.get_weather_icon(description)
            
            print(f"{icon} {display_date}: {avg_temp:.1f}°C | "
                  f"H:{max_temp:.1f}°C L:{min_temp:.1f}°C | {description}")
    
    def get_weather_icon(self, description):
        """Return appropriate emoji for weather conditions"""
        description_lower = description.lower()
        if 'rain' in description_lower:
            return '🌧️'
        elif 'cloud' in description_lower:
            return '☁️'
        elif 'clear' in description_lower:
            return '☀️'
        elif 'snow' in description_lower:
            return '❄️'
        elif 'storm' in description_lower:
            return '⛈️'
        elif 'fog' in description_lower or 'mist' in description_lower:
            return '🌫️'
        else:
            return '🌈'
    
    def create_visualizations(self, forecast_data, city):
        """Create temperature and humidity charts"""
        print(f"\n📊 GENERATING WEATHER VISUALIZATIONS...")
        
        # Prepare data for charts
        timestamps = []
        temperatures = []
        humidities = []
        
        for item in forecast_data['list'][:8]:  # Next 24 hours (3-hour intervals)
            timestamp = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
            timestamps.append(timestamp.strftime('%H:%M'))
            temperatures.append(item['main']['temp'])
            humidities.append(item['main']['humidity'])
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Temperature chart
        ax1.plot(timestamps, temperatures, marker='o', linewidth=2, color='#e74c3c', label='Temperature')
        ax1.set_title(f'24-Hour Temperature Forecast - {city}', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Temperature (°C)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Humidity chart
        ax2.bar(timestamps, humidities, color='#3498db', alpha=0.7, label='Humidity')
        ax2.set_title('24-Hour Humidity Forecast', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Humidity (%)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(f'weather_forecast_{city}.png', dpi=300, bbox_inches='tight')
        print(f"✅ Chart saved as 'weather_forecast_{city}.png'")
        
        # Show plot (optional - comment out if running in headless environment)
        # plt.show()
    
    def save_weather_data(self, current_data, forecast_data, city):
        """Save weather data to JSON and CSV files"""
        print(f"\n💾 SAVING WEATHER DATA...")
        
        # Prepare data for saving
        weather_summary = {
            'city': city,
            'country': current_data['sys']['country'],
            'current_weather': {
                'temperature': current_data['main']['temp'],
                'feels_like': current_data['main']['feels_like'],
                'humidity': current_data['main']['humidity'],
                'pressure': current_data['main']['pressure'],
                'wind_speed': current_data['wind']['speed'],
                'description': current_data['weather'][0]['description'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'forecast': self._prepare_forecast_data(forecast_data)
        }
        
        # Save to JSON
        json_filename = f'weather_data_{city}.json'
        with open(json_filename, 'w') as f:
            json.dump(weather_summary, f, indent=2)
        print(f"✅ JSON data saved as '{json_filename}'")
        
        # Save to CSV
        self._save_forecast_csv(forecast_data, city)
    
    def _prepare_forecast_data(self, forecast_data):
        """Prepare forecast data for saving"""
        forecast_summary = []
        
        for item in forecast_data['list'][:10]:  # First 10 time periods
            forecast_summary.append({
                'datetime': item['dt_txt'],
                'temperature': item['main']['temp'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'description': item['weather'][0]['description']
            })
        
        return forecast_summary
    
    def _save_forecast_csv(self, forecast_data, city):
        """Save forecast data to CSV file using pandas"""
        data = []
        
        for item in forecast_data['list']:
            data.append({
                'datetime': item['dt_txt'],
                'temperature': item['main']['temp'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'wind_speed': item['wind']['speed'],
                'description': item['weather'][0]['description']
            })
        
        df = pd.DataFrame(data)
        csv_filename = f'forecast_data_{city}.csv'
        df.to_csv(csv_filename, index=False)
        print(f"✅ CSV data saved as '{csv_filename}'")

def main():
    app = WeatherApp()
    
    print("🌤️  WEATHER FORECAST APPLICATION")
    print("=" * 50)
    print("A Python Project for Your Developer Portfolio")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Get weather for a city")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1 or 2): ").strip()
        
        if choice == '1':
            city = input("Enter city name: ").strip()
            if city:
                success = app.get_weather(city)
                if not success:
                    print("❌ Could not fetch weather data. Please check:")
                    print("   - City name spelling")
                    print("   - Internet connection")
                    print("   - API key configuration")
            else:
                print("❌ Please enter a valid city name.")
        
        elif choice == '2':
            print("\nThank you for using the Weather Forecast App! 🌟")
            print("This project demonstrates Python skills for your resume!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
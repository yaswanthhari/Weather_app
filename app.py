import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import signal
import sys

def signal_handler(sig, frame):
    print('\n👋 Server stopped gracefully!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

from flask import Flask, render_template, request, jsonify
import requests
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import json
import os
import io
import base64

app = Flask(__name__)

class WeatherApp:
    def __init__(self):
        self.api_key = "2ebeb0774c2dc900f4739ab00bf3bcdc"  # Replace with your actual API key
        self.base_url = "http://api.openweathermap.org/data/2.5/"
    
    def get_weather_data(self, city_name):
        """Get current weather and forecast for a city"""
        try:
            current_data = self._fetch_current_weather(city_name)
            forecast_data = self._fetch_forecast(city_name)
            
            if current_data and forecast_data:
                chart_image = self.create_chart_image(forecast_data, city_name)
                return {
                    'success': True,
                    'current': self._process_current_data(current_data),
                    'forecast': self._process_forecast_data(forecast_data),
                    'chart': chart_image
                }
            return {'success': False, 'error': 'Could not fetch weather data'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _fetch_current_weather(self, city):
        url = f"{self.base_url}weather"
        params = {'q': city, 'appid': self.api_key, 'units': 'metric'}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def _fetch_forecast(self, city):
        url = f"{self.base_url}forecast"
        params = {'q': city, 'appid': self.api_key, 'units': 'metric'}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def _process_current_data(self, data):
        return {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'].title(),
            'icon': data['weather'][0]['icon']
        }
    
    def _process_forecast_data(self, data):
        daily_forecasts = {}
        for item in data['list']:
            date = item['dt_txt'].split(' ')[0]
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            daily_forecasts[date].append(item)
        
        forecast = []
        dates = sorted(daily_forecasts.keys())[:5]
        
        for date in dates:
            day_data = daily_forecasts[date]
            avg_temp = sum(item['main']['temp'] for item in day_data) / len(day_data)
            min_temp = min(item['main']['temp_min'] for item in day_data)
            max_temp = max(item['main']['temp_max'] for item in day_data)
            description = day_data[len(day_data)//2]['weather'][0]['description'].title()
            
            forecast.append({
                'date': datetime.strptime(date, '%Y-%m-%d').strftime('%a, %b %d'),
                'avg_temp': avg_temp,
                'min_temp': min_temp,
                'max_temp': max_temp,
                'description': description,
                'icon': self.get_weather_icon(description)
            })
        
        return forecast
    
    def get_weather_icon(self, description):
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
    
    def create_chart_image(self, forecast_data, city):
        """Create chart and return as base64 image"""
        timestamps = []
        temperatures = []
        humidities = []
        
        for item in forecast_data['list'][:8]:
            timestamp = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
            timestamps.append(timestamp.strftime('%H:%M'))
            temperatures.append(item['main']['temp'])
            humidities.append(item['main']['humidity'])
        
        # Create figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        
        # Temperature plot
        ax1.plot(timestamps, temperatures, marker='o', linewidth=2, color='#e74c3c')
        ax1.set_title(f'24-Hour Temperature Forecast - {city}', fontweight='bold')
        ax1.set_ylabel('Temperature (°C)')
        ax1.grid(True, alpha=0.3)
        
        # Humidity plot
        ax2.bar(timestamps, humidities, color='#3498db', alpha=0.7)
        ax2.set_title('24-Hour Humidity Forecast', fontweight='bold')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Humidity (%)')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Convert plot to base64 string
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{plot_url}"

# Initialize weather app
weather_app = WeatherApp()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.json.get('city')
    if not city:
        return jsonify({'success': False, 'error': 'City name is required'})
    
    result = weather_app.get_weather_data(city)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
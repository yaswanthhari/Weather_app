@"
# Weather Forecast App 🌤️

A full-stack web application built with Python Flask that provides real-time weather information and 5-day forecasts.

## Features

- 🌡️ Real-time weather data from OpenWeatherMap API
- 📅 5-day weather forecast
- 📊 Interactive temperature and humidity charts
- 🎨 Responsive web design
- 🔍 Search any city worldwide

## Technologies Used

- **Backend**: Python, Flask, REST APIs
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Visualization**: Matplotlib
- **API Integration**: OpenWeatherMap
- **Data Processing**: Pandas

## Installation

1. Clone this repository:
\`\`\`bash
git clone https://github.com/yourusername/weatherapp.git
cd weatherapp
\`\`\`

2. Create virtual environment and install dependencies:
\`\`\`bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
\`\`\`

3. Get your free API key from [OpenWeatherMap](https://openweathermap.org/api)

4. Add your API key to \`app.py\`:
\`\`\`python
self.api_key = 'your_api_key_here'
\`\`\`

5. Run the application:
\`\`\`bash
python app.py
\`\`\`

6. Open http://127.0.0.1:5000 in your browser

## Project Structure

\`\`\`
weatherapp/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Frontend template
├── README.md          # Project documentation
└── .gitignore         # Git ignore rules
\`\`\`

## Demo

![Weather App Screenshot](https://via.placeholder.com/800x400/74b9ff/ffffff?text=Weather+Forecast+App)

## License

MIT License
"@ | Out-File README.md -Encoding utf8
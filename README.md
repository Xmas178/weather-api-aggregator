# Weather API Aggregator

A comprehensive weather data aggregator that fetches real-time weather information from multiple sources and provides historical analysis, trends, and visualizations.

## Features

- **Multi-source data aggregation**: Combines data from FMI (Finnish Meteorological Institute) and Yr.no (Norwegian Meteorological Institute)
- **Worldwide coverage**: Works for any city globally using automatic geocoding
- **Historical data storage**: SQLite database for storing weather observations
- **Analytics & trends**: Temperature trends, statistical analysis, source comparison
- **Data visualization**: Charts and graphs for weather patterns
- **REST API**: Clean, documented API endpoints
- **React frontend**: Modern dashboard with Material-UI

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLite** - Database for historical data
- **Pandas** - Data analysis and statistics
- **httpx** - Async HTTP requests
- **geopy** - Automatic city-to-coordinates geocoding

### Frontend
- **React** (Vite)
- **Material-UI (MUI)** - Component library
- **Recharts** - Data visualization
- **Axios** - API requests

## Project Structure
```
weather-api/
├── main.py                 # FastAPI application
├── database.py             # SQLite database operations
├── analytics.py            # Pandas-based data analysis
├── services/
│   ├── fmi.py             # FMI API integration
│   └── yr.py              # Yr.no API integration
├── weather_data.db         # SQLite database (auto-created)
└── requirements.txt

weather-frontend/
├── src/
│   ├── App.jsx            # Main dashboard
│   ├── components/
│   │   ├── WeatherStats.jsx
│   │   └── SourceComparison.jsx
│   └── services/
│       └── api.js         # API client
└── package.json
```

## Installation

### Backend Setup

1. **Clone the repository**
```bash
# 1. Kloonaa repositorio
git clone https://github.com/Xmas178/weather-api-aggregator.git
cd weather-api-aggregator
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the backend**
```bash
uvicorn main:app --reload
```

Backend runs on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd weather-frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Run the development server**
```bash
npm run dev
```

Frontend runs on `http://localhost:5173`

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoints

#### Get Current Weather
```
GET /weather?city={city_name}
```
Example: `http://localhost:8000/weather?city=Helsinki`

Returns current weather data from available sources.

#### Get Historical Data
```
GET /weather/history/{city}?hours=24
```
Returns past weather observations.

#### Get Statistics
```
GET /weather/stats/{city}?hours=24
```
Returns min, max, and average temperatures.

#### Get Temperature Trend
```
GET /weather/trend/{city}?hours=24
```
Analyzes if temperature is warming, cooling, or stable.

#### Compare Data Sources
```
GET /weather/compare/{city}?hours=24
```
Compares accuracy between FMI and Yr.no.

#### Get Hourly Data
```
GET /weather/hourly/{city}?hours=24
```
Returns hourly temperature averages for charts.

## Data Sources

### FMI (Finnish Meteorological Institute)
- **Coverage**: Finland only
- **Data**: Temperature, humidity, wind speed, precipitation
- **API**: Open data, WFS format
- **Note**: Some stations may not provide all parameters (e.g., pressure)

### Yr.no (Norwegian Meteorological Institute)
- **Coverage**: Worldwide
- **Data**: Temperature, humidity, pressure, wind speed
- **API**: Free, requires User-Agent header
- **Geocoding**: Automatic city-to-coordinates conversion using geopy

## How It Works

1. **User searches for a city** (e.g., "London")
2. **Backend fetches data** from both FMI and Yr.no
3. **Data is combined**: FMI data preferred for Finnish cities, missing fields filled from Yr.no
4. **Saved to database**: All observations stored for historical analysis
5. **Analytics computed**: Trends, statistics, and comparisons calculated with Pandas
6. **Frontend displays**: Dashboard shows current weather, charts, and analytics

## Database Schema

### weather_data table
- `id` - Primary key
- `city` - City name
- `source` - Data source (FMI or Yr)
- `temperature` - Temperature in Celsius
- `humidity` - Relative humidity (%)
- `pressure` - Air pressure (hPa)
- `wind_speed` - Wind speed (m/s)
- `precipitation` - Precipitation (mm)
- `weather_description` - Weather condition
- `timestamp` - Observation time

## Future Improvements

- [ ] **City validation**: Verify city exists before geocoding to prevent invalid location results
- [ ] **Weather forecast**: Add 5-7 day forecast data
- [ ] **More data sources**: Add OpenWeatherMap, WeatherAPI
- [ ] **User favorites**: Save favorite cities
- [ ] **Weather alerts**: Push notifications for severe weather
- [ ] **Map view**: Interactive map with weather overlay
- [ ] **Export data**: Download historical data as CSV
- [ ] **Docker deployment**: Containerize for easy deployment
- [ ] **PostgreSQL**: Migrate from SQLite for production

## Known Limitations

- **FMI coverage**: Only works for Finnish cities
- **Geocoding accuracy**: May return results for misspelled or invalid city names
- **Rate limits**: Yr.no has rate limits for API requests
- **Pressure data**: FMI doesn't provide pressure for all stations

## Development

### Adding a new weather source

1. Create new service file in `services/` (e.g., `openweather.py`)
2. Implement `get_current_weather(city)` method
3. Add to `main.py` `/weather` endpoint
4. Update database saving logic

### Running tests
```bash
# Backend tests (when implemented)
pytest

# Frontend tests
npm test
```

## Contributing

This is a portfolio project. Suggestions and feedback welcome!

## License

MIT License - Free to use for learning and portfolio purposes.

## Author

**Xmas178**
- GitHub: [@Xmas178](https://github.com/Xmas178)

## Acknowledgments

- **FMI** - Finnish Meteorological Institute for open weather data
- **Yr.no** - Norwegian Meteorological Institute for global weather API
- **FastAPI** - Amazing Python web framework
- **Material-UI** - Beautiful React components

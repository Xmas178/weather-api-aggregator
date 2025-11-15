"""
Weather API - FastAPI Backend

Aggregates weather data from multiple sources:
- FMI (Finnish Meteorological Institute) - Finland only
- Yr.no (Norwegian Meteorological Institute) - Worldwide

Stores historical data for analysis and trends.
"""

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Weather API",
    description="Multi-source weather data aggregator with analytics",
    version="1.0.0",
)

# CORS middleware - allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/weather")
async def get_weather(city: str):
    """
    Get current weather for a city from multiple sources.

    - Finnish cities: Returns FMI data (most accurate for Finland)
    - Other cities: Returns Yr.no data (worldwide coverage)
    - Saves all observations to database for historical analysis

    Args:
        city: City name (e.g., "Helsinki", "London", "Tokyo")

    Returns:
        Weather data with temperature, humidity, wind, pressure, etc.
    """
    from services.fmi import fmi_service
    from services.yr import yr_service
    from database import weather_db

    sources = {}

    # Fetch from FMI (Finnish Meteorological Institute)
    # Only works for Finnish cities
    try:
        fmi_data = await fmi_service.get_current_weather(place=city)
        if fmi_data:
            sources["FMI"] = fmi_data
            weather_db.save_observation(city, "FMI", fmi_data)
    except Exception as e:
        print(f"FMI error: {e}")

    # Fetch from Yr.no (Norwegian Meteorological Institute)
    # Works worldwide with automatic geocoding
    try:
        yr_data = await yr_service.get_current_weather(city)
        if yr_data:
            sources["Yr"] = yr_data
            weather_db.save_observation(city, "Yr", yr_data)
    except Exception as e:
        print(f"Yr error: {e}")

    # Combine data from both sources if available
    # Use FMI pressure if available, otherwise Yr.no pressure
    if sources:
        if "FMI" in sources and "Yr" in sources:
            # Combine: Use FMI as base, fill missing data from Yr.no
            combined_data = sources["FMI"].copy()
            if combined_data.get("pressure") is None:
                combined_data["pressure"] = sources["Yr"].get("pressure")
            if combined_data.get("wind_speed") is None:
                combined_data["wind_speed"] = sources["Yr"].get("wind_speed")

            return {"city": city, "source": "FMI + Yr.no", "data": combined_data}
        else:
            # Single source available
            primary_source = "FMI" if "FMI" in sources else "Yr"
            return {
                "city": city,
                "source": primary_source,
                "data": sources[primary_source],
            }
    else:
        return {"error": f"No weather data found for '{city}'"}


@app.get("/weather/history/{city}")
async def get_weather_history(city: str, hours: int = 24):
    """
    Get historical weather data for a city.

    Args:
        city: City name
        hours: Number of hours of history (default: 24)

    Returns:
        List of past weather observations
    """
    from database import weather_db

    history = weather_db.get_history(city, hours)

    return {
        "city": city,
        "hours": hours,
        "observation_count": len(history),
        "data": history,
    }


@app.get("/weather/stats/{city}")
async def get_weather_stats(city: str, hours: int = 24):
    """
    Get weather statistics for a city.

    Calculates min, max, and average temperatures.

    Args:
        city: City name
        hours: Time period for statistics (default: 24)

    Returns:
        Statistical summary of weather data
    """
    from database import weather_db

    stats = weather_db.get_statistics(city, hours)

    return {"city": city, "period_hours": hours, "statistics": stats}


@app.get("/weather/trend/{city}")
async def get_temperature_trend(city: str, hours: int = 24):
    """
    Analyze temperature trend (warming/cooling/stable).

    Args:
        city: City name
        hours: Time period for analysis (default: 24)

    Returns:
        Trend analysis with temperature change
    """
    from analytics import analytics

    trend = analytics.get_temperature_trend(city, hours)

    return {"city": city, "period_hours": hours, "trend_analysis": trend}


@app.get("/weather/compare/{city}")
async def compare_sources(city: str, hours: int = 24):
    """
    Compare data accuracy between different weather sources.

    Shows average, min, max temperatures from each source.

    Args:
        city: City name
        hours: Time period for comparison (default: 24)

    Returns:
        Comparison table of all data sources
    """
    from analytics import analytics

    comparison = analytics.compare_sources(city, hours)

    return {"city": city, "period_hours": hours, "source_comparison": comparison}


@app.get("/weather/hourly/{city}")
async def get_hourly_data(city: str, hours: int = 24):
    """
    Get hourly temperature averages for charts.

    Args:
        city: City name
        hours: Time period (default: 24)

    Returns:
        Hourly data points for visualization
    """
    from analytics import analytics

    hourly = analytics.get_hourly_averages(city, hours)

    return {"city": city, "period_hours": hours, "hourly_data": hourly}


# Serve frontend static files
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

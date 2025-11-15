"""
Yr.no (Norwegian Meteorological Institute) API integration.

Yr.no is free but requires User-Agent header.
Uses geopy for automatic city-to-coordinates conversion.
"""

import httpx
from typing import Optional, Dict, Any
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


class YrService:
    """
    Yr.no API service with automatic geocoding.

    Converts any city name to coordinates automatically.
    """

    def __init__(self):
        self.base_url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
        self.headers = {
            "User-Agent": "WeatherAPIAggregator/1.0 (github.com/Xmas178/weather-api-aggregator)"
        }
        # Initialize geocoder
        self.geolocator = Nominatim(user_agent="weather-api-aggregator")
        # Cache for coordinates to avoid repeated geocoding
        self.coords_cache = {}

    def get_coordinates(self, city: str) -> Optional[Dict[str, float]]:
        """
        Get coordinates for any city using geocoding.

        Args:
            city: City name (e.g., "Oulu", "Paris", "New York")

        Returns:
            Dictionary with lat/lon or None if not found
        """
        # Check cache first
        if city in self.coords_cache:
            return self.coords_cache[city]

        try:
            location = self.geolocator.geocode(city, timeout=10)
            if location:
                coords = {
                    "lat": round(location.latitude, 2),
                    "lon": round(location.longitude, 2),
                }
                # Cache the result
                self.coords_cache[city] = coords
                return coords
            else:
                print(f"⚠️ Geocoding: City '{city}' not found")
                return None

        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"❌ Geocoding error for '{city}': {e}")
            return None

    async def get_current_weather(self, city: str = "Oulu") -> Optional[Dict[str, Any]]:
        """
        Get current weather from Yr.no for any city.

        Args:
            city: City name (works for any city worldwide!)

        Returns:
            Dictionary with weather data or None if fetch fails
        """
        # Get coordinates for the city
        coords = self.get_coordinates(city)
        if not coords:
            return None

        try:
            params = {"lat": coords["lat"], "lon": coords["lon"]}

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    self.base_url, params=params, headers=self.headers
                )
                response.raise_for_status()
                data = response.json()

                return self._parse_current_weather(data)

        except Exception as e:
            print(f"❌ Yr.no weather fetch failed: {e}")
            return None

    def _parse_current_weather(self, data: dict) -> Dict[str, Any]:
        """
        Convert Yr.no data to unified format.
        """
        timeseries = data.get("properties", {}).get("timeseries", [])

        if not timeseries:
            return {}

        current = timeseries[0].get("data", {}).get("instant", {}).get("details", {})

        return {
            "temperature": current.get("air_temperature", 0),
            "weather": "Unknown",
            "wind_speed": current.get("wind_speed", 0),
            "humidity": current.get("relative_humidity"),
            "pressure": current.get("air_pressure_at_sea_level"),
            "precipitation": None,
        }


# Single instance
yr_service = YrService()

"""
Yr.no (Norjan meteorologinen instituutti) API integraatio.

Yr.no on ilmainen, mutta vaatii User-Agent headerin.
"""

import httpx
from typing import Optional, Dict, Any


class YrService:
    """
    Yr.no API -palvelu.
    
    Käyttää LocationForecast API:a.
    """
    
    def __init__(self):
        self.base_url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
        self.oulu_lat = 65.01
        self.oulu_lon = 25.47
        # Yr.no vaatii User-Agent headerin
        self.headers = {
            "User-Agent": "WeatherAPIAggregator/1.0 (github.com/Xmas178/weather-api-aggregator)"
        }
    
    async def get_current_weather(self) -> Optional[Dict[str, Any]]:
        """
        Hakee nykyisen sään Ouluun Yr.no:lta.
        
        Returns:
            Dictionary säätiedoilla tai None jos haku epäonnistuu
        """
        try:
            params = {
                "lat": self.oulu_lat,
                "lon": self.oulu_lon
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    self.base_url,
                    params=params,
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()
                
                # Parsitaan data
                return self._parse_current_weather(data)
                
        except Exception as e:
            print(f"❌ Yr.no säätietojen haku epäonnistui: {e}")
            return None
    
    def _parse_current_weather(self, data: dict) -> Dict[str, Any]:
        """
        Muuntaa Yr.no:n datan yhtenäiseen muotoon.
        """
        # Yr.no palauttaa timeseries-listan, otetaan ensimmäinen (nykyhetki)
        timeseries = data.get("properties", {}).get("timeseries", [])
        
        if not timeseries:
            return {}
        
        current = timeseries[0].get("data", {}).get("instant", {}).get("details", {})
        
        return {
            "temperature": current.get("air_temperature", 0),
            "weather": "Unknown",  # Yr.no ei anna yksinkertaista kuvausta
            "wind_speed": current.get("wind_speed", 0),
            "humidity": current.get("relative_humidity"),
            "pressure": current.get("air_pressure_at_sea_level"),
            "precipitation": None  # Ei saatavilla instant-datassa
        }


# Yksittäinen instanssi
yr_service = YrService()
"""
FMI (Ilmatieteen laitos) API integraatio.

FMI käyttää XML-muotoa ja WFS-standardia.
"""

import httpx
import xmltodict
from typing import Optional, Dict, Any


class FMIService:
    """
    FMI API -palvelu.
    
    Hakee säätiedot Ilmatieteen laitoksen avoimesta datasta.
    """
    
    def __init__(self):
        self.base_url = "https://opendata.fmi.fi/wfs"
        self.oulu_lat = 65.01
        self.oulu_lon = 25.47
    
    async def get_current_weather(self) -> Optional[Dict[str, Any]]:
        """
        Hakee nykyisen sään Ouluun FMI:ltä.
        
        Returns:
            Dictionary säätiedoilla tai None jos haku epäonnistuu
        """
        try:
            params = {
                "service": "WFS",
                "version": "2.0.0",
                "request": "getFeature",
                "storedquery_id": "fmi::observations::weather::simple",
                "place": "Oulu"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                
                # Muunna XML -> Dictionary
                data = xmltodict.parse(response.text)
                
                # Parsitaan uusin data
                return self._parse_latest_weather(data)
                
        except Exception as e:
            print(f"❌ FMI säätietojen haku epäonnistui: {e}")
            return None
    
    def _parse_latest_weather(self, xml_data: dict) -> Dict[str, Any]:
        """
        Poimii uusimman säädatan FMI:n XML-vastauksesta.
        
        FMI palauttaa historiallista dataa, joten otetaan viimeisin.
        """
        members = xml_data.get("wfs:FeatureCollection", {}).get("wfs:member", [])
        
        if not members:
            return {}
        
        # Kerätään kaikki parametrit
        latest_data = {}
        
        # FMI palauttaa jokaisen parametrin erikseen
        # Käydään läpi ja poimitaan viimeisimmät arvot
        for member in members:
            element = member.get("BsWfs:BsWfsElement", {})
            param_name = element.get("BsWfs:ParameterName")
            param_value = element.get("BsWfs:ParameterValue")
            
            # Ohitetaan NaN-arvot
            if param_value and param_value != "NaN":
                latest_data[param_name] = param_value
        
        # Muunnetaan FMI:n parametrit yhtenäiseen muotoon
        return {
            "temperature": float(latest_data.get("t2m", 0)),
            "weather": "Unknown",  # FMI ei anna suoraa säätilan kuvausta
            "wind_speed": float(latest_data.get("ws_10min", 0)) if latest_data.get("ws_10min") else None,
            "humidity": int(float(latest_data.get("rh", 0))) if latest_data.get("rh") else None,
            "pressure": float(latest_data.get("p_sea", 0)) if latest_data.get("p_sea") else None,
            "precipitation": float(latest_data.get("ri_10min", 0)) if latest_data.get("ri_10min") else None
        }


# Yksittäinen instanssi
fmi_service = FMIService()
"""
Foreca Weather API integraatio.

Tämä moduuli hoitaa:
1. Autentikoinnin (token-haku)
2. Säätietojen hakemisen
"""

import httpx
import os
from typing import Optional, Dict, Any


class ForecaService:
    """
    Foreca API -palvelu.
    """
    
    def __init__(self):
        self.base_url = "https://pfa.foreca.com"
        self.user = os.getenv("FORECA_USER")
        self.password = os.getenv("FORECA_PASSWORD")
        self.oulu_location_id = "100643492"
    
    async def get_token(self) -> Optional[str]:
        """
        Hakee access token Foreca API:sta.
        
        Returns:
            Token string tai None jos epäonnistuu
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/authorize/token?expire_hours=2",
                    json={"user": self.user, "password": self.password}
                )
                response.raise_for_status()
                data = response.json()
                return data.get("access_token")
        except Exception as e:
            print(f"❌ Foreca autentikointi epäonnistui: {e}")
            return None
    
    async def get_current_weather(self) -> Optional[Dict[str, Any]]:
        """
        Hakee nykyisen sään Ouluun.
        
        Returns:
            Dictionary säätiedoilla tai None jos haku epäonnistuu
        """
        token = await self.get_token()
        if not token:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {token}"}
                response = await client.get(
                    f"{self.base_url}/api/v1/current/{self.oulu_location_id}",
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()
                
                current = data.get("current", {})
                return {
                    "temperature": current.get("temperature"),
                    "weather": current.get("symbolPhrase"),
                    "wind_speed": current.get("windSpeed"),
                    "humidity": current.get("relHumidity"),
                    "pressure": current.get("pressure"),
                    "precipitation": current.get("precipRate")
                }
        except Exception as e:
            print(f"❌ Foreca säätietojen haku epäonnistui: {e}")
            return None


# Yksittäinen instanssi
foreca_service = ForecaService()
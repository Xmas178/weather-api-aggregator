from fastapi import FastAPI
from dotenv import load_dotenv
import os
import httpx

# Ladataan .env tiedosto
load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Weather API"}

@app.get("/test-foreca")
async def test_foreca():
    """Testataan API yhteyttä"""
    user = os.getenv("FORECA_USER")
    password = os.getenv("FORECA_PASSWORD")
    
    # Haetaan token
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://pfa.foreca.com/authorize/token?expire_hours=2",
            json={"user": user, "password": password}
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            return {
                "status": "success",
                "token_received": True,
                "token_length": len(token)
            }
        else:
            return {
                "status": "error",
                "status_code": response.status_code
            }

@app.get("/find-oulu")
async def find_oulu():
    """Etsitään Oulun ID"""
    user = os.getenv("FORECA_USER")
    password = os.getenv("FORECA_PASSWORD")
    
    # 1. Haetaan token
    async with httpx.AsyncClient() as client:
        auth_response = await client.post(
            "https://pfa.foreca.com/authorize/token?expire_hours=2",
            json={"user": user, "password": password}
        )
        
        if auth_response.status_code != 200:
            return {"error": "Authentication failed"}
        
        token = auth_response.json().get("access_token")
        
        # 2. Haetaan Oulu
        headers = {"Authorization": f"Bearer {token}"}
        search_response = await client.get(
            "https://pfa.foreca.com/api/v1/location/search/Oulu",
            headers=headers
        )
        
        if search_response.status_code == 200:
            data = search_response.json()
            return {
                "status": "success",
                "locations": data
            }
        else:
            return {
                "status": "error",
                "status_code": search_response.status_code
            }
        
@app.get("/weather/oulu")
async def get_oulu_weather():
    """Haetaan Oulun sää kaikista lähteistä"""
    from services.fmi import fmi_service
    from services.yr import yr_service
    
    sources = {}
    
    # 1. Foreca
    
    try:
        from services.foreca import foreca_service
        foreca_weather = await foreca_service.get_current_weather()
        if foreca_weather:
            sources["foreca"] = foreca_weather
            print("✅ Foreca data haettu")
    except Exception as e:
        print(f"❌ Foreca virhe: {e}")
    
    # 2. FMI
    try:
        fmi_weather = await fmi_service.get_current_weather()
        if fmi_weather:
            sources["fmi"] = fmi_weather
            print("✅ FMI data haettu")
    except Exception as e:
        print(f"❌ FMI virhe: {e}")
    
    # 3. Yr.no
    try:
        yr_weather = await yr_service.get_current_weather()
        if yr_weather:
            sources["yr"] = yr_weather
            print("✅ Yr.no data haettu")
    except Exception as e:
        print(f"❌ Yr.no virhe: {e}")
    
    # Palautetaan kaikki lähteet
    return {
        "location": "Oulu",
        "latitude": 65.01,
        "longitude": 25.47,
        "sources": sources,
        "timestamp": "2025-11-04T15:30:00Z"
    }
        
@app.get("/test-fmi")
async def test_fmi():
    """Testataan FMI API yhteyttä"""
    from services.fmi import fmi_service
    
    weather = await fmi_service.get_current_weather()
    
    if weather:
        return {
            "status": "success",
            "source": "FMI",
            "data": weather
        }
    else:
        return {
            "status": "error",
            "message": "FMI data ei saatavilla"
        }

@app.get("/test-yr")
async def test_yr():
    """Testataan Yr.no API yhteyttä"""
    from services.yr import yr_service
    
    weather = await yr_service.get_current_weather()
    
    if weather:
        return {
            "status": "success",
            "source": "Yr.no",
            "data": weather
        }
    else:
        return {
            "status": "error",
            "message": "Yr.no data ei saatavilla"
        }
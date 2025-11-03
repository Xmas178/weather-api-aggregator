from fastapi import FastAPI
from dotenv import load_dotenv
import os
import httpx

# Ladataan .env tiedosto
load_dotenv()

app = FastAPI()

async def get_foreca_token():
    """Apufunktio: Hakee Foreca API tokenin"""
    user = os.getenv("FORECA_USER")
    password = os.getenv("FORECA_PASSWORD")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://pfa.foreca.com/authorize/token?expire_hours=2",
            json={"user": user, "password": password}
        )
        
        if response.status_code == 200:
            return response.json().get("access_token")
        return None

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
    """Haetaan Oulun nykyinen sää"""
    oulu_id = "100643492"
    
    # 1. Haetaan token apufunktiolla
    token = await get_foreca_token()
    if not token:
        return {"error": "Authentication failed"}
    
    # 2. Haetaan sää
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(
            f"https://pfa.foreca.com/api/v1/current/{oulu_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": "error",
                "status_code": response.status_code
            }
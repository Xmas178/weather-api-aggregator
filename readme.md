# Weather API Aggregator

Yksinkertainen backend-palvelu joka kerää säätiedot kolmesta eri lähteestä ja tarjoaa ne yhtenäisessä muodossa.

## Ominaisuudet

- Nykyinen sää Ouluun kolmesta eri lähteestä
- Useat datalähteet: Foreca, FMI (Ilmatieteen laitos), Yr.no
- Nopea FastAPI-pohjainen REST API
- Yhtenäinen JSON-muoto kaikille lähteille
- Asynkroninen - kaikki lähteet haetaan samanaikaisesti

## Teknologiat

- **Backend**: Python 3.9+
- **Framework**: FastAPI
- **HTTP Client**: httpx (async)
- **XML Parser**: xmltodict (FMI)
- **Data sources**: 
  - Foreca Weather API
  - FMI Open Data
  - Yr.no (MET Norway)

## Asennus

### 1. Kloonaa repositorio
```bash
git clone https://github.com/Xmas178/weather-api-aggregator.git
cd weather-api-aggregator
```

### 2. Luo virtuaaliympäristö
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# tai Windows: venv\Scripts\activate
```

### 3. Asenna riippuvuudet
```bash
pip install fastapi uvicorn httpx python-dotenv xmltodict
```

### 4. Konfiguroi ympäristömuuttujat
Luo `.env` tiedosto projektin juureen:
```
FORECA_USER=your_username
FORECA_PASSWORD=your_password
FORECA_ADMIN_PASSWORD=your_admin_password
```

### 5. Käynnistä palvelin
```bash
uvicorn main:app --reload
```

Palvelin käynnistyy osoitteessa: http://localhost:8000

## API Dokumentaatio

### Interaktiivinen dokumentaatio
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpointit

#### `GET /`
Tervetuloviesti ja API:n perustiedot.

**Vastaus:**
```json
{
  "message": "Weather API"
}
```

#### `GET /weather/oulu`
Palauttaa nykyisen sään Oulusta kaikista kolmesta lähteestä.

**Vastaus:**
```json
{
  "location": "Oulu",
  "latitude": 65.01,
  "longitude": 25.47,
  "sources": {
    "foreca": {
      "temperature": 7.0,
      "weather": "overcast",
      "wind_speed": 6,
      "humidity": 77,
      "pressure": 1002.73,
      "precipitation": 0.01
    },
    "fmi": {
      "temperature": 7.2,
      "weather": "Unknown",
      "wind_speed": null,
      "humidity": 78,
      "pressure": null,
      "precipitation": 0.0
    },
    "yr": {
      "temperature": 7.4,
      "weather": "Unknown",
      "wind_speed": 6.2,
      "humidity": 82.9,
      "pressure": 1002.8,
      "precipitation": null
    }
  },
  "timestamp": "2025-11-04T15:30:00Z"
}
```

#### `GET /test-foreca`
Testaa Foreca API:n yhteyttä.

#### `GET /test-fmi`
Testaa FMI API:n yhteyttä.

#### `GET /test-yr`
Testaa Yr.no API:n yhteyttä.

## Projektin rakenne
```
weather-api-aggregator/
├── main.py                 # FastAPI sovellus ja endpointit
├── services/
│   ├── foreca.py          # Foreca API integraatio
│   ├── fmi.py             # FMI API integraatio
│   └── yr.py              # Yr.no API integraatio
├── .env                   # API-avaimet (EI versionhallinnassa!)
├── .gitignore             # Git-ignore säännöt
├── venv/                  # Virtuaaliympäristö
└── README.md              # Tämä tiedosto
```

## Käyttöesimerkkejä

### Python
```python
import httpx
import asyncio

async def get_weather():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/weather/oulu")
        data = response.json()
        
        # Tulosta kaikkien lähteiden lämpötilat
        for source, weather in data["sources"].items():
            print(f"{source}: {weather['temperature']}°C")

asyncio.run(get_weather())
```

### cURL
```bash
curl http://localhost:8000/weather/oulu
```

### JavaScript/Fetch
```javascript
fetch('http://localhost:8000/weather/oulu')
  .then(response => response.json())
  .then(data => {
    console.log('Foreca:', data.sources.foreca.temperature + '°C');
    console.log('FMI:', data.sources.fmi.temperature + '°C');
    console.log('Yr.no:', data.sources.yr.temperature + '°C');
  });
```

## Tulevaisuuden kehitysideat

- Tietokannan lisäys (historiallinen data)
- Useiden kaupunkien tuki
- Ennusteen haku (1-7 päivää)
- Caching (Redis)
- Rate limiting
- Testit (pytest)
- Docker-konttitus
- Deploy pilvipalveluun (Railway/Render)

## Lisenssit

- **Projekti**: MIT License
- **Foreca**: Kaupallinen API (ilmainen trial)
- **FMI**: Avoin data (CC BY 4.0)
- **Yr.no**: Ilmainen (vaatii User-Agent)

## Tekijä

**(Xmas178)**
- GitHub: [@Xmas178](https://github.com/Xmas178)
- Email: xmas178@gmail.com

---

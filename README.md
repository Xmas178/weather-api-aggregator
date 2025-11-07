# Weather API Aggregator

Sääpalvelu joka yhdistää useita pohjoismaisia säädatalähteitä yhteen API:in. Sisältää sekä backendin (FastAPI) että yksinkertaisen web-käyttöliittymän.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Ominaisuudet

- **Useita datalähteitä**: FMI (Ilmatieteen laitos), Foreca, Yr.no (MET Norway)
- **Nopea asynkroninen haku**: httpx-kirjastolla
- **Web-käyttöliittymä**: Yksinkertainen frontend ilman Reactia
- **Yhtenäinen data**: Kaikki lähteet samassa muodossa
- **Reaaliaikainen**: Hakee tuoreimmat tiedot

## Pika-aloitus

### Vaatimukset

- Python 3.9 tai uudempi
- pip
- Foreca API-tunnukset (ilmainen trial: [developer.foreca.com](https://developer.foreca.com))

### Asennus
```bash
# 1. Kloonaa repositorio
git clone https://github.com/Xmas178/weather-api-aggregator.git
cd weather-api-aggregator

# 2. Luo virtuaaliympäristö
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# tai Windows: venv\Scripts\activate

# 3. Asenna riippuvuudet
pip install -r requirements.txt

# 4. Konfiguroi Foreca API-tunnukset
# Luo .env tiedosto projektin juureen:
```

**.env tiedosto:**
```env
FORECA_USER=your_username
FORECA_PASSWORD=your_password
FORECA_ADMIN_PASSWORD=your_admin_password
```

### Käynnistys
```bash
uvicorn main:app --reload
```

Palvelu käynnistyy osoitteessa: **http://localhost:8000**

## Käyttöliittymä

Avaa selaimessa: **http://localhost:8000**

Frontend tarjoaa:
- Kaupunkihaku
- Reaaliaikainen säätila
- Lämpötila, kosteus, ilmanpaine
- Tuulen nopeus ja sademäärä

## API Endpointit

### Hae sää kaupungille
```http
GET /weather?city={kaupunki}
```

**Esimerkki:**
```bash
curl http://localhost:8000/weather?city=Oulu
```

**Vastaus:**
```json
{
  "city": "Oulu",
  "sources": {
    "foreca": {
      "temperature": 7.3,
      "humidity": 96,
      "pressure": 1012.6,
      "wind_speed": 3.7,
      "precipitation": null,
      "weather": "pilvistä"
    },
    "fmi": {
      "temperature": 7.1,
      "humidity": 95,
      "pressure": 1012.8,
      "wind_speed": 4.0,
      "precipitation": 0,
      "weather": "pilvistä"
    },
    "yr": {
      "temperature": 7.5,
      "humidity": 94,
      "pressure": 1012.5,
      "wind_speed": 3.5,
      "precipitation": null,
      "weather": "pilvistä"
    }
  },
  "timestamp": "2024-11-07T15:30:00Z"
}
```

### API Dokumentaatio

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Projektirakenne
```
weather-api-aggregator/
├── main.py                 # FastAPI sovellus
├── services/               # API-integraatiot
│   ├── foreca.py          # Foreca API
│   ├── fmi.py             # FMI API
│   └── yr.py              # Yr.no API
├── frontend/               # Web-käyttöliittymä
│   ├── index.html         # HTML-pohja
│   ├── style.css          # Tyylit
│   └── script.js          # Frontend-logiikka
├── .env                    # Ympäristömuuttujat (ei versionhallintaan)
├── .gitignore
├── requirements.txt
└── README.md
```

## Teknologiat

**Backend:**
- [FastAPI](https://fastapi.tiangolo.com/) - Moderni Python web framework
- [httpx](https://www.python-httpx.org/) - Asynkroninen HTTP client
- [xmltodict](https://github.com/martinblech/xmltodict) - XML-parser (FMI)
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Ympäristömuuttujat

**Frontend:**
- HTML5
- CSS3
- Vanilla JavaScript (Fetch API)

## Datalähteet

| Lähde | Tyyppi | Lisenssi |
|-------|--------|----------|
| **FMI** (Ilmatieteen laitos) | Avoin data | CC BY 4.0 |
| **Foreca** | Kaupallinen API | Ilmainen trial |
| **Yr.no** (MET Norway) | Ilmainen | Vaatii User-Agent |

## Tulevaisuuden kehitysideat

- [ ] Sääennuste 1-7 päivää
- [ ] Redis-caching
- [ ] Kaupunkien suosikit
- [ ] Docker-tuki
- [ ] Responsiivinen mobiili-UI
- [ ] Pytest-testit
- [ ] Historiatietojen tallennus
- [ ] Sääkartat

## Kehittäjälle

**Xmas178**
- GitHub: [@Xmas178](https://github.com/Xmas178)
- Email: xmas178@gmail.com

## Lisenssi

Projekti: MIT License

Huomaa että käytetyt API:t ja datalähteet ovat omien lisenssien alaisia.

## Kiitokset

- [FMI](https://www.ilmatieteenlaitos.fi/) - Avoin säädata
- [Foreca](https://www.foreca.fi/) - Säädatapalvelu
- [Yr.no](https://www.yr.no/) - Norjan meteorologinen instituutti

# Weather API Aggregator

Yksinkertainen backend-palvelu, joka kerää säätiedot eri lähteistä ja tarjoaa ne yhtenäisessä muodossa.  
Nyt mukana myös **selainpohjainen käyttöliittymä (frontend)** ilman Reactia — vain HTML + CSS + JavaScript!

---

## Ominaisuudet

- Hakee säätiedot mistä tahansa kaupungista
- Dat lähteet: FMI (Ilmatieteen laitos), Foreca, Yr.no (MET Norway)
- FastAPI-pohjainen backend
- Asynkroninen haku httpx:llä
- JSON-muotoinen vastaus
- Yksinkertainen frontend selaimessa (hakukenttä ja tulokset)

---

## Teknologiat

- **Backend**: Python 3.9+
- **Framework**: FastAPI
- **HTTP Client**: httpx (async)
- **XML Parser**: xmltodict (FMI)
- **Frontend**: HTML, CSS, JavaScript (fetch API)

---

## Asennus

### 1. Kloonaa repositorio
```bash
git clone https://github.com/Xmas178/weather-api-aggregator.git
cd weather-api-aggregator


### 2. Luo virtuaaliympäristö
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# tai Windows: venv\Scripts\activate


### 3. Asenna riippuvuudet
pip install -r requirements.txt


### 4. Konfiguroi ympäristömuuttujat
Luo `.env` tiedosto projektin juureen:
FORECA_USER=your_username
FORECA_PASSWORD=your_password
FORECA_ADMIN_PASSWORD=your_admin_password


### 5. Käynnistä palvelin
```bash
uvicorn main:app --reload
```

Palvelin käynnistyy osoitteessa: http://localhost:8000
Frontend löytyy osoitteesta: http://localhost:8000/

## API Dokumentaatio

### Interaktiivinen dokumentaatio
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpointit

GET /weather?city=<kaupunki>

Palauttaa nykyisen sään annetusta kaupungista (esim. Oulu).

Vastaus:

{
  "city": "Oulu",
  "source": "FMI",
  "data": {
    "temperature": 7.3,
    "wind_speed": 3.7,
    "humidity": 96,
    "pressure": 1012.6,
    "precipitation": null,
    "weather": "pilvistä tai puolipilvistä"
  }
}

## Frontend (selainkäyttöliittymä)

Frontend sijaitsee kansiossa frontend/ ja käynnistyy automaattisesti FastAPI-palvelimen mukana.
Selaimessa voit:

  - Syöttää kaupungin nimen

  - Paina Enter tai klikkaa "Hae"
→ Näet lämpötilan, kosteuden, ilmanpaineen ja sään kuvauksen

Ulkoasua voi muokata frontend/style.css tiedostossa (esim. värit, marginaalit, fontit).

## Projektin rakenne
weather-api-aggregator/
├── main.py                 # FastAPI sovellus
├── services/
│   ├── foreca.py
│   ├── fmi.py
│   └── yr.py
├── frontend/
│   ├── index.html          # Yksinkertainen käyttöliittymä
│   ├── style.css           # Tyylitiedosto
│   └── script.js           # Frontend-logiikka
├── static/                 # Mahdolliset lisäresurssit
├── .env                    # Ympäristömuuttujat (ei versionhallintaan)
├── requirements.txt
└── README.md


## Tulevaisuuden kehitysideat

- Sääennuste 1–7 päivää

- Caching (Redis)

- Kaupunkien lista ja suosikit

- Docker-tuki

- Responsiivinen UI

- Testaus (pytest)

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

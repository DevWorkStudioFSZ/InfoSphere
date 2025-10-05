# InfoSphere

**InfoSphere** is a location intelligence platform that helps users discover detailed information about places including addresses, ratings, reviews, contact info, and geolocation, by combining **OpenStreetMap (Overpass API)** data with **OpenWeather Geocoding** and a custom-built review system.  

It features a **Next.js frontend** for a seamless user experience and a **Flask backend** for efficient data handling, caching, and API integrations.

---

## Features

- **Search Places**  
  Search for any category (restaurants, parks, hospitals, etc.) in any supported city.

- **Geocoding Integration**  
  Uses **OpenWeather Geocoding API** to convert user-entered addresses or cities into coordinates.

- **Place Details from OpenStreetMap (Overpass API)**  
  Fetches place details such as name, phone number, website, and formatted address.

- **Custom Review System**  
  Users can add, fetch, and delete reviews for specific places with author names and ratings.

- **Caching Layer**  
  Reduces redundant API calls by caching place searches and results in MongoDB.

- **Modular Service Design**  
  Each core feature (geocoding, reviews, DB operations, OSM queries) is implemented as a separate service module.

- **Unit Testing Coverage**  
  Fully tested using Python’s `unittest` and `mock` libraries for reliability and maintainability.

---

## Architecture Overview

```
Frontend (Next.js)
    ↓
Flask REST API (Backend)
    ├── google_places.py      → Handles Overpass (OpenStreetMap) data fetching & normalization
    ├── geocode.py            → Handles OpenWeather Geocoding API calls
    ├── db_service.py         → Handles MongoDB connections, caching, and data persistence
    ├── reviews.py            → Manages review CRUD operations
    └── app.py                → Main Flask entry point (routes registration, CORS setup, etc.)
```

---

## Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | Next.js (React), Tailwind CSS |
| **Backend** | Flask (Python) |
| **Database** | MongoDB |
| **APIs** | OpenWeather Geocoding API, Overpass API (OpenStreetMap) |
| **Environment** | Python 3.12+, Node.js 14+ |
| **Testing** | Python `unittest`, `unittest.mock` |
| **Others** | dotenv, requests, logging |

---

## Installation & Setup

### Clone the Repository
```bash
git clone https://github.com/yourusername/InfoSphere.git
cd InfoSphere
```

### Set Up Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the backend directory:
```env
MONGO_URI=mongodb+srv://your_connection_string
OPENWEATHER_API_KEY=your_openweather_api_key
```

### Run Flask Server
```bash
python app.py
```

By default, it runs at:  
`http://127.0.0.1:5000/`

---

### Set Up Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

By default, it runs at:  
`http://localhost:3000/`

---

## Key API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| **GET** | `/places/<city>/<category>` | Fetch nearby places based on Overpass API |
| **POST** | `/reviews` | Add a review for a place |
| **GET** | `/reviews/<place_id>` | Get all reviews for a specific place |
| **DELETE** | `/reviews/<review_id>` | Delete a review by ID |
| **GET** | `/geocode?address=lahore` | Convert address → latitude/longitude |

---

## How It Works

1. **User enters a city & category** (e.g., “restaurants in Lahore”) → sent to Flask backend.  
2. **Geocode Service** (via OpenWeather API) converts the city name into latitude & longitude.  
3. **Google Places Service** (actually powered by Overpass API) fetches real-world place data.  
4. Results are **cached in MongoDB** to prevent duplicate API calls.  
5. Users can **add reviews**, **see ratings**, and **fetch cached data** instantly.

---

## Running Tests

```bash
python -m unittest -v
```

Tests cover:
- Geocoding logic  
- Overpass API integration  
- Review CRUD operations  
- MongoDB caching  

---

## Folder Structure

```
InfoSphere/
│
├── backend/
│   ├── app.py
│   ├── routes/
│   │   └── reviews.py
│   ├── services/
│   │   ├── db_service.py
│   │   ├── google_places.py
│   │   ├── geocode.py
│   │   └── __init__.py
│   ├── tests/
│   │   ├── test_reviews.py
│   │   ├── test_google_places.py
│   │   └── __init__.py
│   └── .env
│
└── frontend/
    ├── pages/
    ├── components/
    ├── styles/
    └── package.json
```

---

## Contributors

1. Hanzala Salaheen
2. Syeda Sadaf Naqvi
3. Khansa Urooj
4. Humaira Batool

---

## License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute it with attribution.

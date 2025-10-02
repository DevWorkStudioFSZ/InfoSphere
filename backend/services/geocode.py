import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"

def geocode_address(address):
    """
    Geocode an address into latitude and longitude using OpenWeather API.
    Returns {lat, lng, formatted_address} or None on failure.
    """
    if not OPENWEATHER_API_KEY:
        raise ValueError("OPENWEATHER_API_KEY is missing in environment variables")

    try:
        params = {"q": address, "limit": 1, "appid": OPENWEATHER_API_KEY}
        response = requests.get(GEOCODE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data and isinstance(data, list) and len(data) > 0:
            result = data[0]
            return {
                "lat": result.get("lat"),
                "lng": result.get("lon"),
                "formatted_address": f"{result.get('name')}, {result.get('country')}"
            }
        else:
            logger.warning(f"Geocode failed for '{address}': no results")
            return None

    except requests.RequestException as e:
        logger.error(f"Geocoding API request error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in geocode_address: {str(e)}")
        return None
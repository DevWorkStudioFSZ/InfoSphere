import requests
import logging

logger = logging.getLogger(__name__)

# Basic mapping for categories → OSM tags
CATEGORY_MAP = {
    "libraries": {"amenity": "library"},
    "cafes": {"amenity": "cafe"},
    "shops": {"shop": "yes"},
    "restaurants": {"amenity": "restaurant"},
    "hospitals": {"amenity": "hospital"},
}


def search_places(city, category, filters=None):
    """
    Search places using OpenStreetMap Nominatim + Overpass.
    Returns dict: { "search_meta": {...}, "entities": [...] }
    """
    filters = filters or {}
    try:
        # 1️⃣ Geocode city → lat/lon bounding box
        geo_url = "https://nominatim.openstreetmap.org/search"
        geo_params = {"q": city, "format": "json", "limit": 1}
        geo_resp = requests.get(geo_url, params=geo_params, timeout=10, headers={"User-Agent": "InfoSphere-App"})
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()

        if not geo_data:
            raise ValueError(f"City '{city}' not found")

        bbox = geo_data[0].get("boundingbox")
        if not bbox:
            raise ValueError(f"No bounding box found for {city}")

        lat_min, lat_max = bbox[0], bbox[1]
        lon_min, lon_max = bbox[2], bbox[3]

        # 2️⃣ Build Overpass query
        tags = CATEGORY_MAP.get(category.lower())
        if not tags:
            raise ValueError(f"Unsupported category: {category}")

        tag_str = "".join([f'["{k}"="{v}"]' for k, v in tags.items()])
        overpass_query = f"""
        [out:json][timeout:25];
        (
          node{tag_str}({lat_min},{lon_min},{lat_max},{lon_max});
          way{tag_str}({lat_min},{lon_min},{lat_max},{lon_max});
          relation{tag_str}({lat_min},{lon_min},{lat_max},{lon_max});
        );
        out center;
        """

        overpass_url = "https://overpass-api.de/api/interpreter"
        resp = requests.post(overpass_url, data={"data": overpass_query}, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        # 3️⃣ Parse entities
        elements = data.get("elements", [])
        entities = []
        for el in elements:
            tags = el.get("tags", {})
            entities.append({
                "id": el.get("id"),
                "name": tags.get("name", "Unknown"),
                "category": category,
                "lat": el.get("lat") or el.get("center", {}).get("lat"),
                "lon": el.get("lon") or el.get("center", {}).get("lon"),
                "address": tags.get("addr:full") or tags.get("addr:street"),
                "phone": tags.get("phone"),
                "website": tags.get("website"),
            })

        return {
            "search_meta": {
                "city": city,
                "category": category,
                "count": len(entities),
            },
            "entities": entities,
        }

    except Exception as e:
        logger.error(f"OSM search failed: {e}")
        return {
            "search_meta": {"city": city, "category": category, "count": 0},
            "entities": [],
            "error": str(e),
        }


















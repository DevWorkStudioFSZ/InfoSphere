
# from __future__ import annotations
# from dataclasses import dataclass, asdict
# from typing import Dict, List, Optional, Any, Tuple
# from datetime import datetime, timezone
# import re
# import hashlib
# import unicodedata
# from urllib.parse import urlparse, urlunparse

# DAY_KEYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

# def now_iso_utc() -> str:
#     return datetime.now(timezone.utc).isoformat()

# def _slug(s: str) -> str:
#     s = unicodedata.normalize("NFKC", s or "").strip().lower()
#     s = re.sub(r"\s+", " ", s)
#     return s

# def normalize_phone(phone: Optional[str]) -> Optional[str]:
#     if not phone:
#         return None
#     digits = re.sub(r"[^\d+]", "", phone)
#     return digits or None

# def normalize_website(url: Optional[str]) -> Optional[str]:
#     if not url:
#         return None
#     url = url.strip()
#     if not re.match(r"^https?://", url, re.I):
#         url = "http://" + url
#     try:
#         parts = urlparse(url)
#         netloc = parts.netloc.lower()
#         clean = parts._replace(netloc=netloc, fragment="", query="")
#         return urlunparse(clean)
#     except Exception:
#         return None

# def normalize_address(addr: Optional[str]) -> Optional[str]:
#     if not addr:
#         return None
#     a = unicodedata.normalize("NFKC", addr).strip()
#     a = re.sub(r"\s*,\s*", ", ", a)
#     a = re.sub(r"\s+", " ", a)
#     return a

# def compute_entity_id(name: str, address: Optional[str], city: Optional[str], source_id: Optional[str]) -> str:
#     if source_id:
#         return source_id
#     base = f"{_slug(name)}|{_slug(address or '')}|{_slug(city or '')}"
#     return hashlib.sha1(base.encode("utf-8")).hexdigest()

# @dataclass
# class Entity:
#     id: str
#     name: str
#     category: Optional[str]
#     address: Optional[str]
#     city: Optional[str]
#     lat: Optional[float]
#     lng: Optional[float]
#     phone: Optional[str]
#     website: Optional[str]
#     hours: Optional[Dict[str, List[Tuple[str, str]]]]
#     rating_average: Optional[float]
#     rating_count: Optional[int]
#     source: str
#     source_id: Optional[str]
#     source_url: Optional[str]
#     open_now: Optional[bool]
#     created_at: str
#     updated_at: str

#     def to_dict(self) -> Dict[str, Any]:
#         return asdict(self)

#     def to_mongo(self) -> Dict[str, Any]:
#         doc = self.to_dict()
#         doc["_id"] = doc.pop("id")
#         return doc

#     @staticmethod
#     def from_mongo(doc: Dict[str, Any]) -> "Entity":
#         d = dict(doc)
#         d["id"] = d.pop("_id")
#         return Entity(**d)

# def hours_from_google_periods(periods: Any) -> Optional[Dict[str, List[Tuple[str, str]]]]:
#     if not periods:
#         return None
#     out = {k: [] for k in DAY_KEYS}
#     try:
#         for p in periods:
#             o = p.get("open", {})
#             c = p.get("close", {})
#             d_idx = o.get("day")
#             if d_idx is None:
#                 continue
#             day = DAY_KEYS[int(d_idx)]

#             def fmt(t: Optional[str]) -> Optional[str]:
#                 if not t or len(t) < 3: return None
#                 t = t.zfill(4)
#                 return f"{t[:2]}:{t[2:4]}"

#             start = fmt(o.get("time"))
#             end = fmt(c.get("time"))
#             if start and end:
#                 out[day].append((start, end))
#         out = {k: v for k, v in out.items() if v}
#         return out or None
#     except Exception:
#         return None

# def entity_from_google(place: Dict[str, Any], *, city: Optional[str], category: Optional[str]) -> Entity:
#     name = place.get("name") or ""
#     address = place.get("formatted_address") or place.get("vicinity")
#     coords = place.get("geometry", {}).get("location", {})
#     lat = coords.get("lat")
#     lng = coords.get("lng")
#     phone = place.get("formatted_phone_number") or place.get("international_phone_number")
#     website = place.get("website")
#     rating_avg = place.get("rating")
#     rating_cnt = place.get("user_ratings_total")
#     place_id = place.get("place_id")
#     google_url = f"https://maps.google.com/?cid={place_id}" if place_id else None
#     hours = None
#     if place.get("opening_hours", {}).get("periods"):
#         hours = hours_from_google_periods(place["opening_hours"]["periods"])
#     open_now = place.get("opening_hours", {}).get("open_now")

#     clean_phone = normalize_phone(phone)
#     clean_site = normalize_website(website)
#     clean_addr = normalize_address(address)
#     eid = compute_entity_id(name, clean_addr, city, place_id)
#     timestamp = now_iso_utc()

#     return Entity(
#         id=eid,
#         name=name.strip(),
#         category=category,
#         address=clean_addr,
#         city=city,
#         lat=float(lat) if lat is not None else None,
#         lng=float(lng) if lng is not None else None,
#         phone=clean_phone,
#         website=clean_site,
#         hours=hours,
#         rating_average=float(rating_avg) if rating_avg is not None else None,
#         rating_count=int(rating_cnt) if rating_cnt is not None else None,
#         source="google_places",
#         source_id=place_id,
#         source_url=google_url,
#         open_now=open_now if isinstance(open_now, bool) else None,
#         created_at=timestamp,
#         updated_at=timestamp,
#     )




# data/schema.py
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone
import re
import hashlib
import unicodedata
from urllib.parse import urlparse, urlunparse

# Day keys used by hours parsing & filters
DAY_KEYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def now_iso_utc() -> str:
    """Return current UTC time in ISO format (string)."""
    return datetime.now(timezone.utc).isoformat()


def _slug(s: str) -> str:
    """Normalize a string to a searchable slug (lower, collapse whitespace)."""
    s = unicodedata.normalize("NFKC", s or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


def normalize_phone(phone: Optional[str]) -> Optional[str]:
    """Return digits and leading plus only, or None."""
    if not phone:
        return None
    # Keep digits and plus sign
    digits = re.sub(r"[^\d+]", "", phone)
    return digits or None


def normalize_website(url: Optional[str]) -> Optional[str]:
    """Normalize website: ensure scheme, lowercase host, strip query/fragment."""
    if not url:
        return None
    url = url.strip()
    if not re.match(r"^https?://", url, re.I):
        url = "http://" + url
    try:
        parts = urlparse(url)
        netloc = parts.netloc.lower()
        clean = parts._replace(netloc=netloc, fragment="", query="")
        return urlunparse(clean)
    except Exception:
        return None


def normalize_address(addr: Optional[str]) -> Optional[str]:
    """Simple Unicode normalization and whitespace/address cleanup."""
    if not addr:
        return None
    a = unicodedata.normalize("NFKC", addr).strip()
    a = re.sub(r"\s*,\s*", ", ", a)
    a = re.sub(r"\s+", " ", a)
    return a


def compute_entity_id(name: str, address: Optional[str], city: Optional[str], source_id: Optional[str]) -> str:
    """
    Stable id: if source_id provided return it, else compute sha1 of slugged fields.
    """
    if source_id:
        return source_id
    base = f"{_slug(name)}|{_slug(address or '')}|{_slug(city or '')}"
    return hashlib.sha1(base.encode("utf-8")).hexdigest()


@dataclass
class Entity:
    id: str
    name: str
    category: Optional[str]
    address: Optional[str]
    city: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    phone: Optional[str]
    website: Optional[str]
    hours: Optional[Dict[str, List[Tuple[str, str]]]]
    rating_average: Optional[float]
    rating_count: Optional[int]
    source: str
    source_id: Optional[str]
    source_url: Optional[str]
    open_now: Optional[bool]
    created_at: str
    updated_at: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict suitable for JSON response / exporter."""
        return asdict(self)

    def to_mongo(self) -> Dict[str, Any]:
        doc = self.to_dict()
        doc["_id"] = doc.pop("id")
        return doc

    @staticmethod
    def from_mongo(doc: Dict[str, Any]) -> "Entity":
        d = dict(doc)
        d["id"] = d.pop("_id")
        return Entity(**d)


def fmt_time(t: Optional[str]) -> Optional[str]:
    """Helper to format Google Places time (e.g. '900' -> '09:00', '0900' -> '09:00')."""
    if not t or len(t) < 3:
        return None
    t = t.zfill(4)
    return f"{t[:2]}:{t[2:4]}"


def hours_from_google_periods(periods: Any) -> Optional[Dict[str, List[Tuple[str, str]]]]:
    """
    Convert Google Places 'periods' list into dict: { 'mon': [('09:00','17:00'), ...], ... }
    Returns None if no usable hours present.
    """
    if not periods:
        return None
    out: Dict[str, List[Tuple[str, str]]] = {k: [] for k in DAY_KEYS}
    try:
        for p in periods:
            o = p.get("open", {})
            c = p.get("close", {})
            d_idx = o.get("day")
            if d_idx is None:
                continue
            day = DAY_KEYS[int(d_idx)]
            start = fmt_time(o.get("time"))
            end = fmt_time(c.get("time"))
            if start and end:
                out[day].append((start, end))
        out = {k: v for k, v in out.items() if v}
        return out or None
    except Exception:
        return None


def entity_from_google(place: Dict[str, Any], *, city: Optional[str], category: Optional[str]) -> Entity:
    """
    Build an Entity from a Google Places `place` dict.
    Keeps fields minimal and normalized.
    """
    name = place.get("name") or ""
    address = place.get("formatted_address") or place.get("vicinity")
    coords = place.get("geometry", {}).get("location", {})
    lat = coords.get("lat")
    lng = coords.get("lng")
    phone = place.get("formatted_phone_number") or place.get("international_phone_number")
    website = place.get("website")
    rating_avg = place.get("rating")
    rating_cnt = place.get("user_ratings_total")
    place_id = place.get("place_id")
    google_url = f"https://maps.google.com/?cid={place_id}" if place_id else None

    hours = None
    if place.get("opening_hours", {}).get("periods"):
        hours = hours_from_google_periods(place["opening_hours"]["periods"])
    open_now = place.get("opening_hours", {}).get("open_now")

    clean_phone = normalize_phone(phone)
    clean_site = normalize_website(website)
    clean_addr = normalize_address(address)
    eid = compute_entity_id(name, clean_addr, city, place_id)
    timestamp = now_iso_utc()

    return Entity(
        id=eid,
        name=name.strip(),
        category=category,
        address=clean_addr,
        city=city,
        lat=float(lat) if lat is not None else None,
        lng=float(lng) if lng is not None else None,
        phone=clean_phone,
        website=clean_site,
        hours=hours,
        rating_average=float(rating_avg) if rating_avg is not None else None,
        rating_count=int(rating_cnt) if rating_cnt is not None else None,
        source="google_places",
        source_id=place_id,
        source_url=google_url,
        open_now=open_now if isinstance(open_now, bool) else None,
        created_at=timestamp,
        updated_at=timestamp,
    )


# from __future__ import annotations
# from typing import List, Dict, Any, Tuple, Optional
# from math import radians, sin, cos, asin, sqrt
# from urllib.parse import urlparse
# from .schema import Entity, _slug

# def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
#     # meters
#     R = 6371000.0
#     p = radians
#     dlat = p(lat2 - lat1)
#     dlon = p(lon2 - lon1)
#     a = sin(dlat/2)**2 + cos(p(lat1)) * cos(p(lat2)) * sin(dlon/2)**2
#     return 2 * R * asin(sqrt(a))

# def _domain(url: Optional[str]) -> Optional[str]:
#     if not url:
#         return None
#     try:
#         return urlparse(url).netloc
#     except Exception:
#         return None

# def normalize_entities(raw_places: List[Dict[str, Any]], city: Optional[str], category: Optional[str]) -> Tuple[List[Entity], Dict[str, Any]]:
#     """
#     Convert raw Google places to canonical Entities and dedupe.
#     Returns (entities, stats)
#     """
#     from .schema import entity_from_google
#     entities: List[Entity] = [entity_from_google(p, city=city, category=category) for p in raw_places]
#     deduped, stats = dedupe_entities(entities)
#     return deduped, stats

# def dedupe_entities(entities: List[Entity], *, distance_m_threshold: float = 120.0) -> Tuple[List[Entity], Dict[str, Any]]:
#     """
#     Merge entities that are the same business:
#     - Same phone OR same website domain OR same normalized name within ~100m.
#     """
#     clusters: List[List[Entity]] = []
#     used = [False] * len(entities)

#     def same_name(a: Entity, b: Entity) -> bool:
#         return _slug(a.name) == _slug(b.name)

#     def close_by(a: Entity, b: Entity) -> bool:
#         if a.lat is None or a.lng is None or b.lat is None or b.lng is None:
#             return False
#         return _haversine_m(a.lat, a.lng, b.lat, b.lng) <= distance_m_threshold

#     def same_phone(a: Entity, b: Entity) -> bool:
#         return bool(a.phone and b.phone and a.phone == b.phone)

#     def same_site(a: Entity, b: Entity) -> bool:
#         da, db = _domain(a.website), _domain(b.website)
#         return bool(da and db and da == db)

#     for i, e in enumerate(entities):
#         if used[i]:
#             continue
#         cluster = [e]
#         used[i] = True
#         for j in range(i + 1, len(entities)):
#             if used[j]:
#                 continue
#             f = entities[j]
#             if same_phone(e, f) or same_site(e, f) or (same_name(e, f) and close_by(e, f)):
#                 cluster.append(f)
#                 used[j] = True
#         clusters.append(cluster)

#     merged: List[Entity] = [merge_cluster(c) for c in clusters]
#     stats = {
#         "input_count": len(entities),
#         "clusters": len(clusters),
#         "output_count": len(merged),
#         "deduped": len(entities) - len(merged),
#     }
#     return merged, stats

# def merge_cluster(items: List[Entity]) -> Entity:
#     # Choose representative: highest rating_count, else first
#     best = max(items, key=lambda x: (x.rating_count or 0, x.rating_average or 0.0))

#     # Merge fields conservatively
#     def pick(*vals):
#         for v in vals:
#             if v not in (None, "", []):
#                 return v
#         return None

#     phone = pick(*[it.phone for it in items])
#     website = pick(*[it.website for it in items])
#     address = pick(*[it.address for it in items])
#     city = pick(*[it.city for it in items])
#     category = pick(*[it.category for it in items])

#     # ratings: pick max count and average from that record
#     rating_count = max([it.rating_count or 0 for it in items]) or None
#     rating_avg = None
#     if rating_count is not None:
#         cand = [it for it in items if (it.rating_count or 0) == rating_count]
#         rating_avg = cand[0].rating_average if cand else best.rating_average
#     else:
#         rating_avg = best.rating_average

#     # hours: use any non-empty; if multiple exist, keep the one with more days
#     hours_candidates = [it.hours for it in items if it.hours]
#     hours = None
#     if hours_candidates:
#         hours = max(hours_candidates, key=lambda h: len(h))

#     # open_now: prefer True if any True, else any bool, else None
#     open_vals = [it.open_now for it in items if isinstance(it.open_now, bool)]
#     open_now = True if True in open_vals else (open_vals[0] if open_vals else None)

#     # lat/lng: pick from best
#     lat, lng = best.lat, best.lng

#     merged = Entity(
#         id=best.id,  # keep representative id
#         name=best.name,
#         category=category,
#         address=address,
#         city=city,
#         lat=lat,
#         lng=lng,
#         phone=phone,
#         website=website,
#         hours=hours,
#         rating_average=rating_avg,
#         rating_count=rating_count,
#         source=best.source,
#         source_id=best.source_id,
#         source_url=best.source_url,
#         open_now=open_now,
#         created_at=best.created_at,
#         updated_at=best.updated_at,
#     )
#     return merged






from __future__ import annotations
from typing import List, Dict, Any, Tuple, Optional
from math import radians, sin, cos, asin, sqrt
from urllib.parse import urlparse
from .schema import Entity, _slug

def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # meters
    R = 6371000.0
    p = radians
    dlat = p(lat2 - lat1)
    dlon = p(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(p(lat1)) * cos(p(lat2)) * sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

def _domain(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    try:
        return urlparse(url).netloc
    except Exception:
        return None

def normalize_entities(raw_places: List[Dict[str, Any]], city: Optional[str], category: Optional[str]) -> Tuple[List[Entity], Dict[str, Any]]:
    """
    Convert raw Google places to canonical Entities and dedupe.
    Returns (entities, stats)
    """
    from .schema import entity_from_google
    entities: List[Entity] = [entity_from_google(p, city=city, category=category) for p in raw_places]
    deduped, stats = dedupe_entities(entities)
    return deduped, stats

def dedupe_entities(entities: List[Entity], *, distance_m_threshold: float = 120.0) -> Tuple[List[Entity], Dict[str, Any]]:
    """
    Merge entities that are the same business:
    - Same phone OR same website domain OR same normalized name within ~100m.
    """
    clusters: List[List[Entity]] = []
    used = [False] * len(entities)

    def same_name(a: Entity, b: Entity) -> bool:
        return _slug(a.name) == _slug(b.name)

    def close_by(a: Entity, b: Entity) -> bool:
        if a.lat is None or a.lng is None or b.lat is None or b.lng is None:
            return False
        return _haversine_m(a.lat, a.lng, b.lat, b.lng) <= distance_m_threshold

    def same_phone(a: Entity, b: Entity) -> bool:
        return bool(a.phone and b.phone and a.phone == b.phone)

    def same_site(a: Entity, b: Entity) -> bool:
        da, db = _domain(a.website), _domain(b.website)
        return bool(da and db and da == db)

    for i, e in enumerate(entities):
        if used[i]:
            continue
        cluster = [e]
        used[i] = True
        for j in range(i + 1, len(entities)):
            if used[j]:
                continue
            f = entities[j]
            if same_phone(e, f) or same_site(e, f) or (same_name(e, f) and close_by(e, f)):
                cluster.append(f)
                used[j] = True
        clusters.append(cluster)

    merged: List[Entity] = [merge_cluster(c) for c in clusters]
    stats = {
        "input_count": len(entities),
        "clusters": len(clusters),
        "output_count": len(merged),
        "deduped": len(entities) - len(merged),
    }
    return merged, stats

def merge_cluster(items: List[Entity]) -> Entity:
    # Choose representative: highest rating_count, else first
    best = max(items, key=lambda x: (x.rating_count or 0, x.rating_average or 0.0))

    # Merge fields conservatively
    def pick(*vals):
        for v in vals:
            if v not in (None, "", []):
                return v
        return None

    phone = pick(*[it.phone for it in items])
    website = pick(*[it.website for it in items])
    address = pick(*[it.address for it in items])
    city = pick(*[it.city for it in items])
    category = pick(*[it.category for it in items])

    # ratings: pick max count and average from that record
    rating_count = max([it.rating_count or 0 for it in items]) or None
    rating_avg = None
    if rating_count is not None:
        cand = [it for it in items if (it.rating_count or 0) == rating_count]
        rating_avg = cand[0].rating_average if cand else best.rating_average
    else:
        rating_avg = best.rating_average

    # hours: use any non-empty; if multiple exist, keep the one with more days
    hours_candidates = [it.hours for it in items if it.hours]
    hours = None
    if hours_candidates:
        hours = max(hours_candidates, key=lambda h: len(h))

    # open_now: prefer True if any True, else any bool, else None
    open_vals = [it.open_now for it in items if isinstance(it.open_now, bool)]
    open_now = True if True in open_vals else (open_vals[0] if open_vals else None)

    # lat/lng: pick from best
    lat, lng = best.lat, best.lng

    merged = Entity(
        id=best.id,  # keep representative id
        name=best.name,
        category=category,
        address=address,
        city=city,
        lat=lat,
        lng=lng,
        phone=phone,
        website=website,
        hours=hours,
        rating_average=rating_avg,
        rating_count=rating_count,
        source=best.source,
        source_id=best.source_id,
        source_url=best.source_url,
        open_now=open_now,
        created_at=best.created_at,
        updated_at=best.updated_at,
    )
    return merged

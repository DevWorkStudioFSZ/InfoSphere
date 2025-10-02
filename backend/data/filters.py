from __future__ import annotations
from typing import List, Optional, Tuple, Any
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

PK_TZ = ZoneInfo("Asia/Karachi")

# Define DAY_KEYS locally (Mon–Sun)
DAY_KEYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def _now_pk() -> datetime:
    return datetime.now(PK_TZ)


def _day_key(dt: datetime) -> str:
    return DAY_KEYS[dt.weekday()]  # Monday=0


def _time_in_range(now_hhmm: str, intervals: List[Tuple[str, str]]) -> bool:
    for start, end in intervals:
        if start <= now_hhmm <= end:
            return True
    return False


def _get_attr(entity: Any, key: str, default=None):
    """Helper to safely get attributes or dict keys."""
    if isinstance(entity, dict):
        return entity.get(key, default)
    return getattr(entity, key, default)


def is_open_now(entity: dict | object, *, when: Optional[datetime] = None) -> Optional[bool]:
    open_now = _get_attr(entity, "open_now")
    if isinstance(open_now, bool):
        return open_now

    hours = _get_attr(entity, "hours")
    if not hours:
        return False

    dt = when or _now_pk()
    key = _day_key(dt)
    if key not in hours:
        return False

    now_hhmm = dt.strftime("%H:%M")
    return _time_in_range(now_hhmm, hours[key])


def apply_filters(
    entities: List[dict | object],
    *,
    min_rating: Optional[float] = None,
    open_now: Optional[bool] = None,
    has_phone: Optional[bool] = None,
    has_website: Optional[bool] = None,
) -> List[dict | object]:
    """Apply filters on entities (supports both dicts and objects)."""
    out = []
    for e in entities:
        rating = _get_attr(e, "rating_average", 0.0)
        phone = _get_attr(e, "phone")
        website = _get_attr(e, "website")

        if min_rating is not None and (rating or 0.0) < float(min_rating):
            continue
        if has_phone is True and not phone:
            continue
        if has_phone is False and phone:
            continue
        if has_website is True and not website:
            continue
        if has_website is False and website:
            continue
        if open_now is not None:
            on = is_open_now(e)
            if on is None or on is not open_now:
                continue

        out.append(e)

    return out
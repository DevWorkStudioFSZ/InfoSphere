from __future__ import annotations
from typing import List, Dict, Any, Tuple
import csv
import io
import json
from .schema import Entity

def _flatten_entity(e: Entity) -> Dict[str, Any]:
    d = e.to_dict()
    # flatten hours to a single JSON string column for CSV
    if isinstance(d.get("hours"), dict):
        d["hours_json"] = json.dumps(d["hours"], ensure_ascii=False, separators=(",", ":"))
    else:
        d["hours_json"] = None
    # remove nested obj to keep CSV clean
    d.pop("hours", None)
    return d

def export_json(entities: List[Entity], search_meta: Dict[str, Any]) -> bytes:
    payload = {
        "search_meta": search_meta,
        "entities": [e.to_dict() for e in entities],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")

def export_csv(entities: List[Entity]) -> bytes:
    rows = [_flatten_entity(e) for e in entities]
    if not rows:
        return b""
    # stable column order
    fieldnames = [
        "id","name","category","address","city","lat","lng","phone","website",
        "rating_average","rating_count","open_now","source","source_id","source_url",
        "created_at","updated_at","hours_json"
    ]
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    return buf.getvalue().encode("utf-8")

def export_response(fmt: str, entities: List[Entity], search_meta: Dict[str, Any]) -> Tuple[str, bytes, str]:
    """
    Returns (filename, data_bytes, mimetype)
    """
    if fmt.lower() == "json":
        data = export_json(entities, search_meta)
        return ("results.json", data, "application/json; charset=utf-8")
    elif fmt.lower() == "csv":
        data = export_csv(entities)
        return ("results.csv", data, "text/csv; charset=utf-8")
    else:
        raise ValueError("Unsupported export format")
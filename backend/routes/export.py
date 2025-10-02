# from flask import Blueprint, request, jsonify, Response
# from werkzeug.exceptions import BadRequest, NotFound
# from services.google_places import search_places
# from data.normalizer import normalize_entities
# from data.exporter import export_csv
# from utils.error_handler import handle_error

# export_bp = Blueprint("export", __name__)
# export_bp.register_error_handler(Exception, handle_error)  # register globally


# @export_bp.route("/export", methods=["GET"])
# def export_entities():
#     """
#     Export entities from cache or live search.
#     Query params:
#       - city: required if no cache_key
#       - category: required if no cache_key
#       - filters[min_rating]: optional
#       - filters[open_now]: optional
#       - cache_key: optional, use cached results
#       - format: csv (default) or json
#     """
#     fmt = request.args.get("format", "csv").lower()
#     cache_key = request.args.get("cache_key")

#     city = request.args.get("city")
#     category = request.args.get("category")

#     # Filters
#     filters = {}
#     min_rating = request.args.get("filters[min_rating]")
#     if min_rating:
#         try:
#             filters["min_rating"] = float(min_rating)
#         except ValueError:
#             raise BadRequest("filters[min_rating] must be a number")

#     open_now = request.args.get("filters[open_now]")
#     if open_now:
#         filters["open_now"] = open_now.lower() == "true"

#     # Ensure required params
#     if not cache_key and (not city or not category):
#         raise BadRequest("Either cache_key or (city + category) required")

#     # Fetch results (search_places handles cache itself)
#     if cache_key:
#         results = search_places(city, category, filters=filters, cache_key=cache_key)
#     else:
#         results = search_places(city, category, filters=filters)

#     # 🔹 Validate format early (fixes invalid format test)
#     if fmt not in ("json", "csv"):
#         raise BadRequest("Only 'csv' or 'json' allowed")

#     if not results:
#         raise NotFound("No entities found")

#     # Normalize results
#     normalized = normalize_entities(results, city, category)

#     if fmt == "json":
#         return jsonify({
#             "export_meta": {
#                 "count": len(normalized),
#                 "format": "json"
#             },
#             "entities": normalized
#         })

#     elif fmt == "csv":
#         # 🔹 Ensure we have flat list of dict-like objects
#         flat_entities = []
#         for e in normalized:
#             if isinstance(e, list):
#                 flat_entities.extend(e)  # unpack nested lists
#             else:
#                 flat_entities.append(e)

#         # 🔹 Wrap dicts into objects with .to_dict()
#         class DictWrapper:
#             def __init__(self, d):
#                 self._d = d

#             def to_dict(self):
#                 return self._d

#         wrapped = [DictWrapper(e) if isinstance(e, dict) else e for e in flat_entities]

#         return Response(
#             export_csv(wrapped),
#             mimetype="text/csv",
#             headers={"Content-Disposition": "attachment; filename=entities.csv"}
#         )


# routes/export.py
from flask import Blueprint, request, jsonify, Response
import io
import csv
import logging
from services.google_places import search_places

logger = logging.getLogger(__name__)
export_bp = Blueprint("export", __name__)

@export_bp.route("/export/csv", methods=["POST"])
def export_csv():
    """
    POST JSON body: { "city": "...", "category": "...", "filters": {...} }
    Returns: CSV attachment
    """
    try:
        payload = request.get_json(force=True) or {}
        city = payload.get("city")
        category = payload.get("category")
        filters = payload.get("filters", {}) or {}

        if not city or not category:
            return jsonify({"error": "city and category are required"}), 400

        result = search_places(city, category, filters=filters)
        entities = result.get("entities", []) or []

        if not entities:
            return jsonify({"error": "No entities found"}), 404

        fieldnames = ["name", "address", "phone", "website", "lat", "lng", "hours", "source_url", "category"]
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()

        for e in entities:
            writer.writerow({
                "name": e.get("name") or "",
                "address": e.get("address") or "",
                "phone": e.get("phone") or "",
                "website": e.get("website") or "",
                "lat": e.get("lat") or "",
                "lng": e.get("lng") or "",
                "hours": e.get("hours") or "",
                "source_url": e.get("source_url") or "",
                "category": e.get("category") or category,
            })

        csv_bytes = buf.getvalue().encode("utf-8")
        filename = f"{city.replace(' ','_')}_{category.replace(' ','_')}.csv"

        return Response(
            csv_bytes,
            mimetype="text/csv; charset=utf-8",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as exc:
        logger.exception("Failed to build CSV")
        return jsonify({"error": str(exc)}), 500

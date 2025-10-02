# # from flask import Blueprint, request, jsonify
# # from services.google_places import search_places
# # from data.filters import format_place_result, apply_filters
# # from data.normalizer import normalize_entities
# # from data.exporter import export_response

# # router = Blueprint("search", __name__)

# # @router.route("/search", methods=["POST"])
# # def search():
# #     payload = request.get_json(force=True) or {}
# #     city = payload.get("city")
# #     category = payload.get("category")
# #     filters = payload.get("filters", {})  # may contain min_rating, open_now, etc.
# #     export_fmt = payload.get("export", None)  # json / csv

# #     if not city or not category:
# #         return jsonify({"error": "city and category are required"}), 400

# #     try:
# #         # 1. 🔹 Fetch raw search results from OSM (google_places.py)
# #         raw_result = search_places(city, category, filters)
# #         raw_places = raw_result.get("entities", [])   # <-- FIXED

# #         # 2. 🔹 Normalize into Entities + deduplicate
# #         entities, stats = normalize_entities(raw_places, city=city, category=category)

# #         # 3. 🔹 Apply filters (rating, open_now, phone, website)
# #         filtered_entities = apply_filters(
# #             entities,
# #             min_rating=filters.get("min_rating"),
# #             open_now=filters.get("open_now"),
# #             has_phone=filters.get("has_phone"),
# #             has_website=filters.get("has_website"),
# #         )

# #         # 4. 🔹 Export (JSON / CSV) if requested
# #         if export_fmt:
# #             filename, data, mimetype = export_response(export_fmt, filtered_entities, stats)
# #             return (
# #                 data,
# #                 200,
# #                 {
# #                     "Content-Disposition": f"attachment; filename={filename}",
# #                     "Content-Type": mimetype,
# #                 },
# #             )

# #         # 5. 🔹 Default response (for frontend)
# #         return jsonify({
# #             "search_meta": stats,
# #             "entities": [e.to_dict() if hasattr(e, "to_dict") else e for e in filtered_entities]
# #         })

# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500








# from flask import Blueprint, request, jsonify
# from services.google_places import search_places
# from data.filters import apply_filters

# router = Blueprint("search", __name__)

# @router.route("/search", methods=["POST"])
# def search():
#     payload = request.get_json(force=True, silent=True) or {}
#     city = payload.get("city")
#     category = payload.get("category")
#     filters = payload.get("filters", {})  # min_rating, open_now, has_phone, has_website

#     if not city or not category:
#         return jsonify({"error": "city and category are required"}), 400

#     try:
#         # search_places now handles plural/synonym mapping + fallbacks
#         result = search_places(city, category, filters)
#         entities = result.get("entities") or result.get("places") or []

#         # Ensure normalized list of dicts (search_places returns consistent dicts)
#         # Apply filters (works with list of dicts)
#         filtered = apply_filters(
#             entities,
#             min_rating=filters.get("min_rating"),
#             open_now=filters.get("open_now"),
#             has_phone=filters.get("has_phone"),
#             has_website=filters.get("has_website"),
#         )

#         return jsonify({
#             "search_meta": result.get("search_meta", {}),
#             "entities": filtered
#         })

#     except Exception as e:
#         # return stack-like message for dev (you can remove details in production)
#         return jsonify({"error": str(e)}), 500

# routes/search.py

# from flask import Blueprint, request, jsonify
# import logging
# from services.google_places import search_places
# from data.filters import apply_filters

# # Use "router" so app.py import works:
# router = Blueprint("search", __name__)
# logger = logging.getLogger(__name__)


# @router.route("/search", methods=["POST"])
# def search():
#     """
#     API endpoint: POST /api/search
#     Payload: { "city": "Karachi", "category": "libraries", "filters": {...} }
#     """
#     payload = request.get_json(force=True, silent=True) or {}
#     city = payload.get("city")
#     category = payload.get("category")
#     filters = payload.get("filters", {})  # min_rating, open_now, has_phone, has_website

#     if not city or not category:
#         return jsonify({"error": "city and category are required"}), 400

#     try:
#         # 🔹 Call service to fetch raw places
#         result = search_places(city, category, filters)
#         entities = result.get("entities") or result.get("places") or []

#         # 🔹 Apply filters if provided
#         filtered = apply_filters(
#             entities,
#             min_rating=filters.get("min_rating"),
#             open_now=filters.get("open_now"),
#             has_phone=filters.get("has_phone"),
#             has_website=filters.get("has_website"),
#         )

#         return jsonify({
#             "search_meta": result.get("search_meta", {}),
#             "entities": filtered
#         })

#     except ValueError as ve:
#         logger.warning(f"Bad request: {ve}")
#         return jsonify({"error": str(ve)}), 400

#     except Exception as e:
#         logger.error(f"Unexpected search error: {e}")
#         return jsonify({"error": "Internal server error"}), 500



from flask import Blueprint, request, jsonify
import logging
from services.google_places import search_places
from data.filters import apply_filters

# Use consistent name: search_bp
search_bp = Blueprint("search", __name__)
logger = logging.getLogger(__name__)


@search_bp.route("/search", methods=["POST"])
def search():
    """
    API endpoint: POST /api/search
    Payload: { "city": "Karachi", "category": "libraries", "filters": {...} }
    """
    payload = request.get_json(force=True, silent=True) or {}
    city = payload.get("city")
    category = payload.get("category")
    filters = payload.get("filters", {})

    if not city or not category:
        return jsonify({"error": "city and category are required"}), 400

    try:
        # Call service to fetch raw places
        result = search_places(city, category, filters)
        entities = result.get("entities") or result.get("places") or []

        # Apply filters if provided
        filtered = apply_filters(
            entities,
            min_rating=filters.get("min_rating"),
            open_now=filters.get("open_now"),
            has_phone=filters.get("has_phone"),
            has_website=filters.get("has_website"),
        )

        return jsonify({
            "search_meta": result.get("search_meta", {}),
            "entities": filtered
        })

    except ValueError as ve:
        logger.warning(f"Bad request: {ve}")
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        logger.error(f"Unexpected search error: {e}")
        return jsonify({"error": "Internal server error"}), 500

from flask import Blueprint, request, jsonify
from services.db_service import DatabaseService
# from bson import ObjectId

router = Blueprint("reviews", __name__)
db = DatabaseService()

@router.route("/reviews/<place_id>", methods=["GET"])
def get_reviews(place_id):
    """
    Fetch all reviews for a given place_id
    """
    try:
        reviews = db.get_reviews_by_place(place_id)
        return jsonify({"place_id": place_id, "reviews": reviews}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@router.route("/reviews", methods=["POST"])
def add_review():
    """
    Add a new review for a place
    Body: { "place_id": "...", "author": "...", "rating": 4, "text": "..." }
    """
    payload = request.get_json(force=True) or {}
    place_id = payload.get("place_id")
    author = payload.get("author")
    rating = payload.get("rating")
    text = payload.get("text")

    if not place_id or not author or rating is None:
        return jsonify({"error": "place_id, author and rating are required"}), 400

    try:
        review_doc = {
            "place_id": place_id,
            "author": author,
            "rating": rating,
            "text": text,
        }
        inserted_id = db.add_review(review_doc)
        return jsonify({"message": "Review added", "id": str(inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@router.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """
    Delete a review by its ID
    """
    try:
        deleted = db.delete_review(review_id)
        if not deleted:
            return jsonify({"error": "Review not found"}), 404
        return jsonify({"message": "Review deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

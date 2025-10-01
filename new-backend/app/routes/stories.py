from flask import Blueprint, jsonify


bp = Blueprint("stories", __name__)


@bp.get("/")
def list_stories():
    return jsonify([
        {"id": 1, "title": "From Campus to FAANG", "author": "Alice"},
        {"id": 2, "title": "Scholarship Journey", "author": "Sam"},
    ])



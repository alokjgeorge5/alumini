from flask import Blueprint, jsonify


bp = Blueprint("mentorship", __name__)


@bp.get("/")
def list_mentorships():
    return jsonify([
        {"id": 1, "title": "Resume Review", "mentor": "Alice Alumni"},
        {"id": 2, "title": "Interview Prep", "mentor": "Bob Alumni"},
    ])



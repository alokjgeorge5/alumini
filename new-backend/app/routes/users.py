from flask import Blueprint, jsonify


bp = Blueprint("users", __name__)


@bp.get("/")
def list_users():
    # placeholder dataset
    return jsonify([
        {"id": 1, "name": "Alice Alumni", "role": "alumni"},
        {"id": 2, "name": "Sam Student", "role": "student"},
    ])



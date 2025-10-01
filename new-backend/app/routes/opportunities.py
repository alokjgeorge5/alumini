from flask import Blueprint, jsonify


bp = Blueprint("opportunities", __name__)


@bp.get("/")
def list_opportunities():
    return jsonify([
        {"id": 1, "company": "TechCorp", "role": "SWE Intern"},
        {"id": 2, "company": "DataWorks", "role": "Data Analyst"},
    ])



from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import get_engine
from sqlalchemy import text

bp = Blueprint("scholarships", __name__)


@bp.get("/")
def list_scholarships():
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT s.id, s.title, s.description, s.amount, s.deadline, 
                       s.requirements, s.created_at, u.name as posted_by_name
                FROM scholarships s
                LEFT JOIN users u ON s.posted_by = u.id
                WHERE s.is_active = TRUE
                ORDER BY s.deadline ASC
            """))
            
            scholarships = []
            for row in result:
                scholarships.append({
                    "id": row.id,
                    "title": row.title,
                    "description": row.description,
                    "amount": float(row.amount) if row.amount else None,
                    "deadline": row.deadline.isoformat() if row.deadline else None,
                    "requirements": row.requirements,
                    "posted_by_name": row.posted_by_name,
                    "created_at": row.created_at.isoformat() if row.created_at else None
                })
            
            return jsonify(scholarships), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.post("/")
@jwt_required()
def create_scholarship():
    current_user = get_jwt_identity()
    data = request.get_json()
    
    if current_user["role"] != "alumni":
        return jsonify({"error": "Only alumni can post scholarships"}), 403
    
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                INSERT INTO scholarships (title, description, amount, deadline, requirements, posted_by)
                VALUES (:title, :description, :amount, :deadline, :requirements, :posted_by)
            """), {
                "title": data["title"],
                "description": data.get("description"),
                "amount": data.get("amount"),
                "deadline": data.get("deadline"),
                "requirements": data.get("requirements"),
                "posted_by": current_user["id"]
            })
            conn.commit()
            
            return jsonify({"message": "Scholarship created successfully", "id": result.lastrowid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/<int:scholarship_id>")
def get_scholarship(scholarship_id):
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT s.id, s.title, s.description, s.amount, s.deadline, 
                       s.requirements, s.created_at, u.name as posted_by_name, u.email as posted_by_email
                FROM scholarships s
                LEFT JOIN users u ON s.posted_by = u.id
                WHERE s.id = :scholarship_id AND s.is_active = TRUE
            """), {"scholarship_id": scholarship_id})
            
            scholarship = result.fetchone()
            if not scholarship:
                return jsonify({"error": "Scholarship not found"}), 404
            
            return jsonify({
                "id": scholarship.id,
                "title": scholarship.title,
                "description": scholarship.description,
                "amount": float(scholarship.amount) if scholarship.amount else None,
                "deadline": scholarship.deadline.isoformat() if scholarship.deadline else None,
                "requirements": scholarship.requirements,
                "posted_by_name": scholarship.posted_by_name,
                "posted_by_email": scholarship.posted_by_email,
                "created_at": scholarship.created_at.isoformat() if scholarship.created_at else None
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

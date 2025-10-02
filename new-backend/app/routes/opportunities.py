from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import get_engine
from ..middleware import alumni_required, admin_required
from sqlalchemy import text

bp = Blueprint("opportunities", __name__)


@bp.get("/")
def list_opportunities():
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT o.id, o.title, o.company, o.description, o.requirements, 
                       o.location, o.salary_range, o.type, o.created_at,
                       u.name as posted_by_name
                FROM opportunities o
                LEFT JOIN users u ON o.posted_by = u.id
                WHERE o.is_active = TRUE
                ORDER BY o.created_at DESC
            """))
            
            opportunities = []
            for row in result:
                opportunities.append({
                    "id": row.id,
                    "title": row.title,
                    "company": row.company,
                    "description": row.description,
                    "requirements": row.requirements,
                    "location": row.location,
                    "salary_range": row.salary_range,
                    "type": row.type,
                    "posted_by_name": row.posted_by_name,
                    "created_at": row.created_at.isoformat() if row.created_at else None
                })
            
            return jsonify(opportunities), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.post("/")
@alumni_required
def create_opportunity():
    current_user = get_jwt_identity()
    data = request.get_json()
    
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                INSERT INTO opportunities (title, company, description, requirements, 
                                        location, salary_range, type, posted_by)
                VALUES (:title, :company, :description, :requirements, 
                       :location, :salary_range, :type, :posted_by)
            """), {
                "title": data["title"],
                "company": data["company"],
                "description": data.get("description"),
                "requirements": data.get("requirements"),
                "location": data.get("location"),
                "salary_range": data.get("salary_range"),
                "type": data["type"],
                "posted_by": current_user["id"]
            })
            conn.commit()
            
            return jsonify({"message": "Opportunity created successfully", "id": result.lastrowid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/<int:opportunity_id>")
def get_opportunity(opportunity_id):
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT o.id, o.title, o.company, o.description, o.requirements,
                       o.location, o.salary_range, o.type, o.created_at, o.posted_by,
                       u.name as posted_by_name, u.email as posted_by_email
                FROM opportunities o
                LEFT JOIN users u ON o.posted_by = u.id
                WHERE o.id = :opportunity_id AND o.is_active = TRUE
            """), {"opportunity_id": opportunity_id})

            opportunity = result.fetchone()
            if not opportunity:
                return jsonify({"error": "Opportunity not found"}), 404

            return jsonify({
                "id": opportunity.id,
                "title": opportunity.title,
                "company": opportunity.company,
                "description": opportunity.description,
                "requirements": opportunity.requirements,
                "location": opportunity.location,
                "salary_range": opportunity.salary_range,
                "type": opportunity.type,
                "posted_by": opportunity.posted_by,
                "posted_by_name": opportunity.posted_by_name,
                "posted_by_email": opportunity.posted_by_email,
                "created_at": opportunity.created_at.isoformat() if opportunity.created_at else None
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.put("/<int:opportunity_id>")
@alumni_required
def update_opportunity(opportunity_id):
    current_user = get_jwt_identity()
    data = request.get_json()

    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT posted_by FROM opportunities WHERE id = :opportunity_id
            """), {"opportunity_id": opportunity_id})

            opportunity = result.fetchone()
            if not opportunity:
                return jsonify({"error": "Opportunity not found"}), 404

            if opportunity.posted_by != current_user["id"] and current_user["role"] != "admin":
                return jsonify({"error": "You can only update your own opportunities"}), 403

            conn.execute(text("""
                UPDATE opportunities SET
                    title = :title, company = :company, description = :description,
                    requirements = :requirements, location = :location,
                    salary_range = :salary_range, type = :type
                WHERE id = :opportunity_id
            """), {
                "opportunity_id": opportunity_id,
                "title": data.get("title"),
                "company": data.get("company"),
                "description": data.get("description"),
                "requirements": data.get("requirements"),
                "location": data.get("location"),
                "salary_range": data.get("salary_range"),
                "type": data.get("type")
            })
            conn.commit()

            return jsonify({"message": "Opportunity updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.delete("/<int:opportunity_id>")
@alumni_required
def delete_opportunity(opportunity_id):
    current_user = get_jwt_identity()

    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT posted_by FROM opportunities WHERE id = :opportunity_id
            """), {"opportunity_id": opportunity_id})

            opportunity = result.fetchone()
            if not opportunity:
                return jsonify({"error": "Opportunity not found"}), 404

            if opportunity.posted_by != current_user["id"] and current_user["role"] != "admin":
                return jsonify({"error": "You can only delete your own opportunities"}), 403

            conn.execute(text("""
                UPDATE opportunities SET is_active = FALSE WHERE id = :opportunity_id
            """), {"opportunity_id": opportunity_id})
            conn.commit()

            return jsonify({"message": "Opportunity deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import get_engine
from ..middleware import admin_required
from sqlalchemy import text
import bcrypt

bp = Blueprint("admin", __name__)


@bp.get("/dashboard")
@admin_required
def get_dashboard_stats():
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT
                    (SELECT COUNT(*) FROM users WHERE role = 'student') as total_students,
                    (SELECT COUNT(*) FROM users WHERE role = 'alumni') as total_alumni,
                    (SELECT COUNT(*) FROM users WHERE role = 'admin') as total_admins,
                    (SELECT COUNT(*) FROM opportunities WHERE is_active = TRUE) as active_opportunities,
                    (SELECT COUNT(*) FROM scholarships WHERE status = 'active') as active_scholarships,
                    (SELECT COUNT(*) FROM mentorship_requests WHERE status = 'pending') as pending_mentorships,
                    (SELECT COUNT(*) FROM applications) as total_applications,
                    (SELECT COUNT(*) FROM scholarship_applications) as total_scholarship_applications,
                    (SELECT COUNT(*) FROM messages WHERE is_read = FALSE) as unread_messages,
                    (SELECT COUNT(*) FROM stories) as total_stories
            """))

            stats = result.fetchone()

            return jsonify({
                "users": {
                    "total_students": stats.total_students,
                    "total_alumni": stats.total_alumni,
                    "total_admins": stats.total_admins,
                    "total": stats.total_students + stats.total_alumni + stats.total_admins
                },
                "opportunities": {
                    "active": stats.active_opportunities
                },
                "scholarships": {
                    "active": stats.active_scholarships,
                    "total_applications": stats.total_scholarship_applications
                },
                "mentorships": {
                    "pending": stats.pending_mentorships
                },
                "applications": {
                    "total": stats.total_applications
                },
                "messages": {
                    "unread": stats.unread_messages
                },
                "stories": {
                    "total": stats.total_stories
                }
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/users")
@admin_required
def list_all_users():
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, name, email, role, graduation_year, major, company, position,
                       cgpa, category, phone, email_verified, created_at
                FROM users
                ORDER BY created_at DESC
            """))

            users = []
            for row in result:
                users.append({
                    "id": row.id,
                    "name": row.name,
                    "email": row.email,
                    "role": row.role,
                    "graduation_year": row.graduation_year,
                    "major": row.major,
                    "company": row.company,
                    "position": row.position,
                    "cgpa": float(row.cgpa) if row.cgpa else None,
                    "category": row.category,
                    "phone": row.phone,
                    "email_verified": row.email_verified,
                    "created_at": row.created_at.isoformat() if row.created_at else None
                })

            return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.put("/users/<int:user_id>")
@admin_required
def update_user(user_id):
    data = request.get_json()

    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id FROM users WHERE id = :user_id"), {"user_id": user_id})
            if not result.fetchone():
                return jsonify({"error": "User not found"}), 404

            update_fields = []
            params = {"user_id": user_id}

            if "name" in data:
                update_fields.append("name = :name")
                params["name"] = data["name"]
            if "email" in data:
                update_fields.append("email = :email")
                params["email"] = data["email"]
            if "role" in data and data["role"] in ["student", "alumni", "admin"]:
                update_fields.append("role = :role")
                params["role"] = data["role"]
            if "graduation_year" in data:
                update_fields.append("graduation_year = :graduation_year")
                params["graduation_year"] = data["graduation_year"]
            if "major" in data:
                update_fields.append("major = :major")
                params["major"] = data["major"]
            if "company" in data:
                update_fields.append("company = :company")
                params["company"] = data["company"]
            if "position" in data:
                update_fields.append("position = :position")
                params["position"] = data["position"]
            if "cgpa" in data:
                update_fields.append("cgpa = :cgpa")
                params["cgpa"] = data["cgpa"]
            if "category" in data:
                update_fields.append("category = :category")
                params["category"] = data["category"]
            if "phone" in data:
                update_fields.append("phone = :phone")
                params["phone"] = data["phone"]
            if "bio" in data:
                update_fields.append("bio = :bio")
                params["bio"] = data["bio"]
            if "skills" in data:
                update_fields.append("skills = :skills")
                params["skills"] = data["skills"]

            if not update_fields:
                return jsonify({"error": "No valid fields to update"}), 400

            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = :user_id"
            conn.execute(text(query), params)
            conn.commit()

            return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.delete("/users/<int:user_id>")
@admin_required
def delete_user(user_id):
    current_user = get_jwt_identity()

    if current_user["id"] == user_id:
        return jsonify({"error": "You cannot delete your own account"}), 400

    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id FROM users WHERE id = :user_id"), {"user_id": user_id})
            if not result.fetchone():
                return jsonify({"error": "User not found"}), 404

            conn.execute(text("DELETE FROM users WHERE id = :user_id"), {"user_id": user_id})
            conn.commit()

            return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.post("/users")
@admin_required
def create_user():
    data = request.get_json()

    if not data.get("email") or not data.get("password") or not data.get("name") or not data.get("role"):
        return jsonify({"error": "Email, password, name, and role are required"}), 400

    if data["role"] not in ["student", "alumni", "admin"]:
        return jsonify({"error": "Invalid role"}), 400

    password_hash = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": data["email"]})
            if result.fetchone():
                return jsonify({"error": "User with this email already exists"}), 400

            conn.execute(text("""
                INSERT INTO users (email, password_hash, name, role, graduation_year, major,
                                 company, position, bio, skills, cgpa, category, phone)
                VALUES (:email, :password_hash, :name, :role, :graduation_year, :major,
                       :company, :position, :bio, :skills, :cgpa, :category, :phone)
            """), {
                "email": data["email"],
                "password_hash": password_hash,
                "name": data["name"],
                "role": data["role"],
                "graduation_year": data.get("graduation_year"),
                "major": data.get("major"),
                "company": data.get("company"),
                "position": data.get("position"),
                "bio": data.get("bio"),
                "skills": data.get("skills"),
                "cgpa": data.get("cgpa"),
                "category": data.get("category"),
                "phone": data.get("phone")
            })
            conn.commit()

            return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/opportunities")
@admin_required
def list_all_opportunities():
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT o.id, o.title, o.company, o.type, o.is_active, o.created_at,
                       u.name as posted_by_name, u.email as posted_by_email
                FROM opportunities o
                LEFT JOIN users u ON o.posted_by = u.id
                ORDER BY o.created_at DESC
            """))

            opportunities = []
            for row in result:
                opportunities.append({
                    "id": row.id,
                    "title": row.title,
                    "company": row.company,
                    "type": row.type,
                    "is_active": row.is_active,
                    "posted_by_name": row.posted_by_name,
                    "posted_by_email": row.posted_by_email,
                    "created_at": row.created_at.isoformat() if row.created_at else None
                })

            return jsonify(opportunities), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.delete("/opportunities/<int:opportunity_id>")
@admin_required
def admin_delete_opportunity(opportunity_id):
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id FROM opportunities WHERE id = :id"), {"id": opportunity_id})
            if not result.fetchone():
                return jsonify({"error": "Opportunity not found"}), 404

            conn.execute(text("UPDATE opportunities SET is_active = FALSE WHERE id = :id"), {"id": opportunity_id})
            conn.commit()

            return jsonify({"message": "Opportunity deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/scholarships")
@admin_required
def list_all_scholarships():
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT s.id, s.title, s.amount, s.deadline, s.status, s.created_at,
                       s.cgpa_requirement, s.category_requirement,
                       u.name as created_by_name, u.email as created_by_email,
                       (SELECT COUNT(*) FROM scholarship_applications WHERE scholarship_id = s.id) as application_count
                FROM scholarships s
                LEFT JOIN users u ON s.created_by = u.id
                ORDER BY s.created_at DESC
            """))

            scholarships = []
            for row in result:
                scholarships.append({
                    "id": row.id,
                    "title": row.title,
                    "amount": float(row.amount) if row.amount else None,
                    "deadline": row.deadline.isoformat() if row.deadline else None,
                    "status": row.status,
                    "cgpa_requirement": float(row.cgpa_requirement) if row.cgpa_requirement else None,
                    "category_requirement": row.category_requirement,
                    "created_by_name": row.created_by_name,
                    "created_by_email": row.created_by_email,
                    "application_count": row.application_count,
                    "created_at": row.created_at.isoformat() if row.created_at else None
                })

            return jsonify(scholarships), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.delete("/scholarships/<int:scholarship_id>")
@admin_required
def admin_delete_scholarship(scholarship_id):
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id FROM scholarships WHERE id = :id"), {"id": scholarship_id})
            if not result.fetchone():
                return jsonify({"error": "Scholarship not found"}), 404

            conn.execute(text("UPDATE scholarships SET status = 'inactive' WHERE id = :id"), {"id": scholarship_id})
            conn.commit()

            return jsonify({"message": "Scholarship deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/applications")
@admin_required
def list_all_applications():
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT a.id, a.type, a.status, a.created_at,
                       u.name as applicant_name, u.email as applicant_email,
                       o.title as opportunity_title,
                       s.title as scholarship_title
                FROM applications a
                JOIN users u ON a.applicant_id = u.id
                LEFT JOIN opportunities o ON a.opportunity_id = o.id
                LEFT JOIN scholarships s ON a.scholarship_id = s.id
                ORDER BY a.created_at DESC
            """))

            applications = []
            for row in result:
                applications.append({
                    "id": row.id,
                    "type": row.type,
                    "status": row.status,
                    "applicant_name": row.applicant_name,
                    "applicant_email": row.applicant_email,
                    "opportunity_title": row.opportunity_title,
                    "scholarship_title": row.scholarship_title,
                    "created_at": row.created_at.isoformat() if row.created_at else None
                })

            return jsonify(applications), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

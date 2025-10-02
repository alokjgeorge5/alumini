from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import get_engine
from sqlalchemy import text

bp = Blueprint("users", __name__)


@bp.get("/")
def list_users():
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, name, role, graduation_year, major, company, position, bio, skills
                FROM users ORDER BY name
            """))
            
            users = []
            for row in result:
                users.append({
                    "id": row.id,
                    "name": row.name,
                    "role": row.role,
                    "graduation_year": row.graduation_year,
                    "major": row.major,
                    "company": row.company,
                    "position": row.position,
                    "bio": row.bio,
                    "skills": row.skills
                })
            
            return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/alumni")
def list_alumni():
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, name, graduation_year, major, company, position, bio, skills
                FROM users WHERE role = 'alumni' ORDER BY name
            """))
            
            alumni = []
            for row in result:
                alumni.append({
                    "id": row.id,
                    "name": row.name,
                    "graduation_year": row.graduation_year,
                    "major": row.major,
                    "company": row.company,
                    "position": row.position,
                    "bio": row.bio,
                    "skills": row.skills
                })
            
            return jsonify(alumni), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/students")
def list_students():
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, name, graduation_year, major, bio, skills
                FROM users WHERE role = 'student' ORDER BY name
            """))
            
            students = []
            for row in result:
                students.append({
                    "id": row.id,
                    "name": row.name,
                    "graduation_year": row.graduation_year,
                    "major": row.major,
                    "bio": row.bio,
                    "skills": row.skills
                })
            
            return jsonify(students), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/<int:user_id>")
def get_user(user_id):
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, name, email, role, graduation_year, major, company, position,
                       bio, skills, cgpa, category, phone, email_verified, created_at
                FROM users WHERE id = :user_id
            """), {"user_id": user_id})

            user = result.fetchone()
            if not user:
                return jsonify({"error": "User not found"}), 404

            user_data = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "graduation_year": user.graduation_year,
                "major": user.major,
                "company": user.company,
                "position": user.position,
                "bio": user.bio,
                "skills": user.skills,
                "cgpa": float(user.cgpa) if user.cgpa else None,
                "category": user.category,
                "phone": user.phone,
                "email_verified": user.email_verified,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }

            if user.role == "student":
                result = conn.execute(text("""
                    SELECT COUNT(*) as count FROM scholarship_applications WHERE student_id = :user_id
                """), {"user_id": user_id})
                user_data["scholarship_applications_count"] = result.fetchone().count

                result = conn.execute(text("""
                    SELECT COUNT(*) as count FROM applications WHERE applicant_id = :user_id
                """), {"user_id": user_id})
                user_data["job_applications_count"] = result.fetchone().count

                result = conn.execute(text("""
                    SELECT COUNT(*) as count FROM mentorship_requests WHERE student_id = :user_id
                """), {"user_id": user_id})
                user_data["mentorship_requests_count"] = result.fetchone().count

            elif user.role == "alumni":
                result = conn.execute(text("""
                    SELECT COUNT(*) as count FROM opportunities WHERE posted_by = :user_id AND is_active = TRUE
                """), {"user_id": user_id})
                user_data["active_opportunities_count"] = result.fetchone().count

                result = conn.execute(text("""
                    SELECT COUNT(*) as count FROM scholarships WHERE created_by = :user_id AND status = 'active'
                """), {"user_id": user_id})
                user_data["active_scholarships_count"] = result.fetchone().count

                result = conn.execute(text("""
                    SELECT COUNT(*) as count FROM mentorship_requests WHERE mentor_id = :user_id AND status = 'accepted'
                """), {"user_id": user_id})
                user_data["mentorship_count"] = result.fetchone().count

            return jsonify(user_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.put("/profile")
@jwt_required()
def update_profile():
    current_user = get_jwt_identity()
    data = request.get_json()

    engine = get_engine()
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                UPDATE users SET
                    name = :name, graduation_year = :graduation_year, major = :major,
                    company = :company, position = :position, bio = :bio, skills = :skills,
                    cgpa = :cgpa, category = :category, phone = :phone
                WHERE id = :user_id
            """), {
                "user_id": current_user["id"],
                "name": data.get("name", current_user["name"]),
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

            return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



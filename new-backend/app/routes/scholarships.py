from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import get_engine
from ..middleware import alumni_required, student_required, authenticated_required
from sqlalchemy import text

bp = Blueprint("scholarships", __name__)


@bp.get("/")
def list_scholarships():
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT s.id, s.title, s.description, s.eligibility_criteria,
                       s.cgpa_requirement, s.category_requirement, s.amount, s.deadline,
                       s.status, s.created_at, u.name as created_by_name
                FROM scholarships s
                LEFT JOIN users u ON s.created_by = u.id
                WHERE s.status = 'active'
                ORDER BY s.deadline ASC
            """))

            scholarships = []
            for row in result:
                scholarships.append({
                    "id": row.id,
                    "title": row.title,
                    "description": row.description,
                    "eligibility_criteria": row.eligibility_criteria,
                    "cgpa_requirement": float(row.cgpa_requirement) if row.cgpa_requirement else None,
                    "category_requirement": row.category_requirement,
                    "amount": float(row.amount) if row.amount else None,
                    "deadline": row.deadline.isoformat() if row.deadline else None,
                    "status": row.status,
                    "created_by_name": row.created_by_name,
                    "created_at": row.created_at.isoformat() if row.created_at else None
                })

            return jsonify(scholarships), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/eligible")
@student_required
def get_eligible_scholarships():
    current_user = get_jwt_identity()

    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT cgpa, category FROM users WHERE id = :user_id
            """), {"user_id": current_user["id"]})

            user_data = result.fetchone()
            if not user_data:
                return jsonify({"error": "User not found"}), 404

            user_cgpa = user_data.cgpa if user_data.cgpa else 0.0
            user_category = user_data.category

            result = conn.execute(text("""
                SELECT s.id, s.title, s.description, s.eligibility_criteria,
                       s.cgpa_requirement, s.category_requirement, s.amount, s.deadline,
                       s.status, s.created_at, u.name as created_by_name
                FROM scholarships s
                LEFT JOIN users u ON s.created_by = u.id
                WHERE s.status = 'active'
                  AND (s.cgpa_requirement IS NULL OR s.cgpa_requirement <= :user_cgpa)
                  AND (s.category_requirement IS NULL OR s.category_requirement = :user_category)
                ORDER BY s.deadline ASC
            """), {"user_cgpa": user_cgpa, "user_category": user_category})

            scholarships = []
            for row in result:
                scholarships.append({
                    "id": row.id,
                    "title": row.title,
                    "description": row.description,
                    "eligibility_criteria": row.eligibility_criteria,
                    "cgpa_requirement": float(row.cgpa_requirement) if row.cgpa_requirement else None,
                    "category_requirement": row.category_requirement,
                    "amount": float(row.amount) if row.amount else None,
                    "deadline": row.deadline.isoformat() if row.deadline else None,
                    "status": row.status,
                    "created_by_name": row.created_by_name,
                    "created_at": row.created_at.isoformat() if row.created_at else None
                })

            return jsonify(scholarships), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.post("/")
@alumni_required
def create_scholarship():
    current_user = get_jwt_identity()
    data = request.get_json()

    if not data.get("title") or not data.get("amount"):
        return jsonify({"error": "Title and amount are required"}), 400

    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                INSERT INTO scholarships (title, description, eligibility_criteria,
                                        cgpa_requirement, category_requirement, amount,
                                        deadline, created_by, status)
                VALUES (:title, :description, :eligibility_criteria,
                       :cgpa_requirement, :category_requirement, :amount,
                       :deadline, :created_by, :status)
            """), {
                "title": data["title"],
                "description": data.get("description"),
                "eligibility_criteria": data.get("eligibility_criteria"),
                "cgpa_requirement": data.get("cgpa_requirement"),
                "category_requirement": data.get("category_requirement"),
                "amount": data["amount"],
                "deadline": data.get("deadline"),
                "created_by": current_user["id"],
                "status": data.get("status", "active")
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
                SELECT s.id, s.title, s.description, s.eligibility_criteria,
                       s.cgpa_requirement, s.category_requirement, s.amount, s.deadline,
                       s.status, s.created_by, s.created_at,
                       u.name as created_by_name, u.email as created_by_email
                FROM scholarships s
                LEFT JOIN users u ON s.created_by = u.id
                WHERE s.id = :scholarship_id
            """), {"scholarship_id": scholarship_id})

            scholarship = result.fetchone()
            if not scholarship:
                return jsonify({"error": "Scholarship not found"}), 404

            return jsonify({
                "id": scholarship.id,
                "title": scholarship.title,
                "description": scholarship.description,
                "eligibility_criteria": scholarship.eligibility_criteria,
                "cgpa_requirement": float(scholarship.cgpa_requirement) if scholarship.cgpa_requirement else None,
                "category_requirement": scholarship.category_requirement,
                "amount": float(scholarship.amount) if scholarship.amount else None,
                "deadline": scholarship.deadline.isoformat() if scholarship.deadline else None,
                "status": scholarship.status,
                "created_by": scholarship.created_by,
                "created_by_name": scholarship.created_by_name,
                "created_by_email": scholarship.created_by_email,
                "created_at": scholarship.created_at.isoformat() if scholarship.created_at else None
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.put("/<int:scholarship_id>")
@alumni_required
def update_scholarship(scholarship_id):
    current_user = get_jwt_identity()
    data = request.get_json()

    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT created_by FROM scholarships WHERE id = :scholarship_id
            """), {"scholarship_id": scholarship_id})

            scholarship = result.fetchone()
            if not scholarship:
                return jsonify({"error": "Scholarship not found"}), 404

            if scholarship.created_by != current_user["id"] and current_user["role"] != "admin":
                return jsonify({"error": "You can only update your own scholarships"}), 403

            conn.execute(text("""
                UPDATE scholarships SET
                    title = :title, description = :description,
                    eligibility_criteria = :eligibility_criteria,
                    cgpa_requirement = :cgpa_requirement,
                    category_requirement = :category_requirement,
                    amount = :amount, deadline = :deadline, status = :status
                WHERE id = :scholarship_id
            """), {
                "scholarship_id": scholarship_id,
                "title": data.get("title"),
                "description": data.get("description"),
                "eligibility_criteria": data.get("eligibility_criteria"),
                "cgpa_requirement": data.get("cgpa_requirement"),
                "category_requirement": data.get("category_requirement"),
                "amount": data.get("amount"),
                "deadline": data.get("deadline"),
                "status": data.get("status", "active")
            })
            conn.commit()

            return jsonify({"message": "Scholarship updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.delete("/<int:scholarship_id>")
@alumni_required
def delete_scholarship(scholarship_id):
    current_user = get_jwt_identity()

    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT created_by FROM scholarships WHERE id = :scholarship_id
            """), {"scholarship_id": scholarship_id})

            scholarship = result.fetchone()
            if not scholarship:
                return jsonify({"error": "Scholarship not found"}), 404

            if scholarship.created_by != current_user["id"] and current_user["role"] != "admin":
                return jsonify({"error": "You can only delete your own scholarships"}), 403

            conn.execute(text("""
                UPDATE scholarships SET status = 'inactive' WHERE id = :scholarship_id
            """), {"scholarship_id": scholarship_id})
            conn.commit()

            return jsonify({"message": "Scholarship deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.post("/<int:scholarship_id>/apply")
@student_required
def apply_for_scholarship(scholarship_id):
    current_user = get_jwt_identity()
    data = request.get_json()

    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id FROM scholarships WHERE id = :scholarship_id AND status = 'active'
            """), {"scholarship_id": scholarship_id})

            if not result.fetchone():
                return jsonify({"error": "Scholarship not found or inactive"}), 404

            result = conn.execute(text("""
                SELECT id FROM scholarship_applications
                WHERE student_id = :student_id AND scholarship_id = :scholarship_id
            """), {"student_id": current_user["id"], "scholarship_id": scholarship_id})

            if result.fetchone():
                return jsonify({"error": "You have already applied for this scholarship"}), 400

            conn.execute(text("""
                INSERT INTO scholarship_applications (student_id, scholarship_id, cover_letter, additional_info)
                VALUES (:student_id, :scholarship_id, :cover_letter, :additional_info)
            """), {
                "student_id": current_user["id"],
                "scholarship_id": scholarship_id,
                "cover_letter": data.get("cover_letter"),
                "additional_info": data.get("additional_info")
            })
            conn.commit()

            return jsonify({"message": "Application submitted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/<int:scholarship_id>/applications")
@alumni_required
def get_scholarship_applications(scholarship_id):
    current_user = get_jwt_identity()

    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT created_by FROM scholarships WHERE id = :scholarship_id
            """), {"scholarship_id": scholarship_id})

            scholarship = result.fetchone()
            if not scholarship:
                return jsonify({"error": "Scholarship not found"}), 404

            if scholarship.created_by != current_user["id"] and current_user["role"] != "admin":
                return jsonify({"error": "Access denied"}), 403

            result = conn.execute(text("""
                SELECT sa.id, sa.student_id, sa.application_date, sa.status,
                       sa.cover_letter, sa.additional_info,
                       u.name, u.email, u.cgpa, u.category, u.major
                FROM scholarship_applications sa
                JOIN users u ON sa.student_id = u.id
                WHERE sa.scholarship_id = :scholarship_id
                ORDER BY sa.application_date DESC
            """), {"scholarship_id": scholarship_id})

            applications = []
            for row in result:
                applications.append({
                    "id": row.id,
                    "student_id": row.student_id,
                    "student_name": row.name,
                    "student_email": row.email,
                    "student_cgpa": float(row.cgpa) if row.cgpa else None,
                    "student_category": row.category,
                    "student_major": row.major,
                    "application_date": row.application_date.isoformat() if row.application_date else None,
                    "status": row.status,
                    "cover_letter": row.cover_letter,
                    "additional_info": row.additional_info
                })

            return jsonify(applications), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/applications/my")
@student_required
def get_my_applications():
    current_user = get_jwt_identity()

    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT sa.id, sa.scholarship_id, sa.application_date, sa.status,
                       s.title, s.amount, s.deadline, s.status as scholarship_status
                FROM scholarship_applications sa
                JOIN scholarships s ON sa.scholarship_id = s.id
                WHERE sa.student_id = :student_id
                ORDER BY sa.application_date DESC
            """), {"student_id": current_user["id"]})

            applications = []
            for row in result:
                applications.append({
                    "id": row.id,
                    "scholarship_id": row.scholarship_id,
                    "scholarship_title": row.title,
                    "scholarship_amount": float(row.amount) if row.amount else None,
                    "scholarship_deadline": row.deadline.isoformat() if row.deadline else None,
                    "scholarship_status": row.scholarship_status,
                    "application_date": row.application_date.isoformat() if row.application_date else None,
                    "status": row.status
                })

            return jsonify(applications), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.put("/applications/<int:application_id>/status")
@alumni_required
def update_application_status(application_id):
    current_user = get_jwt_identity()
    data = request.get_json()

    if not data.get("status"):
        return jsonify({"error": "Status is required"}), 400

    if data["status"] not in ["submitted", "under_review", "approved", "rejected"]:
        return jsonify({"error": "Invalid status"}), 400

    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT sa.id, s.created_by
                FROM scholarship_applications sa
                JOIN scholarships s ON sa.scholarship_id = s.id
                WHERE sa.id = :application_id
            """), {"application_id": application_id})

            application = result.fetchone()
            if not application:
                return jsonify({"error": "Application not found"}), 404

            if application.created_by != current_user["id"] and current_user["role"] != "admin":
                return jsonify({"error": "Access denied"}), 403

            conn.execute(text("""
                UPDATE scholarship_applications
                SET status = :status
                WHERE id = :application_id
            """), {"application_id": application_id, "status": data["status"]})
            conn.commit()

            return jsonify({"message": "Application status updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

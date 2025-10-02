from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request


def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            current_user = get_jwt_identity()

            if not current_user or "role" not in current_user:
                return jsonify({"error": "Invalid token"}), 401

            if current_user["role"] not in allowed_roles:
                return jsonify({
                    "error": "Access denied",
                    "message": f"This endpoint requires one of these roles: {', '.join(allowed_roles)}"
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def admin_required(fn):
    return role_required("admin")(fn)


def alumni_required(fn):
    return role_required("alumni", "admin")(fn)


def student_required(fn):
    return role_required("student", "admin")(fn)


def authenticated_required(fn):
    return role_required("student", "alumni", "admin")(fn)

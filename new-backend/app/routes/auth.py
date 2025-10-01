from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from ..models import get_engine
from sqlalchemy import text

bp = Blueprint("auth", __name__)


@bp.post("/register")
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    role = data.get("role", "student")
    
    if not email or not password or not name:
        return jsonify({"error": "Email, password, and name are required"}), 400
    
    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    engine = get_engine()
    try:
        with engine.connect() as conn:
            # Check if user exists
            result = conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": email})
            if result.fetchone():
                return jsonify({"error": "User already exists"}), 400
            
            # Insert new user
            conn.execute(text("""
                INSERT INTO users (email, password_hash, name, role) 
                VALUES (:email, :password_hash, :name, :role)
            """), {
                "email": email,
                "password_hash": password_hash,
                "name": name,
                "role": role
            })
            conn.commit()
            
            return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.post("/login")
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    engine = get_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, email, password_hash, name, role FROM users WHERE email = :email
            """), {"email": email})
            
            user = result.fetchone()
            if not user:
                return jsonify({"error": "Invalid credentials"}), 401
            
            # Verify password
            if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                return jsonify({"error": "Invalid credentials"}), 401
            
            # Create JWT token
            access_token = create_access_token(identity={
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role
            })
            
            return jsonify({
                "access_token": access_token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "role": user.role
                }
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/me")
@jwt_required()
def get_current_user():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200

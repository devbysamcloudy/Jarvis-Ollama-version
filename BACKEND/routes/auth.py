from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from db import db, bcrypt
from models import User, Preference

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Username, email and password are required"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already taken"}), 409

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409

    hashed = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user = User(
        username=data["username"],
        email=data["email"],
        password_hash=hashed,
        display_name=data.get("display_name", data["username"]),
    )
    db.session.add(user)
    db.session.flush()

    prefs = Preference(user_id=user.id)
    db.session.add(prefs)
    db.session.commit()

    token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=7))

    return jsonify({
        "message": "Account created successfully",
        "token":   token,
        "user":    user.to_dict(),
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data.get("username")).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, data.get("password", "")):
        return jsonify({"error": "Invalid username or password"}), 401

    if not user.is_active:
        return jsonify({"error": "Account is disabled"}), 403

    user.last_login = datetime.utcnow()
    db.session.commit()

    token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=7))

    return jsonify({
        "message": "Login successful",
        "token":   token,
        "user":    user.to_dict(),
    }), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": user.to_dict()}), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({"message": "Logged out successfully"}), 200
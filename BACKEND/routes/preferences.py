from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import Preference

prefs_bp = Blueprint("preferences", __name__)


@prefs_bp.route("/", methods=["GET"])
@jwt_required()
def get_prefs():
    user_id = get_jwt_identity()
    prefs = Preference.query.filter_by(user_id=user_id).first()
    if not prefs:
        return jsonify({"error": "Preferences not found"}), 404
    return jsonify({"preferences": prefs.to_dict()}), 200


@prefs_bp.route("/", methods=["PATCH"])
@jwt_required()
def update_prefs():
    user_id = get_jwt_identity()
    data = request.get_json()
    prefs = Preference.query.filter_by(user_id=user_id).first()
    if not prefs:
        return jsonify({"error": "Preferences not found"}), 404

    allowed = ["ai_model", "voice_enabled", "theme", "language", "city", "notifications_on"]
    for field in allowed:
        if field in data:
            setattr(prefs, field, data[field])

    db.session.commit()
    return jsonify({"message": "Preferences updated", "preferences": prefs.to_dict()}), 200
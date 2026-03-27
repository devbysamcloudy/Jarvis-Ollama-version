from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import Notification

notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("/", methods=["GET"])
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()
    notifs = Notification.query.filter_by(user_id=user_id)\
        .order_by(Notification.created_at.desc()).all()
    return jsonify({"notifications": [n.to_dict() for n in notifs]}), 200


@notifications_bp.route("/", methods=["POST"])
@jwt_required()
def create_notification():
    user_id = get_jwt_identity()
    data = request.get_json()
    notif = Notification(
        user_id=user_id,
        type=data.get("type", "info"),
        title=data.get("title", "Notification"),
        message=data.get("message"),
        source=data.get("source", "system"),
    )
    db.session.add(notif)
    db.session.commit()
    return jsonify({"message": "Created", "notification": notif.to_dict()}), 201


@notifications_bp.route("/<int:notif_id>/read", methods=["PATCH"])
@jwt_required()
def mark_read(notif_id):
    user_id = get_jwt_identity()
    notif = Notification.query.filter_by(id=notif_id, user_id=user_id).first()
    if not notif:
        return jsonify({"error": "Not found"}), 404
    notif.is_read = True
    db.session.commit()
    return jsonify({"message": "Marked as read"}), 200


@notifications_bp.route("/<int:notif_id>", methods=["DELETE"])
@jwt_required()
def delete_notification(notif_id):
    user_id = get_jwt_identity()
    notif = Notification.query.filter_by(id=notif_id, user_id=user_id).first()
    if not notif:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(notif)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200


@notifications_bp.route("/", methods=["DELETE"])
@jwt_required()
def clear_notifications():
    user_id = get_jwt_identity()
    Notification.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return jsonify({"message": "All cleared"}), 200
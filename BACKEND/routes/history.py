from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import CommandHistory, ChatHistory, FileAction

history_bp = Blueprint("history", __name__)


@history_bp.route("/commands", methods=["GET"])
@jwt_required()
def get_commands():
    user_id = get_jwt_identity()
    limit = request.args.get("limit", 50, type=int)
    commands = CommandHistory.query.filter_by(user_id=user_id)\
        .order_by(CommandHistory.executed_at.desc()).limit(limit).all()
    return jsonify({"commands": [c.to_dict() for c in commands]}), 200


@history_bp.route("/commands", methods=["POST"])
@jwt_required()
def save_command():
    user_id = get_jwt_identity()
    data = request.get_json()
    cmd = CommandHistory(
        user_id=user_id,
        command_text=data["command"],
        command_type=data.get("type", "general"),
        response_text=data.get("response"),
        success=data.get("success", True),
        source=data.get("source", "cli"),
    )
    db.session.add(cmd)
    db.session.commit()
    return jsonify({"message": "Saved", "command": cmd.to_dict()}), 201


@history_bp.route("/commands", methods=["DELETE"])
@jwt_required()
def clear_commands():
    user_id = get_jwt_identity()
    CommandHistory.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return jsonify({"message": "History cleared"}), 200


@history_bp.route("/chat", methods=["GET"])
@jwt_required()
def get_chat():
    user_id = get_jwt_identity()
    limit = request.args.get("limit", 50, type=int)
    chats = ChatHistory.query.filter_by(user_id=user_id)\
        .order_by(ChatHistory.sent_at.desc()).limit(limit).all()
    return jsonify({"chat": [c.to_dict() for c in chats]}), 200


@history_bp.route("/chat", methods=["POST"])
@jwt_required()
def save_chat():
    user_id = get_jwt_identity()
    data = request.get_json()
    chat = ChatHistory(
        user_id=user_id,
        mode=data.get("mode", "chat"),
        user_message=data["user_message"],
        ai_response=data.get("ai_response"),
        tokens_used=data.get("tokens_used", 0),
        model_used=data.get("model_used"),
    )
    db.session.add(chat)
    db.session.commit()
    return jsonify({"message": "Saved", "chat": chat.to_dict()}), 201


@history_bp.route("/files", methods=["GET"])
@jwt_required()
def get_file_actions():
    user_id = get_jwt_identity()
    actions = FileAction.query.filter_by(user_id=user_id)\
        .order_by(FileAction.performed_at.desc()).limit(50).all()
    return jsonify({"file_actions": [a.to_dict() for a in actions]}), 200


@history_bp.route("/files", methods=["POST"])
@jwt_required()
def save_file_action():
    user_id = get_jwt_identity()
    data = request.get_json()
    action = FileAction(
        user_id=user_id,
        action_type=data["action_type"],
        source_path=data.get("source_path"),
        dest_path=data.get("dest_path"),
        file_category=data.get("file_category"),
        source=data.get("source", "cli"),
    )
    db.session.add(action)
    db.session.commit()
    return jsonify({"message": "Saved", "action": action.to_dict()}), 201
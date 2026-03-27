from datetime import datetime
from db import db


class User(db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    display_name  = db.Column(db.String(100))
    avatar_url    = db.Column(db.String(300))
    role          = db.Column(db.String(20), default="user")
    is_active     = db.Column(db.Boolean, default=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    last_login    = db.Column(db.DateTime)

    preferences     = db.relationship("Preference", backref="user", uselist=False, cascade="all, delete")
    command_history = db.relationship("CommandHistory", backref="user", lazy=True, cascade="all, delete")
    file_actions    = db.relationship("FileAction", backref="user", lazy=True, cascade="all, delete")
    chat_history    = db.relationship("ChatHistory", backref="user", lazy=True, cascade="all, delete")
    notifications   = db.relationship("Notification", backref="user", lazy=True, cascade="all, delete")
    sessions        = db.relationship("Session", backref="user", lazy=True, cascade="all, delete")

    def to_dict(self):
        return {
            "id":           self.id,
            "username":     self.username,
            "email":        self.email,
            "display_name": self.display_name,
            "avatar_url":   self.avatar_url,
            "role":         self.role,
            "created_at":   self.created_at.isoformat(),
            "last_login":   self.last_login.isoformat() if self.last_login else None,
        }


class Preference(db.Model):
    __tablename__ = "preferences"

    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    theme            = db.Column(db.String(20), default="dark")
    language         = db.Column(db.String(10), default="en")
    city             = db.Column(db.String(100), default="Nairobi")
    ai_model         = db.Column(db.String(50), default="llama3.2:1b")
    voice_enabled    = db.Column(db.Boolean, default=False)
    notifications_on = db.Column(db.Boolean, default=True)
    updated_at       = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "theme":            self.theme,
            "language":         self.language,
            "city":             self.city,
            "ai_model":         self.ai_model,
            "voice_enabled":    self.voice_enabled,
            "notifications_on": self.notifications_on,
        }


class CommandHistory(db.Model):
    __tablename__ = "command_history"

    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    command_text  = db.Column(db.Text, nullable=False)
    command_type  = db.Column(db.String(50), default="general")
    response_text = db.Column(db.Text)
    success       = db.Column(db.Boolean, default=True)
    source        = db.Column(db.String(20), default="cli")
    executed_at   = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":          self.id,
            "command":     self.command_text,
            "type":        self.command_type,
            "response":    self.response_text,
            "success":     self.success,
            "source":      self.source,
            "executed_at": self.executed_at.isoformat(),
        }


class FileAction(db.Model):
    __tablename__ = "file_actions"

    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action_type   = db.Column(db.String(50), nullable=False)
    source_path   = db.Column(db.String(500))
    dest_path     = db.Column(db.String(500))
    file_category = db.Column(db.String(50))
    undone        = db.Column(db.Boolean, default=False)
    source        = db.Column(db.String(20), default="cli")
    performed_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":           self.id,
            "action":       self.action_type,
            "source_path":  self.source_path,
            "dest_path":    self.dest_path,
            "category":     self.file_category,
            "undone":       self.undone,
            "source":       self.source,
            "performed_at": self.performed_at.isoformat(),
        }


class ChatHistory(db.Model):
    __tablename__ = "chat_history"

    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    mode          = db.Column(db.String(20), default="chat")
    user_message  = db.Column(db.Text, nullable=False)
    ai_response   = db.Column(db.Text)
    tokens_used   = db.Column(db.Integer, default=0)
    model_used    = db.Column(db.String(50))
    sent_at       = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":           self.id,
            "mode":         self.mode,
            "user_message": self.user_message,
            "ai_response":  self.ai_response,
            "tokens_used":  self.tokens_used,
            "model_used":   self.model_used,
            "sent_at":      self.sent_at.isoformat(),
        }


class Notification(db.Model):
    __tablename__ = "notifications"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    type       = db.Column(db.String(20), default="info")
    title      = db.Column(db.String(200), nullable=False)
    message    = db.Column(db.Text)
    is_read    = db.Column(db.Boolean, default=False)
    source     = db.Column(db.String(20), default="system")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "type":       self.type,
            "title":      self.title,
            "message":    self.message,
            "is_read":    self.is_read,
            "source":     self.source,
            "created_at": self.created_at.isoformat(),
        }


class Session(db.Model):
    __tablename__ = "sessions"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    token      = db.Column(db.String(500), unique=True, nullable=False)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(200))
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
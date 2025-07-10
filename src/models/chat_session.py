"""
Database Models
Defines the database models for chat sessions and messages
"""

import uuid
from datetime import datetime
from src.database.db_manager import db

class ChatSession(db.Model):
    """Chat session model"""
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(100), nullable=False, default='anonymous')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship with messages
    messages = db.relationship('Message', backref='session', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ChatSession {self.id}>'
    
    def to_dict(self):
        """Convert session to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'last_activity': self.last_activity.isoformat(),
            'is_active': self.is_active,
            'message_count': len(self.messages) if self.messages else 0
        }
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.utcnow()
        db.session.commit()

class Message(db.Model):
    """Message model"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey('chat_sessions.id'), nullable=False)
    sender = db.Column(db.String(20), nullable=False)  # 'user' or 'bot'
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    message_type = db.Column(db.String(20), default='text')  # 'text', 'voice', 'image'
    
    # Optional fields for voice messages
    audio_file_path = db.Column(db.String(255), nullable=True)
    transcription_confidence = db.Column(db.Float, nullable=True)
    
    def __repr__(self):
        return f'<Message {self.id}: {self.sender}>'
    
    def to_dict(self):
        """Convert message to dictionary"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'sender': self.sender,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'message_type': self.message_type,
            'audio_file_path': self.audio_file_path,
            'transcription_confidence': self.transcription_confidence
        }

class UserSession(db.Model):
    """User session model for tracking user information"""
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(100), nullable=False)
    session_token = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # User preferences
    preferred_voice = db.Column(db.String(50), default='en')
    preferred_speed = db.Column(db.Float, default=1.0)
    
    def __repr__(self):
        return f'<UserSession {self.id}>'
    
    def to_dict(self):
        """Convert user session to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'is_active': self.is_active,
            'preferred_voice': self.preferred_voice,
            'preferred_speed': self.preferred_speed
        }
    
    def is_expired(self):
        """Check if session is expired"""
        return datetime.utcnow() > self.expires_at

class ChatSettings(db.Model):
    """Chat settings model"""
    __tablename__ = 'chat_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey('chat_sessions.id'), nullable=False)
    setting_key = db.Column(db.String(50), nullable=False)
    setting_value = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatSettings {self.setting_key}: {self.setting_value}>'
    
    def to_dict(self):
        """Convert setting to dictionary"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'setting_key': self.setting_key,
            'setting_value': self.setting_value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

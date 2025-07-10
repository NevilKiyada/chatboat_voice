"""
Database Manager
Handles database operations for chat sessions and messages
"""

import os
import logging
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

# Initialize SQLAlchemy
db = SQLAlchemy()

class DatabaseManager:
    """Manages database operations"""
    
    def __init__(self, app=None):
        """Initialize database manager"""
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        db.init_app(app)
        self.app = app
        logger.info("Database manager initialized")
    
    def create_session(self, user_id: Optional[str] = None):
        """Create a new chat session"""
        try:
            from src.models.chat_session import ChatSession
            
            session = ChatSession(
                user_id=user_id or 'anonymous',
                created_at=datetime.utcnow()
            )
            
            db.session.add(session)
            db.session.commit()
            
            logger.info(f"Created new chat session: {session.id}")
            return session
            
        except Exception as e:
            logger.error(f"Error creating session: {str(e)}")
            db.session.rollback()
            raise
    
    def get_session(self, session_id: str):
        """Get chat session by ID"""
        try:
            from src.models.chat_session import ChatSession
            
            session = ChatSession.query.filter_by(id=session_id).first()
            return session
            
        except Exception as e:
            logger.error(f"Error getting session {session_id}: {str(e)}")
            return None
    
    def save_message(self, session_id: str, sender: str, content: str):
        """Save a message to the database"""
        try:
            from src.models.chat_session import Message
            
            message = Message(
                session_id=session_id,
                sender=sender,
                content=content,
                timestamp=datetime.utcnow()
            )
            
            db.session.add(message)
            db.session.commit()
            
            logger.info(f"Saved message for session {session_id}: {sender}")
            return message
            
        except Exception as e:
            logger.error(f"Error saving message: {str(e)}")
            db.session.rollback()
            raise
    
    def get_session_messages(self, session_id: str):
        """Get all messages for a session"""
        try:
            from src.models.chat_session import Message
            
            messages = Message.query.filter_by(session_id=session_id).order_by(Message.timestamp).all()
            return messages
            
        except Exception as e:
            logger.error(f"Error getting messages for session {session_id}: {str(e)}")
            return []
    
    def get_recent_sessions(self, user_id: Optional[str] = None, limit: int = 10):
        """Get recent chat sessions"""
        try:
            from src.models.chat_session import ChatSession
            
            query = ChatSession.query
            
            if user_id:
                query = query.filter_by(user_id=user_id)
            
            sessions = query.order_by(ChatSession.created_at.desc()).limit(limit).all()
            return sessions
            
        except Exception as e:
            logger.error(f"Error getting recent sessions: {str(e)}")
            return []
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a chat session and its messages"""
        try:
            from src.models.chat_session import ChatSession, Message
            
            # Delete messages first
            Message.query.filter_by(session_id=session_id).delete()
            
            # Delete session
            ChatSession.query.filter_by(id=session_id).delete()
            
            db.session.commit()
            
            logger.info(f"Deleted session: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting session {session_id}: {str(e)}")
            db.session.rollback()
            return False
    
    def get_session_stats(self, session_id: str) -> dict:
        """Get statistics for a session"""
        try:
            from src.models.chat_session import Message
            
            messages = self.get_session_messages(session_id)
            
            user_messages = [m for m in messages if m.sender == 'user']
            bot_messages = [m for m in messages if m.sender == 'bot']
            
            stats = {
                'total_messages': len(messages),
                'user_messages': len(user_messages),
                'bot_messages': len(bot_messages),
                'session_duration': None,
                'average_response_time': None
            }
            
            if messages:
                # Calculate session duration
                first_message = min(messages, key=lambda m: m.timestamp)
                last_message = max(messages, key=lambda m: m.timestamp)
                duration = last_message.timestamp - first_message.timestamp
                stats['session_duration'] = duration.total_seconds()
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting session stats: {str(e)}")
            return {}
    
    def cleanup_old_sessions(self, days_old: int = 30) -> int:
        """Clean up sessions older than specified days"""
        try:
            from src.models.chat_session import ChatSession, Message
            from datetime import timedelta
            
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            
            # Get old sessions
            old_sessions = ChatSession.query.filter(ChatSession.created_at < cutoff_date).all()
            session_ids = [s.id for s in old_sessions]
            
            if not session_ids:
                return 0
            
            # Delete messages for old sessions
            Message.query.filter(Message.session_id.in_(session_ids)).delete(synchronize_session=False)
            
            # Delete old sessions
            count = ChatSession.query.filter(ChatSession.created_at < cutoff_date).delete(synchronize_session=False)
            
            db.session.commit()
            
            logger.info(f"Cleaned up {count} old sessions")
            return count
            
        except Exception as e:
            logger.error(f"Error cleaning up old sessions: {str(e)}")
            db.session.rollback()
            return 0
    
    def backup_database(self, backup_path: str) -> bool:
        """Create a backup of the database"""
        try:
            import shutil
            
            db_url = self.app.config.get('SQLALCHEMY_DATABASE_URI', '')
            
            if db_url.startswith('sqlite:///'):
                # For SQLite databases
                db_file = db_url.replace('sqlite:///', '')
                shutil.copy2(db_file, backup_path)
                logger.info(f"Database backed up to: {backup_path}")
                return True
            else:
                logger.warning("Backup only supported for SQLite databases")
                return False
                
        except Exception as e:
            logger.error(f"Error backing up database: {str(e)}")
            return False

"""
Voice Chatbot Application - Production Version
A Flask-based chatbot with voice assistance using Gemini API
Optimized for Docker deployment and production environments
"""

import os
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from datetime import datetime
import signal
import sys
from werkzeug.middleware.proxy_fix import ProxyFix

# Import custom modules
from src.api.gemini_client import GeminiClient
from src.voice.speech_processor import SpeechProcessor
from src.database.db_manager import DatabaseManager
from src.models.chat_session import ChatSession
from src.utils.logger import setup_logger

# Load environment variables
load_dotenv()

def create_app():
    """Application factory pattern for production"""
    app = Flask(__name__)
    
    # Production Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'production-secret-key-change-me')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/chatbot.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Security headers
    app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # Enable CORS with production settings
    CORS(app, origins=os.getenv('ALLOWED_ORIGINS', '*').split(','))
    
    # Proxy fix for production deployments
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
    
    # Setup logging
    logger = setup_logger()
    
    # Initialize components with error handling
    try:
        gemini_client = GeminiClient()
        speech_processor = SpeechProcessor()
        db_manager = DatabaseManager(app)
        logger.info("All components initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize components: {str(e)}")
        raise
    
    # Health check endpoint (important for Docker)
    @app.route('/health')
    def health_check():
        """Health check endpoint for Docker and load balancers"""
        try:
            # Test database connection
            from src.database.db_manager import db
            from sqlalchemy import text
            with app.app_context():
                db.session.execute(text('SELECT 1'))
            
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': os.getenv('APP_VERSION', '1.0.0'),
                'environment': os.getenv('ENVIRONMENT', 'production')
            }), 200
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return jsonify({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 503
    
    @app.route('/ready')
    def readiness_check():
        """Readiness check for Kubernetes"""
        return jsonify({'status': 'ready'}), 200
    
    @app.route('/')
    def index():
        """Main page"""
        return render_template('index.html')
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        """Handle text chat requests"""
        try:
            data = request.get_json()
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return jsonify({'error': 'Message is required'}), 400
            
            if len(user_message) > 1000:  # Input validation
                return jsonify({'error': 'Message too long (max 1000 characters)'}), 400
            
            # Get or create session
            session_id = session.get('session_id')
            if not session_id:
                chat_session = db_manager.create_session()
                session['session_id'] = chat_session.id
                session_id = chat_session.id
            
            # Save user message
            db_manager.save_message(session_id, 'user', user_message)
            
            # Get response from Gemini
            bot_response = gemini_client.get_response(user_message)
            
            # Save bot response
            db_manager.save_message(session_id, 'bot', bot_response)
            
            logger.info(f"Chat session {session_id}: User message processed")
            
            return jsonify({
                'response': bot_response,
                'session_id': session_id,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error in chat endpoint: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/voice/record', methods=['POST'])
    def record_voice():
        """Handle voice recording and transcription"""
        try:
            # Get audio data from request
            audio_file = request.files.get('audio')
            
            if not audio_file:
                return jsonify({'error': 'Audio file is required'}), 400
            
            # File size validation (10MB max)
            if len(audio_file.read()) > 10 * 1024 * 1024:
                return jsonify({'error': 'Audio file too large (max 10MB)'}), 400
            
            audio_file.seek(0)  # Reset file pointer
            
            # Save audio file temporarily with proper extension
            timestamp = datetime.now().timestamp()
            filename = audio_file.filename or 'recording.webm'
            file_ext = filename.split('.')[-1] if '.' in filename else 'webm'
            audio_path = f"audio_files/temp_{timestamp}.{file_ext}"
            
            # Ensure audio_files directory exists
            os.makedirs('audio_files', exist_ok=True)
            audio_file.save(audio_path)
            
            logger.info(f"Saved audio file: {audio_path} (size: {os.path.getsize(audio_path)} bytes)")
            
            # Transcribe audio to text
            transcribed_text = speech_processor.speech_to_text(audio_path)
            
            # Clean up temporary file
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            return jsonify({
                'transcription': transcribed_text,
                'success': True
            })
            
        except Exception as e:
            logger.error(f"Error in voice recording: {str(e)}")
            return jsonify({'error': 'Voice processing failed'}), 500
    
    @app.route('/api/voice/speak', methods=['POST'])
    def text_to_speech():
        """Convert text to speech"""
        try:
            data = request.get_json()
            text = data.get('text', '').strip()
            
            if not text:
                return jsonify({'error': 'Text is required'}), 400
            
            if len(text) > 2000:  # Input validation
                return jsonify({'error': 'Text too long (max 2000 characters)'}), 400
            
            # Generate audio file
            audio_path = speech_processor.text_to_speech(text)
            
            if audio_path:
                return jsonify({
                    'audio_url': f'/static/audio/{os.path.basename(audio_path)}',
                    'success': True
                })
            else:
                return jsonify({'error': 'Failed to generate audio'}), 500
            
        except Exception as e:
            logger.error(f"Error in text-to-speech: {str(e)}")
            return jsonify({'error': 'Text-to-speech failed'}), 500
    
    @app.route('/api/sessions/<session_id>/history')
    def get_chat_history(session_id):
        """Get chat history for a session"""
        try:
            messages = db_manager.get_session_messages(session_id)
            return jsonify({
                'messages': [
                    {
                        'sender': msg.sender,
                        'content': msg.content,
                        'timestamp': msg.timestamp.isoformat()
                    }
                    for msg in messages
                ],
                'session_id': session_id
            })
        except Exception as e:
            logger.error(f"Error getting chat history: {str(e)}")
            return jsonify({'error': 'Failed to get chat history'}), 500
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({'error': 'Request entity too large'}), 413
    
    # Security headers
    @app.after_request
    def after_request(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    return app

def signal_handler(sig, frame):
    """Graceful shutdown handler"""
    logger = logging.getLogger(__name__)
    logger.info('Received shutdown signal, gracefully shutting down...')
    sys.exit(0)

if __name__ == '__main__':
    # Setup graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    app = create_app()
    
    # Create database tables
    with app.app_context():
        try:
            from src.database.db_manager import db
            
            # Ensure instance directory exists
            instance_dir = os.path.join(os.path.dirname(__file__), 'instance')
            os.makedirs(instance_dir, exist_ok=True)
            
            db.create_all()
            print("✅ Database tables created successfully")
        except Exception as e:
            print(f"❌ Database initialization failed: {str(e)}")
            sys.exit(1)
    
    # Production configuration
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Voice Chatbot starting on http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"🌍 Environment: {os.getenv('ENVIRONMENT', 'production')}")
    
    # Run the application
    app.run(host=host, port=port, debug=debug, threaded=True)

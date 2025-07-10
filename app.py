"""
Voice Chatbot Application
A Flask-based chatbot with voice assistance using Gemini API
"""

import os
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from datetime import datetime

# Import custom modules
from src.api.gemini_client import GeminiClient
from src.voice.speech_processor import SpeechProcessor
from src.database.db_manager import DatabaseManager
from src.models.chat_session import ChatSession
from src.utils.logger import setup_logger

# Load environment variables
load_dotenv()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///chatbot.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Enable CORS
    CORS(app)
    
    # Setup logging
    logger = setup_logger()
    
    # Initialize components
    gemini_client = GeminiClient()
    speech_processor = SpeechProcessor()
    db_manager = DatabaseManager(app)
    
    @app.route('/')
    def index():
        """Main page"""
        return render_template('index.html')
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        """Handle text chat requests"""
        try:
            data = request.get_json()
            user_message = data.get('message', '')
            
            if not user_message:
                return jsonify({'error': 'Message is required'}), 400
            
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
            
            logger.info(f"Chat session {session_id}: User: {user_message[:50]}...")
            
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
            text = data.get('text', '')
            
            if not text:
                return jsonify({'error': 'Text is required'}), 400
            
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
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Create database tables
    with app.app_context():
        from src.database.db_manager import db
        db.create_all()
    
    # Run the application
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Voice Chatbot starting on http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)

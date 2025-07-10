<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Voice Chatbot Project Instructions

This is a Python Flask-based voice chatbot application with the following key components:

## Project Structure
- **Flask web application** with voice recording and text-to-speech capabilities
- **Gemini AI integration** for intelligent responses
- **SQLite database** for storing chat sessions and messages
- **Speech processing** using SpeechRecognition and gTTS libraries
- **RESTful API endpoints** for chat, voice recording, and TTS

## Key Technologies
- **Backend**: Flask, SQLAlchemy, Python
- **AI**: Google Gemini API
- **Voice**: SpeechRecognition, gTTS, PyAudio
- **Database**: SQLite (configurable for PostgreSQL/MySQL)
- **Frontend**: HTML, JavaScript (to be implemented)

## Core Modules
1. `src/api/gemini_client.py` - Handles Gemini AI API interactions
2. `src/voice/speech_processor.py` - Manages speech-to-text and text-to-speech
3. `src/database/db_manager.py` - Database operations and session management
4. `src/models/chat_session.py` - SQLAlchemy models for sessions and messages
5. `src/utils/logger.py` - Logging configuration and utilities

## Development Guidelines
- Use environment variables for API keys and configuration
- Follow Python PEP 8 style guidelines
- Implement proper error handling and logging
- Use type hints for better code documentation
- Follow RESTful API design principles

## Configuration
- Environment variables are defined in `.env` file
- Database models support SQLite, PostgreSQL, and MySQL
- Logging is configured with both file and console output
- Voice processing supports multiple TTS/STT providers

## Security Considerations
- API keys should be stored in environment variables
- Database connections should use proper authentication
- User sessions should have appropriate timeout values
- Input validation is required for all user inputs

When working on this project, prioritize:
1. **Error handling** for all external API calls
2. **Type safety** with proper type hints
3. **Logging** for debugging and monitoring
4. **Modular design** for easy testing and maintenance
5. **Configuration flexibility** for different deployment environments

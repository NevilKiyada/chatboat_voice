#!/bin/bash

# Voice Chatbot Launch Script

echo "🚀 Starting Voice Chatbot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Using default configuration."
    echo "💡 Add your Gemini API key to .env file for full functionality."
fi

# Create database tables if they don't exist
echo "📊 Setting up database..."
python -c "
from app import create_app
from src.database.db_manager import db

app = create_app()
with app.app_context():
    db.create_all()
    print('✅ Database tables created successfully!')
"

# Start the application
echo "🌐 Starting web server..."
echo "📱 Access the chatbot at: http://localhost:5000"
echo "🔄 Press Ctrl+C to stop the server"
echo ""

python app.py

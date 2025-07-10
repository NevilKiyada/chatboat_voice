#!/bin/bash
# Easy setup script for Voice Chatbot

echo "🎤 Voice Chatbot - Setup Script"
echo "=============================="

# Check Python version
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    echo "✅ Found $python_version"
else
    echo "❌ Python 3 not found! Please install Python 3.9 or later."
    exit 1
fi

# Create virtual environment
echo -e "\n📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "🔄 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo -e "\n📚 Installing dependencies..."
pip install -r requirements.txt

# Create directories if they don't exist
echo -e "\n📁 Creating required directories..."
mkdir -p audio_files static/audio logs instance

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "\n⚠️ .env file not found, creating from template..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file from example template."
        echo "⚠️ Please edit the .env file to add your Gemini API key!"
    else
        echo "CREATE YOUR OWN .env FILE WITH THE FOLLOWING CONTENT:" > .env
        echo "GEMINI_API_KEY=your_gemini_api_key_here" >> .env
        echo "SECRET_KEY=change_this_in_production" >> .env
        echo "DATABASE_URL=sqlite:///instance/chatbot.db" >> .env
        echo "FLASK_ENV=development" >> .env
        echo "DEBUG=True" >> .env
        echo "✅ Created basic .env file."
        echo "⚠️ Please edit the .env file to add your Gemini API key!"
    fi
fi

# Make start script executable
echo -e "\n🔧 Setting permissions..."
chmod +x start.sh
if [ -f "setup.sh" ]; then
    chmod +x setup.sh
fi

# Create database
echo -e "\n📊 Setting up database..."
python -c "
from app import create_app
from src.database.db_manager import db

app = create_app()
with app.app_context():
    db.create_all()
    print('✅ Database tables created successfully!')
"

echo -e "\n🎉 Setup Complete!"
echo "--------------------"
echo "To start the Voice Chatbot:"
echo "1. Make sure you've added your Gemini API key to the .env file"
echo "2. Run: ./start.sh"
echo "3. Open http://localhost:5000 in your web browser"
echo ""
echo "Enjoy your Voice Chatbot! 🤖🎤"

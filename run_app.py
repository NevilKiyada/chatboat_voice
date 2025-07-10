"""
Voice Chatbot - Simple Launch Script
This script provides a simple way to start the Voice Chatbot application.
It handles common setup steps and provides better error messages.
"""

import os
import sys

def check_dependencies():
    """Check if all required modules are installed"""
    required_modules = [
        'flask', 'google.generativeai', 'pygame', 'speech_recognition',
        'gtts', 'pyaudio', 'pydub', 'dotenv'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module.split('.')[0])
        except ImportError:
            missing_modules.append(module)
    
    return missing_modules

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ['audio_files', 'static/audio', 'logs', 'instance']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Directory structure verified")

def check_env_file():
    """Check if .env file exists and has Gemini API key"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            print("⚠️ .env file not found. Creating from example...")
            with open('.env.example', 'r', encoding='utf-8') as example_file:
                with open('.env', 'w', encoding='utf-8') as env_file:
                    env_file.write(example_file.read())
            print("✅ Created .env file")
        else:
            print("❌ .env and .env.example files not found!")
            print("   Please create a .env file with at least:")
            print("   GEMINI_API_KEY=your_key_here")
            return False
    
    # Check if API key is set
    with open('.env', 'r', encoding='utf-8') as env_file:
        content = env_file.read()
        if 'GEMINI_API_KEY=your' in content or 'GEMINI_API_KEY=' not in content:
            print("⚠️ Warning: Gemini API key not properly set in .env file")
            print("   Please edit the .env file and add your API key from https://aistudio.google.com/")
    
    return True

def main():
    """Main function to run the application"""
    print("🎤🤖 Voice Chatbot - Startup")
    print("============================")
    
    # Check for dependencies
    print("\nChecking dependencies...")
    missing_modules = check_dependencies()
    if missing_modules:
        print(f"❌ Missing modules: {', '.join(missing_modules)}")
        print("\nPlease install missing dependencies with:")
        print("pip install -r requirements.txt")
        print("\nOr try our helper script:")
        print("python install_dependencies.py")
        return
    
    # Check directory structure
    print("\nChecking directory structure...")
    create_directories()
    
    # Check .env file
    print("\nChecking environment configuration...")
    if not check_env_file():
        return
    
    # Start the application
    print("\n✅ All checks passed. Starting the application...")
    print("📱 Access the chatbot at: http://localhost:5000")
    print("🔄 Press Ctrl+C to stop the server\n")
    
    try:
        # Import and run the Flask app
        from app import create_app
        
        app = create_app()
        
        # Create database tables
        with app.app_context():
            from src.database.db_manager import db
            db.create_all()
            print("✅ Database tables created successfully!")
        
        # Get configuration from environment or use defaults
        host = os.environ.get('HOST', '0.0.0.0')
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('DEBUG', 'True').lower() == 'true'
        
        # Run the Flask application
        app.run(host=host, port=port, debug=debug)
        
    except Exception as e:
        print(f"❌ Error starting application: {str(e)}")
        print("\nPlease check the TROUBLESHOOTING.md file for solutions.")

if __name__ == "__main__":
    main()

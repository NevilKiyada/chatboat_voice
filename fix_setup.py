"""
Voice Chatbot Project - Fix Common Issues Script
This script automatically fixes common issues with the voice chatbot setup
"""

import os
import sys
import shutil
from pathlib import Path

def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        'instance',
        'logs',
        'audio_files',
        'static/audio'
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"Creating directory: {dir_path}")
            dir_path.mkdir(parents=True, exist_ok=True)
    
    print("✓ All required directories created")

def create_env_file():
    """Create or update .env file if it doesn't exist"""
    env_path = Path(".env")
    if not env_path.exists():
        print("Creating .env file with default settings")
        with open(env_path, 'w') as f:
            f.write("""# Voice Chatbot Environment Configuration

# Flask Configuration
SECRET_KEY=your-secret-key-here
HOST=0.0.0.0
PORT=5000
DEBUG=True

# Database Configuration (SQLite is default for development)
DATABASE_URL=sqlite:///instance/chatbot.db

# Gemini API Configuration
GEMINI_API_KEY=your-gemini-api-key-here

# Audio Configuration
SAMPLE_RATE=16000
CHUNK_SIZE=1024
AUDIO_FORMAT=wav

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/chatbot.log

# Voice Processing
# Set to 'dummy' to use dummy audio driver if ALSA issues persist
SDL_AUDIODRIVER=dummy
""")
        print("✓ Created .env file")
    else:
        print("✓ .env file already exists")

def fix_permissions():
    """Fix permissions for key directories"""
    directories = [
        'instance',
        'logs',
        'audio_files',
        'static/audio'
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if dir_path.exists():
            try:
                # Make directory writable
                dir_path.chmod(0o755)
                print(f"✓ Set permissions for {dir_path}")
            except Exception as e:
                print(f"! Failed to set permissions for {dir_path}: {e}")

def create_empty_database():
    """Create an empty SQLite database file"""
    try:
        import sqlite3
        db_path = Path("instance/chatbot.db")
        
        # Create empty database file if it doesn't exist
        if not db_path.exists():
            conn = sqlite3.connect(str(db_path))
            conn.close()
            print(f"✓ Created empty database file at {db_path}")
        else:
            print(f"✓ Database file already exists at {db_path}")
    except Exception as e:
        print(f"! Failed to create database file: {e}")

def test_database_connection():
    """Test database connection"""
    try:
        import sqlite3
        db_path = Path("instance/chatbot.db")
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()
        conn.close()
        
        print(f"✓ Database connection successful (SQLite version: {version[0]})")
        return True
    except Exception as e:
        print(f"! Database connection failed: {e}")
        return False

def main():
    """Main function to fix common issues"""
    print("=== Voice Chatbot Setup Helper ===")
    print("Fixing common setup issues...")
    
    # Fix directory structure
    ensure_directories()
    
    # Fix environment file
    create_env_file()
    
    # Fix permissions
    fix_permissions()
    
    # Fix database
    create_empty_database()
    test_database_connection()
    
    print("\nSetup complete. Try running app.py again.")
    print("\nIf you're still experiencing issues with ALSA audio:")
    print("- Run with: SDL_AUDIODRIVER=dummy python app.py")
    print("- Or edit .env to set SDL_AUDIODRIVER=dummy")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

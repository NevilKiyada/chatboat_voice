"""
Voice Chatbot - Dependency Installer Helper
Run this script if you have trouble installing dependencies with requirements.txt

Usage:
    python install_dependencies.py
"""

import subprocess
import sys
import os
import time

def run_command(command):
    """Run a command and return its output"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True, check=False)
    if result.returncode == 0:
        print("✅ Success!")
        return True
    else:
        print(f"❌ Error: {result.stderr}")
        return False

def main():
    print("Voice Chatbot - Dependency Installer")
    print("====================================")
    
    # Core dependencies
    dependencies = [
        "pip install --upgrade pip",
        "pip install Flask==2.3.3",
        "pip install Flask-CORS==4.0.0",
        "pip install Flask-SQLAlchemy==3.0.5",
        "pip install Werkzeug==2.3.7",
        "pip install google-generativeai==0.3.2",
        "pip install SpeechRecognition==3.10.0",
        "pip install gtts==2.4.0",
        "pip install pydub==0.25.1",
        "pip install SQLAlchemy==2.0.23",
        "pip install python-dotenv==1.0.0",
        "pip install requests==2.31.0",
        "pip install colorlog==6.7.0",
        "pip install pygame==2.5.2",
    ]
    
    # Try to install PyAudio directly first
    print("\nTrying to install PyAudio...")
    if not run_command("pip install PyAudio==0.2.14"):
        # If direct installation fails, try platform-specific approaches
        if sys.platform.startswith('linux'):
            print("\nTrying Linux-specific PyAudio installation...")
            print("Note: You may need to enter your password for sudo commands")
            run_command("sudo apt-get update")
            run_command("sudo apt-get install -y portaudio19-dev python3-pyaudio")
            run_command("pip install PyAudio==0.2.14")
        elif sys.platform == 'darwin':  # macOS
            print("\nTrying macOS-specific PyAudio installation...")
            print("Note: This requires Homebrew. If you don't have it, please install it first.")
            run_command("brew install portaudio")
            run_command("pip install PyAudio==0.2.14")
        elif sys.platform == 'win32':  # Windows
            print("\nTrying Windows-specific PyAudio installation...")
            run_command("pip install pipwin")
            run_command("pipwin install pyaudio")
    
    # Install each dependency one by one
    success_count = 0
    for dep in dependencies:
        if run_command(dep):
            success_count += 1
        time.sleep(0.5)  # Small delay between installations
    
    # Create necessary directories
    print("\nCreating necessary directories...")
    os.makedirs("audio_files", exist_ok=True)
    os.makedirs("static/audio", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("instance", exist_ok=True)
    
    # Create .env file if it doesn't exist
    if not os.path.exists(".env") and os.path.exists(".env.example"):
        print("\nCreating .env file from example...")
        with open(".env.example", "r", encoding="utf-8") as example_file:
            with open(".env", "w", encoding="utf-8") as env_file:
                env_file.write(example_file.read())
        print("✅ Created .env file. Remember to add your Gemini API key!")
    
    # Summary
    print("\n====================================")
    print(f"Successfully installed {success_count} out of {len(dependencies)} packages")
    print("If you encountered any errors, check the TROUBLESHOOTING.md file")
    print("\nTo run the Voice Chatbot:")
    print("1. Make sure you've added your Gemini API key to the .env file")
    print("2. Run: python app.py")
    print("3. Open http://localhost:5000 in your web browser")

if __name__ == "__main__":
    main()

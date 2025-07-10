#!/usr/bin/env python3
"""
Voice Chatbot - Setup Validation Script
Tests that all components are ready for Docker deployment
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and print result"""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def check_environment():
    """Check environment configuration"""
    print("\n🔧 Checking Environment Configuration...")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_example.exists():
        print("❌ .env.example file missing")
        return False
    
    if not env_file.exists():
        print("⚠️  .env file not found - will be created during setup")
    else:
        print("✅ .env file exists")
        
        # Check if API key is set
        with open('.env', 'r') as f:
            content = f.read()
            if 'your_gemini_api_key_here' in content:
                print("⚠️  GEMINI_API_KEY still has placeholder value")
            elif 'GEMINI_API_KEY=' in content and len(content.split('GEMINI_API_KEY=')[1].split('\n')[0].strip()) > 10:
                print("✅ GEMINI_API_KEY appears to be set")
            else:
                print("⚠️  GEMINI_API_KEY may not be properly configured")
    
    return True

# Docker configuration check has been removed

def check_source_code():
    """Check source code structure"""
    print("\n🧠 Checking Source Code...")
    
    files = [
        ('app.py', 'Main Flask application'),
        ('requirements.txt', 'Python dependencies'),
        ('src/api/gemini_client.py', 'Gemini AI client'),
        ('src/voice/speech_processor.py', 'Voice processing'),
        ('src/database/db_manager.py', 'Database manager'),
        ('src/utils/logger.py', 'Logging utilities'),
        ('templates/index.html', 'Web interface template')
    ]
    
    all_good = True
    for file_path, description in files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    return all_good

def check_directories():
    """Check required directories"""
    print("\n📁 Checking Directory Structure...")
    
    directories = [
        'src/',
        'src/api/',
        'src/voice/',
        'src/database/',
        'src/utils/',
        'src/models/',
        'templates/',
        'static/'
    ]
    
    all_good = True
    for directory in directories:
        if Path(directory).exists():
            print(f"✅ Directory exists: {directory}")
        else:
            print(f"❌ Directory missing: {directory}")
            all_good = False
    
    return all_good

def check_scripts_executable():
    """Check if scripts are executable"""
    print("\n🔧 Checking Script Permissions...")
    
    scripts = ['start.sh']
    
    for script in scripts:
        if Path(script).exists():
            if os.access(script, os.X_OK):
                print(f"✅ {script} is executable")
            else:
                print(f"⚠️  {script} is not executable (run: chmod +x {script})")
        else:
            print(f"❌ {script} not found")

def test_imports():
    """Test that all imports work"""
    print("\n🐍 Testing Python Imports...")
    
    # Add src to path
    sys.path.insert(0, 'src')
    
    modules = [
        ('api.gemini_client', 'GeminiClient'),
        ('voice.speech_processor', 'SpeechProcessor'),
        ('database.db_manager', 'DatabaseManager'),
        ('utils.logger', 'setup_logger')
    ]
    
    all_good = True
    for module_name, class_name in modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"✅ {module_name}.{class_name}")
        except ImportError as e:
            print(f"❌ {module_name}.{class_name} - Import Error: {e}")
            all_good = False
        except AttributeError as e:
            print(f"❌ {module_name}.{class_name} - Attribute Error: {e}")
            all_good = False
        except Exception as e:
            print(f"❌ {module_name}.{class_name} - Error: {e}")
            all_good = False
    
    return all_good

def main():
    """Main validation function"""
    print("🎤 Voice Chatbot - Setup Validation")
    print("=" * 50)
    
    checks = [
        check_environment(),
        check_source_code(),
        check_directories(),
        test_imports()
    ]
    
    check_scripts_executable()
    
    print("\n" + "=" * 50)
    
    if all(checks):
        print("🎉 ALL CHECKS PASSED!")
        print("")
        print("Your Voice Chatbot is ready for:")
        print("✅ Sharing with others")
        print("✅ Local deployment")
        print("")
        print("Next steps:")
        print("1. Run: python app.py")
        print("2. Access the chatbot at http://localhost:5000")
        print("")
        return True
    else:
        print("❌ Some checks failed!")
        print("")
        print("Please fix the issues above before proceeding.")
        print("Run this script again after making fixes.")
        print("")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

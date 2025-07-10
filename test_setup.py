#!/usr/bin/env python3
"""
Test script to verify the voice chatbot setup
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment configuration"""
    print("🔧 Testing Environment Configuration...")
    
    # Load environment variables
    load_dotenv()
    
    # Check required environment variables
    required_vars = ['GEMINI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("💡 Please add them to your .env file")
        return False
    
    print("✅ Environment configuration looks good!")
    return True

def test_imports():
    """Test that all required packages can be imported"""
    print("\n📦 Testing Package Imports...")
    
    packages = [
        ('flask', 'Flask'),
        ('google.generativeai', 'Gemini AI'),
        ('speech_recognition', 'Speech Recognition'),
        ('gtts', 'Google Text-to-Speech'),
        ('flask_sqlalchemy', 'Flask SQLAlchemy'),
        ('dotenv', 'Python Dotenv'),
        ('colorlog', 'Colorlog'),
    ]
    
    failed_imports = []
    
    for package, name in packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: {str(e)}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("💡 Try running: pip install -r requirements.txt")
        return False
    
    print("✅ All packages imported successfully!")
    return True

def test_modules():
    """Test that custom modules can be imported"""
    print("\n🔧 Testing Custom Modules...")
    
    # Add the project root to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    modules = [
        ('src.utils.logger', 'Logger Utility'),
        ('src.api.gemini_client', 'Gemini Client'),
        ('src.voice.speech_processor', 'Speech Processor'),
        ('src.database.db_manager', 'Database Manager'),
        ('src.models.chat_session', 'Chat Models'),
    ]
    
    failed_modules = []
    
    for module, name in modules:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: {str(e)}")
            failed_modules.append(module)
    
    if failed_modules:
        print(f"\n❌ Failed to import modules: {', '.join(failed_modules)}")
        return False
    
    print("✅ All custom modules imported successfully!")
    return True

def main():
    """Run all tests"""
    print("🚀 Voice Chatbot Setup Test\n")
    
    tests = [
        test_environment,
        test_imports,
        test_modules,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Setup looks good! You can now run the chatbot with: python app.py")
        print("🌐 Access the web interface at: http://localhost:5000")
        print("\n📝 Next steps:")
        print("1. Add your Gemini API key to the .env file")
        print("2. Run 'python app.py' to start the application")
        print("3. Open http://localhost:5000 in your browser")
    else:
        print("❌ Some tests failed. Please fix the issues above before running the chatbot.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

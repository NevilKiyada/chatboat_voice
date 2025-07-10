#!/usr/bin/env python3
"""
Voice Chat Diagnostic Tool
Tests the entire voice chat pipeline
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.voice.speech_processor import SpeechProcessor
from src.api.gemini_client import GeminiClient
import tempfile
import wave

def create_test_audio_with_speech():
    """Create a test audio file with actual speech content"""
    print("🎵 Creating test audio with speech...")
    
    # Initialize speech processor
    processor = SpeechProcessor()
    
    # Generate some speech audio using TTS
    test_text = "hello good morning"
    audio_path = processor.text_to_speech(test_text)
    
    if audio_path:
        print(f"✅ Generated test audio: {audio_path}")
        return audio_path
    else:
        print("❌ Failed to generate test audio")
        return None

def test_speech_recognition(audio_path):
    """Test speech recognition on an audio file"""
    print(f"\n🎤 Testing speech recognition on: {audio_path}")
    
    processor = SpeechProcessor()
    
    # Test transcription
    transcription = processor.speech_to_text(audio_path)
    
    if transcription:
        print(f"✅ Transcription successful: '{transcription}'")
        return transcription
    else:
        print("❌ Transcription failed")
        return None

def test_gemini_chat(message):
    """Test Gemini AI chat"""
    print(f"\n💬 Testing Gemini chat with: '{message}'")
    
    try:
        client = GeminiClient()
        response = client.get_response(message)
        
        if response:
            print(f"✅ Gemini response: '{response[:100]}...'")
            return response
        else:
            print("❌ Gemini response failed")
            return None
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return None

def main():
    """Run the complete diagnostic"""
    print("🔧 Voice Chat Diagnostic Tool")
    print("=" * 50)
    
    # Step 1: Create test audio
    audio_path = create_test_audio_with_speech()
    if not audio_path:
        print("Stopping - could not create test audio")
        return
    
    # Step 2: Test speech recognition
    transcription = test_speech_recognition(audio_path)
    if not transcription:
        print("Stopping - speech recognition failed")
        return
    
    # Step 3: Test Gemini chat
    response = test_gemini_chat(transcription)
    if not response:
        print("Stopping - Gemini chat failed")
        return
    
    print("\n" + "=" * 50)
    print("🎉 Complete voice chat pipeline test successful!")
    print(f"Input: '{transcription}' → Output: '{response[:100]}...'")
    
    # Step 4: Test with the exact phrase from the user
    print("\n🎯 Testing with user's exact phrase...")
    user_phrase = "hello good morning"
    user_response = test_gemini_chat(user_phrase)
    
    if user_response:
        print(f"✅ User phrase test successful!")
        print(f"'{user_phrase}' → '{user_response[:100]}...'")
    else:
        print("❌ User phrase test failed")

if __name__ == "__main__":
    main()

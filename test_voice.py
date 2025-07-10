#!/usr/bin/env python3
"""
Simple voice test script to debug voice recognition issues
"""

import os
import sys
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.voice.speech_processor import SpeechProcessor
from src.utils.logger import setup_logger

def main():
    print("🎤 Voice Recognition Test")
    print("=" * 50)
    
    # Setup logging
    logger = setup_logger()
    
    # Initialize speech processor
    try:
        processor = SpeechProcessor()
        print("✅ Speech processor initialized")
    except Exception as e:
        print(f"❌ Failed to initialize speech processor: {e}")
        return False
    
    # Check microphone availability
    print(f"🎤 Microphone available: {processor.is_microphone_available()}")
    
    # Test text-to-speech
    print("\n🗣️ Testing Text-to-Speech...")
    try:
        audio_path = processor.text_to_speech("Hello, this is a test.")
        if audio_path:
            print(f"✅ TTS audio generated: {audio_path}")
        else:
            print("❌ TTS failed")
    except Exception as e:
        print(f"❌ TTS error: {e}")
    
    # Test speech recognition with a simple file
    print("\n🎧 Testing Speech Recognition...")
    
    # Create a simple test scenario
    test_text = "Hello good morning"
    print(f"📝 Test phrase: '{test_text}'")
    
    # Generate audio for testing
    try:
        test_audio_path = processor.text_to_speech(test_text)
        if test_audio_path:
            print(f"📁 Generated test audio: {test_audio_path}")
            
            # Try to transcribe it back
            transcription = processor.speech_to_text(test_audio_path)
            if transcription:
                print(f"✅ Transcription: '{transcription}'")
                
                # Check similarity
                if test_text.lower() in transcription.lower() or transcription.lower() in test_text.lower():
                    print("🎉 Transcription matches expected text!")
                else:
                    print("⚠️ Transcription doesn't match exactly, but recognition is working")
            else:
                print("❌ Transcription failed")
        else:
            print("❌ Could not generate test audio")
    except Exception as e:
        print(f"❌ Speech recognition test error: {e}")
    
    print("\n" + "=" * 50)
    print("Voice test completed.")

if __name__ == '__main__':
    main()

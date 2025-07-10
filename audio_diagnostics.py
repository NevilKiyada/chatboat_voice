#!/usr/bin/env python3
"""
Audio System Diagnostic Script
Diagnoses audio-related issues and provides fixes for voice chatbot
"""

import os
import sys
import subprocess
import platform
import tempfile

def print_system_info():
    """Print system information"""
    print("=== System Information ===")
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    print(f"OS: {platform.system()}")
    print(f"OS Version: {platform.version()}")
    
    # Check for audio devices
    print("\n=== Audio Devices ===")
    try:
        if platform.system() == 'Linux':
            # Check for ALSA devices
            subprocess.run(['arecord', '-l'], check=False)
            subprocess.run(['aplay', '-l'], check=False)
    except FileNotFoundError:
        print("ALSA tools not found")

def check_audio_libraries():
    """Check for required audio libraries"""
    print("\n=== Audio Libraries ===")
    
    # Check PyAudio
    try:
        import pyaudio
        print(f"PyAudio version: {pyaudio.__version__}")
        
        # Try to initialize PyAudio
        try:
            pa = pyaudio.PyAudio()
            
            # Count devices
            device_count = pa.get_device_count()
            print(f"Audio devices found: {device_count}")
            
            # List devices
            if device_count > 0:
                print("\nAvailable audio devices:")
                for i in range(device_count):
                    try:
                        device_info = pa.get_device_info_by_index(i)
                        print(f"  Device {i}: {device_info['name']}")
                        print(f"    Input channels: {device_info['maxInputChannels']}")
                        print(f"    Output channels: {device_info['maxOutputChannels']}")
                        print(f"    Default sample rate: {device_info['defaultSampleRate']}")
                    except Exception as e:
                        print(f"  Device {i}: Error getting info: {e}")
            
            pa.terminate()
        except Exception as e:
            print(f"Error initializing PyAudio: {e}")
    except ImportError:
        print("PyAudio not installed")
    
    # Check SpeechRecognition
    try:
        import speech_recognition
        print(f"SpeechRecognition version: {speech_recognition.__version__}")
        
        # Try to list microphones
        try:
            recognizer = speech_recognition.Recognizer()
            microphones = speech_recognition.Microphone.list_microphone_names()
            
            print(f"Microphones found: {len(microphones)}")
            for i, mic in enumerate(microphones):
                print(f"  Microphone {i}: {mic}")
                
        except Exception as e:
            print(f"Error listing microphones: {e}")
    except ImportError:
        print("SpeechRecognition not installed")
    
    # Check pygame
    try:
        import pygame
        print(f"Pygame version: {pygame.ver}")
        
        # Try to initialize pygame mixer
        try:
            pygame.mixer.init()
            print("Pygame mixer initialized successfully")
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error initializing pygame mixer: {e}")
    except ImportError:
        print("Pygame not installed")

def test_text_to_speech():
    """Test text-to-speech functionality"""
    print("\n=== Testing Text-to-Speech ===")
    
    try:
        from gtts import gTTS
        
        # Create a temporary audio file
        test_text = "This is a test of the text-to-speech system."
        temp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        temp_file.close()
        
        print(f"Creating test audio file: {temp_file.name}")
        tts = gTTS(text=test_text, lang='en', slow=False)
        tts.save(temp_file.name)
        
        print(f"✓ Text-to-speech test successful")
        print(f"  Audio file created at: {temp_file.name}")
        print(f"  You can play it manually to verify TTS works")
        
        # Try to play with pygame
        try:
            import pygame
            print("Attempting to play audio with pygame...")
            
            pygame.mixer.init()
            pygame.mixer.music.load(temp_file.name)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            import time
            time.sleep(3)
            pygame.mixer.quit()
            
            print("✓ Audio playback test successful")
        except Exception as e:
            print(f"Audio playback test failed: {e}")
            print("This is normal if you're using the dummy audio driver")
            
        # Clean up
        os.unlink(temp_file.name)
        
    except ImportError:
        print("gTTS not installed")
    except Exception as e:
        print(f"Text-to-speech test failed: {e}")

def suggest_fixes():
    """Suggest fixes for common audio issues"""
    print("\n=== Recommended Fixes ===")
    
    print("1. Use the dummy audio driver:")
    print("   SDL_AUDIODRIVER=dummy python app.py")
    print()
    
    print("2. Install ALSA utilities:")
    print("   sudo apt-get update && sudo apt-get install -y alsa-utils libasound2-dev")
    print()
    
    print("3. Install PyAudio dependencies:")
    print("   sudo apt-get install -y portaudio19-dev python3-pyaudio")
    print()
    
    print("4. Add the following to your .env file:")
    print("   SDL_AUDIODRIVER=dummy")
    print()
    
    print("5. Use our fixed script:")
    print("   ./fix_and_run.sh")
    print()
    
    print("6. Check your microphone is properly connected and recognized by your system")

def main():
    """Run all diagnostics"""
    print("======================================")
    print("🎤 Voice Chatbot Audio Diagnostics 🔊")
    print("======================================")
    
    print_system_info()
    check_audio_libraries()
    test_text_to_speech()
    suggest_fixes()
    
    print("\nDiagnostic complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())

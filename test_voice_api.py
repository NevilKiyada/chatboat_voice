#!/usr/bin/env python3
"""
Test script to verify voice API functionality
"""
import requests
import json
from pathlib import Path
import tempfile
import wave
import os

def test_voice_api():
    """Test the voice recording API endpoint"""
    base_url = "http://127.0.0.1:5000"
    
    print("🎯 Testing Voice API")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server is not responding")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Server connection failed: {e}")
        return
    
    # Test 2: Create a simple test audio file
    print("\n🎤 Creating test audio file...")
    try:
        # Create a simple WAV file with silence for testing
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            # Create a simple 1-second mono WAV file with silence
            with wave.open(tmp_file.name, 'wb') as wav_file:
                wav_file.setnchannels(1)  # mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(16000)  # 16kHz
                
                # Create 1 second of silence
                silence = b'\x00\x00' * 16000  # 16000 samples of silence
                wav_file.writeframes(silence)
            
            test_audio_path = tmp_file.name
            print(f"✅ Test audio file created: {test_audio_path}")
    except Exception as e:
        print(f"❌ Failed to create test audio: {e}")
        return
    
    # Test 3: Test voice recording endpoint
    print("\n🔊 Testing voice recording endpoint...")
    try:
        with open(test_audio_path, 'rb') as audio_file:
            files = {'audio': ('test.wav', audio_file, 'audio/wav')}
            response = requests.post(f"{base_url}/api/voice/record", files=files, timeout=30)
        
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                transcription = data.get('transcription', '')
                print(f"✅ Voice API working! Transcription: '{transcription}'")
                if transcription:
                    print("🎉 Speech recognition is working")
                else:
                    print("⚠️ No transcription returned (silence detected)")
            else:
                print("⚠️ API returned success=False")
        else:
            print(f"❌ Voice API failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Voice API test failed: {e}")
    finally:
        # Clean up test file
        try:
            os.unlink(test_audio_path)
        except:
            pass
    
    # Test 4: Test text chat endpoint
    print("\n💬 Testing text chat endpoint...")
    try:
        data = {'message': 'Hello, this is a test message'}
        response = requests.post(
            f"{base_url}/api/chat",
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            chat_response = response.json()
            bot_reply = chat_response.get('response', '')
            print(f"✅ Chat API working! Bot response: '{bot_reply[:100]}...'")
        else:
            print(f"❌ Chat API failed: {response.text}")
    except Exception as e:
        print(f"❌ Chat API test failed: {e}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

def test_with_real_audio():
    """Test with the generated TTS audio files"""
    base_url = "http://127.0.0.1:5000"
    
    print("\n🎵 Testing with real audio files...")
    
    # Look for existing TTS audio files
    audio_dir = Path("static/audio")
    if audio_dir.exists():
        audio_files = list(audio_dir.glob("*.mp3"))
        if audio_files:
            test_file = audio_files[0]
            print(f"Using audio file: {test_file}")
            
            try:
                with open(test_file, 'rb') as audio_file:
                    files = {'audio': ('test.mp3', audio_file, 'audio/mp3')}
                    response = requests.post(f"{base_url}/api/voice/record", files=files, timeout=30)
                
                print(f"Status code: {response.status_code}")
                print(f"Response: {response.text}")
                
                if response.status_code == 200:
                    data = response.json()
                    transcription = data.get('transcription', '')
                    print(f"✅ Real audio test! Transcription: '{transcription}'")
                else:
                    print(f"❌ Real audio test failed")
            except Exception as e:
                print(f"❌ Real audio test error: {e}")
        else:
            print("No audio files found in static/audio")
    else:
        print("static/audio directory not found")

if __name__ == "__main__":
    test_voice_api()
    test_with_real_audio()

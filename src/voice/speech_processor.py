"""
Speech Processing Module
Handles speech-to-text and text-to-speech functionality
"""

import os
import speech_recognition as sr
from gtts import gTTS
import pygame
from pydub import AudioSegment
import tempfile
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

class SpeechProcessor:
    """Handles speech recognition and text-to-speech conversion"""
    
    def __init__(self):
        """Initialize the speech processor"""
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.microphone_available = False
        
        # Audio configuration
        self.sample_rate = int(os.getenv('SAMPLE_RATE', 16000))
        self.chunk_size = int(os.getenv('CHUNK_SIZE', 1024))
        self.audio_format = os.getenv('AUDIO_FORMAT', 'wav')
        
        # Set environment variable to disable ALSA error messages
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        
        # Try to initialize microphone (optional for voice features)
        try:
            # List available microphones before attempting to use them
            available_mics = sr.Microphone.list_microphone_names()
            logger.info(f"Available microphones: {available_mics}")
            
            if available_mics:
                self.microphone = sr.Microphone()
                self.microphone_available = True
                logger.info("Microphone initialized successfully")
            else:
                logger.warning("No microphones detected")
        except Exception as e:
            logger.warning(f"Microphone initialization error: {str(e)}")
            logger.info("Voice recording disabled - text-to-speech still available")
        
        # Initialize pygame mixer for audio playback with explicit fallback options
        try:
            # Try different driver options if available
            try:
                pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=1)
                logger.info("Pygame mixer initialized with default driver")
            except:
                # Try with dummy driver if normal initialization fails
                os.environ['SDL_AUDIODRIVER'] = 'dummy'
                pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=1)
                logger.info("Pygame mixer initialized with dummy driver")
        except Exception as e:
            logger.warning(f"Audio playback initialization failed: {str(e)}")
            logger.info("Text-to-speech audio playback may not work properly")
        
        # Calibrate microphone if available
        if self.microphone_available:
            self._calibrate_microphone()
        
        logger.info("Speech processor initialized")
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        if not self.microphone_available or not self.microphone:
            logger.warning("Microphone not available for calibration")
            return
            
        try:
            with self.microphone as source:
                logger.info("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Microphone calibration completed")
        except Exception as e:
            logger.warning(f"Microphone calibration failed: {str(e)}")
    
    def speech_to_text(self, audio_file_path: Optional[str] = None, timeout: int = 10) -> Optional[str]:
        """
        Convert speech to text
        
        Args:
            audio_file_path: Path to audio file (if None, records from microphone)
            timeout: Recording timeout in seconds
            
        Returns:
            Transcribed text or None if failed
        """
        try:
            if audio_file_path:
                # Process uploaded audio file
                return self._transcribe_audio_file(audio_file_path)
            else:
                # Record from microphone
                return self._record_and_transcribe(timeout)
                
        except Exception as e:
            logger.error(f"Speech-to-text error: {str(e)}")
            return None
    
    def _transcribe_audio_file(self, audio_file_path: str) -> Optional[str]:
        """Transcribe an audio file"""
        try:
            logger.info(f"Transcribing audio file: {audio_file_path}")
            
            # Convert audio to supported format if needed
            try:
                # Try to load the audio file
                audio_segment = AudioSegment.from_file(audio_file_path)
            except Exception as e:
                logger.warning(f"Failed to load with pydub: {str(e)}, trying direct WAV")
                # If pydub fails, try direct processing for WAV files
                if audio_file_path.endswith('.wav'):
                    return self._transcribe_wav_directly(audio_file_path)
                else:
                    raise e
            
            # Convert to wav format for speech recognition
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                # Export with specific parameters for better recognition
                audio_segment.export(
                    temp_file.name, 
                    format="wav", 
                    parameters=[
                        "-ar", "16000",  # 16kHz sample rate
                        "-ac", "1",      # Mono channel
                        "-acodec", "pcm_s16le"  # 16-bit PCM
                    ]
                )
                
                # Transcribe the audio
                transcription = self._transcribe_wav_directly(temp_file.name)
                
                # Clean up temp file
                os.unlink(temp_file.name)
                
                return transcription
                
        except Exception as e:
            logger.error(f"Audio transcription error: {str(e)}")
            return None
    
    def _transcribe_wav_directly(self, wav_path: str) -> Optional[str]:
        """Transcribe a WAV file directly using speech recognition"""
        try:
            with sr.AudioFile(wav_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Record the audio
                audio_data = self.recognizer.record(source)
                
                # Try multiple recognition services for better reliability
                recognition_services = [
                    ("Google (default)", lambda: self.recognizer.recognize_google(audio_data)),
                    ("Google (en-US)", lambda: self.recognizer.recognize_google(audio_data, language='en-US')),
                    ("Google (en-GB)", lambda: self.recognizer.recognize_google(audio_data, language='en-GB')),
                ]
                
                for service_name, service_func in recognition_services:
                    try:
                        text = service_func()
                        # Make sure text is a string
                        if text is not None and isinstance(text, str) and text.strip():
                            logger.info(f"Successfully transcribed with {service_name}: {text}")
                            return text.strip()
                        elif text is not None:
                            # Handle case where text is not a string but can be converted to one
                            text_str = str(text)
                            if text_str.strip():
                                logger.info(f"Successfully transcribed with {service_name}: {text_str}")
                                return text_str.strip()
                    except sr.UnknownValueError:
                        logger.warning(f"{service_name} could not understand audio")
                        continue
                    except sr.RequestError as e:
                        logger.warning(f"{service_name} service error: {str(e)}")
                        continue
                    except AttributeError as e:
                        logger.warning(f"{service_name} returned non-string that can't be processed: {e}")
                        continue
                
                # If all services failed
                logger.error("All speech recognition services failed to transcribe")
                return None
                
        except Exception as e:
            logger.error(f"Direct WAV transcription error: {str(e)}")
            return None
    
    def _record_and_transcribe(self, timeout: int) -> Optional[str]:
        """Record audio from microphone and transcribe"""
        if not self.microphone_available or not self.microphone:
            logger.error("Microphone not available for recording")
            return None
            
        try:
            with self.microphone as source:
                logger.info(f"Recording audio for {timeout} seconds...")
                audio_data = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=timeout)
                
            logger.info("Processing audio...")
            text = self.recognizer.recognize_google(audio_data)
            
            # Ensure text is a string type
            if isinstance(text, str):
                logger.info(f"Transcribed: {text[:50]}...")
                return text
            else:
                logger.warning(f"Received non-string response: {type(text)}")
                # Convert to string if possible
                return str(text) if text is not None else None
            
        except sr.WaitTimeoutError:
            logger.warning("Recording timeout")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Recording error: {str(e)}")
            return None
    
    def text_to_speech(self, text: str, lang: str = 'en', slow: bool = False) -> Optional[str]:
        """
        Convert text to speech
        
        Args:
            text: Text to convert
            lang: Language code
            slow: Whether to speak slowly
            
        Returns:
            Path to generated audio file
        """
        try:
            if not text.strip():
                logger.warning("Empty text provided for TTS")
                return None
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            audio_filename = f"tts_output_{timestamp}.mp3"
            audio_path = os.path.join("static", "audio", audio_filename)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            
            # Generate speech
            tts = gTTS(text=text, lang=lang, slow=slow)
            tts.save(audio_path)
            
            logger.info(f"Generated TTS audio: {audio_path}")
            return audio_path
            
        except Exception as e:
            logger.error(f"Text-to-speech error: {str(e)}")
            return None
    
    def play_audio(self, audio_path: str):
        """Play audio file"""
        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
                
            logger.info(f"Played audio: {audio_path}")
            
        except Exception as e:
            logger.error(f"Audio playback error: {str(e)}")
    
    def is_microphone_available(self) -> bool:
        """Check if microphone is available"""
        if not self.microphone_available or not self.microphone:
            return False
            
        try:
            with self.microphone as source:
                pass
            return True
        except Exception as e:
            logger.error(f"Microphone not available: {str(e)}")
            return False
    
    def get_available_microphones(self) -> list:
        """Get list of available microphones"""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            logger.info(f"Available microphones: {mic_list}")
            return mic_list
        except Exception as e:
            logger.error(f"Error getting microphone list: {str(e)}")
            return []
    
    def set_microphone(self, device_index: int):
        """Set microphone device"""
        try:
            self.microphone = sr.Microphone(device_index=device_index)
            self._calibrate_microphone()
            logger.info(f"Microphone set to device index: {device_index}")
        except Exception as e:
            logger.error(f"Error setting microphone: {str(e)}")
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            pygame.mixer.quit()
            logger.info("Speech processor cleaned up")
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}")

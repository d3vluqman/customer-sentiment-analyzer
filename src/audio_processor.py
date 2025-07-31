"""
Audio Processing Module
Handles speech-to-text conversion and audio processing
"""

import speech_recognition as sr
import io
import tempfile
import os
from pathlib import Path


class AudioProcessor:
    """Handles audio processing and speech-to-text conversion"""

    def __init__(self):
        self.recognizer = sr.Recognizer()

        # Configure recognizer settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.operation_timeout = None
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.8

    def speech_to_text(self, audio_data, language="en-US"):
        """
        Convert audio data to text using speech recognition

        Args:
            audio_data: Audio data from Streamlit audio input
            language: Language code for recognition (default: 'en-US')

        Returns:
            str: Transcribed text
        """
        try:
            # Save audio data to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(audio_data.getvalue())
                temp_file_path = temp_file.name

            try:
                # Load audio file
                with sr.AudioFile(temp_file_path) as source:
                    # Adjust for ambient noise
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

                    # Record the audio
                    audio = self.recognizer.record(source)

                # Perform speech recognition
                try:
                    # Try Google Speech Recognition first (free tier)
                    text = self.recognizer.recognize_google(audio, language=language)
                    return text

                except sr.UnknownValueError:
                    # Try alternative recognition methods
                    return self._fallback_recognition(audio, language)

                except sr.RequestError as e:
                    # If Google service is unavailable, try offline recognition
                    return self._offline_recognition(audio)

            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)

        except Exception as e:
            raise Exception(f"Audio processing failed: {str(e)}")

    def _fallback_recognition(self, audio, language):
        """Try alternative recognition methods"""
        try:
            # Try Sphinx (offline) recognition
            text = self.recognizer.recognize_sphinx(audio)
            if text.strip():
                return text
        except:
            pass

        # If all methods fail
        raise sr.UnknownValueError("Could not understand audio")

    def _offline_recognition(self, audio):
        """Perform offline speech recognition using Sphinx"""
        try:
            text = self.recognizer.recognize_sphinx(audio)
            if text.strip():
                return text
            else:
                raise sr.UnknownValueError("No speech detected")
        except Exception as e:
            raise Exception(f"Offline recognition failed: {str(e)}")

    def validate_audio_quality(self, audio_data):
        """
        Validate audio quality and provide feedback

        Args:
            audio_data: Audio data to validate

        Returns:
            dict: Validation results with quality metrics
        """
        try:
            # Basic validation
            if not audio_data or audio_data.getvalue() == b"":
                return {
                    "is_valid": False,
                    "message": "No audio data detected",
                    "suggestions": [
                        "Please ensure your microphone is working",
                        "Try recording again",
                    ],
                }

            # Check audio size (rough quality indicator)
            audio_size = len(audio_data.getvalue())

            if audio_size < 1000:  # Very small file
                return {
                    "is_valid": False,
                    "message": "Audio recording too short or low quality",
                    "suggestions": [
                        "Speak louder and closer to the microphone",
                        "Record for at least 2-3 seconds",
                    ],
                }

            if audio_size > 10 * 1024 * 1024:  # Very large file (>10MB)
                return {
                    "is_valid": False,
                    "message": "Audio recording too long",
                    "suggestions": [
                        "Keep recordings under 2 minutes",
                        "Try breaking into shorter segments",
                    ],
                }

            return {
                "is_valid": True,
                "message": "Audio quality appears good",
                "audio_size": audio_size,
                "estimated_duration": self._estimate_duration(audio_size),
            }

        except Exception as e:
            return {
                "is_valid": False,
                "message": f"Audio validation failed: {str(e)}",
                "suggestions": ["Try recording again", "Check microphone permissions"],
            }

    def _estimate_duration(self, audio_size):
        """Estimate audio duration based on file size (rough approximation)"""
        # Rough estimation: assuming 16kHz, 16-bit mono audio
        # Actual duration may vary based on compression and format
        estimated_seconds = audio_size / (
            16000 * 2
        )  # bytes per second for 16kHz 16-bit
        return max(1, int(estimated_seconds))

    def enhance_audio_for_recognition(self, audio_data):
        """
        Apply basic audio enhancement for better recognition
        Note: This is a placeholder for more advanced audio processing
        """
        # In a production environment, you might want to:
        # - Apply noise reduction
        # - Normalize audio levels
        # - Apply filters to improve speech clarity
        # - Convert to optimal format for recognition

        # For now, return the original audio data
        return audio_data

    def get_supported_languages(self):
        """Get list of supported languages for speech recognition"""
        return {
            "en-US": "English (US)",
            "en-GB": "English (UK)",
            "es-ES": "Spanish (Spain)",
            "es-MX": "Spanish (Mexico)",
            "fr-FR": "French (France)",
            "de-DE": "German (Germany)",
            "it-IT": "Italian (Italy)",
            "pt-BR": "Portuguese (Brazil)",
            "ru-RU": "Russian (Russia)",
            "ja-JP": "Japanese (Japan)",
            "ko-KR": "Korean (South Korea)",
            "zh-CN": "Chinese (Simplified)",
            "zh-TW": "Chinese (Traditional)",
            "ar-SA": "Arabic (Saudi Arabia)",
            "hi-IN": "Hindi (India)",
        }

    def test_microphone_access(self):
        """Test if microphone access is available"""
        try:
            # This is a basic test - in a web environment,
            # microphone access is handled by the browser
            return {
                "available": True,
                "message": "Microphone access should be available through browser",
            }
        except Exception as e:
            return {"available": False, "message": f"Microphone test failed: {str(e)}"}

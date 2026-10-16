"""Speech-to-Text (STT) module for Univerlan.

Transcribes spoken audio (from microphone or audio file) into text,
ready for translation into Univerlan.
Supports SpeechRecognition (Google Speech API, Sphinx, or Whisper).
"""

from __future__ import annotations
import os
import sys
from typing import Optional

try:
    import speech_recognition as sr

    HAS_SR = True
except ImportError:
    HAS_SR = False


class SpeechTranscriber:
    """Handles Speech-to-Text conversion for Univerlan input."""

    def __init__(self, language: str = "en-US") -> None:
        self.language = language
        self.recognizer = sr.Recognizer() if HAS_SR else None

    def transcribe_file(self, audio_path: str) -> Optional[str]:
        """Transcribes an audio file (.wav, .flac, .aiff) into text."""
        if not HAS_SR or not self.recognizer:
            raise RuntimeError(
                "SpeechRecognition library is not installed in the environment."
            )

        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        with sr.AudioFile(audio_path) as source:
            audio_data = self.recognizer.record(source)
            try:
                text = self.recognizer.recognize_google(
                    audio_data, language=self.language
                )
                return text
            except sr.UnknownValueError:
                print(
                    "[STT] Audio could not be understood.",
                    file=sys.stderr,
                )
                return None
            except sr.RequestError as e:
                print(
                    f"[STT] Service request error from Speech API: {e}",
                    file=sys.stderr,
                )
                return None

    def listen_and_transcribe(
        self, timeout: int = 5, phrase_time_limit: int = 10
    ) -> Optional[str]:
        """Captures audio from default microphone and transcribes it to text."""
        if not HAS_SR or not self.recognizer:
            raise RuntimeError(
                "SpeechRecognition library is not installed in the environment."
            )

        try:
            with sr.Microphone() as source:
                print(
                    "[*] Adjusting for ambient noise... Speak clearly into the microphone."
                )
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                print("[*] Listening now...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit,
                )
                print("[*] Processing speech transcription...")
                text = self.recognizer.recognize_google(
                    audio, language=self.language
                )
                return text
        except (sr.UnknownValueError, sr.WaitTimeoutError):
            print("[STT] No speech detected or unclear input.", file=sys.stderr)
            return None
        except Exception as e:
            print(f"[STT Error] {e}", file=sys.stderr)
            return None

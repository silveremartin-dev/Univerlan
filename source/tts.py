"""Text-to-Speech (TTS) module for Univerlan.

Provides speech synthesis capabilities for Univerlan text using Windows SAPI
and cross-platform fallbacks (PowerShell System.Speech, pyttsx3, or WAV export).
"""

from __future__ import annotations
import os
import subprocess
import sys
from typing import Optional

from source.phonetics import to_ipa


class SpeechSynthesizer:
    """Handles speech synthesis for Univerlan."""

    def __init__(self, rate: int = 0, volume: int = 100) -> None:
        """rate: speech speed (-10 to 10)

        volume: 0 to 100
        """
        self.rate = rate
        self.volume = volume

    def prepare_phonetic_script(self, univerlan_text: str) -> str:
        """Prepares Univerlan text for English-based TTS engines so they pronounce

        pure vowels correctly (e.g. 'mi' pronounced as /mi/ rather than English /maɪ/).
        """
        # Minor adjustments for default English SAPI voice phonology
        adapted = univerlan_text
        # Replace 'mov-tu-mi' with separated tokens for clear prosodic pacing
        adapted = adapted.replace("-", " ")
        # Ensure 'mi' is spoken as 'mee' by English voice
        adapted = re_sub_whole_word(adapted, "mi", "mee")
        adapted = re_sub_whole_word(adapted, "wi", "wee")
        adapted = re_sub_whole_word(adapted, "hi", "hee")
        adapted = re_sub_whole_word(adapted, "xe", "shee")
        adapted = re_sub_whole_word(adapted, "de", "deh")
        adapted = re_sub_whole_word(adapted, "tu", "too")
        adapted = re_sub_whole_word(adapted, "nu", "noo")
        adapted = re_sub_whole_word(adapted, "fud", "food")
        adapted = re_sub_whole_word(adapted, "cild", "chilled")
        adapted = re_sub_whole_word(adapted, "cilds", "children")
        return adapted

    def speak(self, text: str, blocking: bool = True) -> bool:
        """Synthesizes and speaks Univerlan text aloud.

        Uses Windows PowerShell System.Speech.Synthesis natively on Windows.
        """
        adapted = self.prepare_phonetic_script(text)

        # On Windows, use System.Speech.Synthesis via PowerShell
        if sys.platform == "win32":
            # Sanitize text for PowerShell single-quote string
            clean_text = adapted.replace("'", "''").replace('"', '`"')
            ps_cmd = (
                f"Add-Type -AssemblyName System.Speech; "
                f"$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                f"$s.Rate = {self.rate}; $s.Volume = {self.volume}; "
                f"$s.Speak('{clean_text}')"
            )
            try:
                subprocess.run(
                    ["powershell", "-NoProfile", "-Command", ps_cmd],
                    check=True,
                    capture_output=True,
                    timeout=15,
                )
                return True
            except Exception as e:
                print(f"[TTS Warning] SAPI execution failed: {e}", file=sys.stderr)
                return False

        # On Linux/macOS fallback to espeak or say
        try:
            if sys.platform == "darwin":
                subprocess.run(["say", adapted], check=True)
                return True
            else:
                subprocess.run(["espeak", adapted], check=True)
                return True
        except Exception:
            return False

    def save_wav(self, text: str, output_path: str) -> bool:
        """Synthesizes text and saves it directly to a .wav audio file."""
        adapted = self.prepare_phonetic_script(text)
        abs_path = os.path.abspath(output_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)

        if sys.platform == "win32":
            clean_text = adapted.replace("'", "''").replace('"', '`"')
            clean_path = abs_path.replace("'", "''")
            ps_cmd = (
                f"Add-Type -AssemblyName System.Speech; "
                f"$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                f"$s.Rate = {self.rate}; $s.Volume = {self.volume}; "
                f"$s.SetOutputToWaveFile('{clean_path}'); "
                f"$s.Speak('{clean_text}'); "
                f"$s.Dispose()"
            )
            try:
                subprocess.run(
                    ["powershell", "-NoProfile", "-Command", ps_cmd],
                    check=True,
                    capture_output=True,
                    timeout=20,
                )
                return os.path.exists(abs_path) and os.path.getsize(abs_path) > 0
            except Exception as e:
                print(f"[TTS Warning] WAV export failed: {e}", file=sys.stderr)
                return False

        return False


def re_sub_whole_word(text: str, word: str, replacement: str) -> str:
    """Helper to replace isolated whole words case-insensitively."""
    import re

    pattern = r"\b" + re.escape(word) + r"\b"
    return re.sub(pattern, replacement, text, flags=re.IGNORECASE)

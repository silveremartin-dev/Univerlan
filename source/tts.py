"""Text-to-Speech (TTS) module for Univerlan.

Provides speech synthesis capabilities for Univerlan text using Windows SAPI
and cross-platform fallbacks (PowerShell System.Speech, pyttsx3, or WAV export).
"""

from __future__ import annotations
import os
import subprocess
import sys
import math
import wave
import struct
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
        adapted = re_sub_whole_word(adapted, "dey", "day")
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

        # On Windows, use System.Speech.Synthesis via PowerShell with safe stdin input
        if sys.platform == "win32":
            ps_script = (
                f"Add-Type -AssemblyName System.Speech; "
                f"$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                f"$s.Rate = {int(self.rate)}; $s.Volume = {int(self.volume)}; "
                f"$text = [Console]::In.ReadToEnd().Trim(); "
                f"if ($text) {{ $s.Speak($text) }}"
            )
            try:
                subprocess.run(
                    ["powershell", "-NoProfile", "-Command", ps_script],
                    input=adapted,
                    text=True,
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

    def generate_formant_wav(self, text: str, output_path: str, sample_rate: int = 22050) -> str:
        """Synthesizes text into a pure 16-bit PCM WAV using formant harmonics without external dependencies."""
        vowel_formants = {
            'a': (800, 1200),
            'e': (500, 1800),
            'i': (280, 2250),
            'o': (500, 850),
            'u': (320, 800)
        }
        clean_text = text.lower()
        samples = []
        f0_base = 130.0

        vowel_duration = 0.16
        consonant_duration = 0.08
        pause_duration = 0.10

        for char in clean_text:
            if char in " ,.?!;:-\n":
                n_samples = int(pause_duration * sample_rate)
                samples.extend([0.0] * n_samples)
                continue

            if char in vowel_formants:
                f1, f2 = vowel_formants[char]
                n_samples = int(vowel_duration * sample_rate)
                for i in range(n_samples):
                    t = i / sample_rate
                    glottal = (math.sin(2 * math.pi * f0_base * t) +
                               0.5 * math.sin(4 * math.pi * f0_base * t) +
                               0.25 * math.sin(6 * math.pi * f0_base * t))
                    v1 = math.sin(2 * math.pi * f1 * t) * math.exp(-t * 20.0)
                    v2 = 0.6 * math.sin(2 * math.pi * f2 * t) * math.exp(-t * 25.0)
                    env = math.sin(math.pi * (i / n_samples))
                    val = (glottal * 0.4 + (v1 + v2) * 0.6) * env * 0.7
                    samples.append(val)
            else:
                n_samples = int(consonant_duration * sample_rate)
                freq = 2200.0 if char in "szx" else 1500.0
                for i in range(n_samples):
                    t = i / sample_rate
                    env = math.sin(math.pi * (i / n_samples))
                    noise = math.sin(2 * math.pi * freq * t) * (0.8 + 0.2 * math.sin(100 * t))
                    samples.append(noise * env * 0.35)

        max_amp = max(abs(s) for s in samples) if samples else 1.0
        if max_amp == 0:
            max_amp = 1.0
        norm_factor = 28000.0 / max_amp

        abs_path = os.path.abspath(output_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)

        with wave.open(abs_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            raw = bytearray()
            for s in samples:
                val = int(s * norm_factor)
                val = max(-32767, min(32767, val))
                raw.extend(struct.pack('<h', val))
            wf.writeframes(raw)

        return abs_path

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
                if os.path.exists(abs_path) and os.path.getsize(abs_path) > 0:
                    return True
            except Exception as e:
                print(f"[TTS SAPI Warning, using formant fallback]: {e}", file=sys.stderr)

        # Fallback cross-platform formant harmonic synthesizer
        try:
            self.generate_formant_wav(text, abs_path)
            return os.path.exists(abs_path) and os.path.getsize(abs_path) > 0
        except Exception as e:
            print(f"[TTS Formant Error]: {e}", file=sys.stderr)
            return False


def re_sub_whole_word(text: str, word: str, replacement: str) -> str:
    """Helper to replace isolated whole words case-insensitively."""
    import re

    pattern = r"\b" + re.escape(word) + r"\b"
    return re.sub(pattern, replacement, text, flags=re.IGNORECASE)

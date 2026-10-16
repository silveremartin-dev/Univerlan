"""Unit tests for the speech synthesis module."""

import os
from source.tts import SpeechSynthesizer


def test_prepare_phonetic_script():
    tts = SpeechSynthesizer()
    adapted = tts.prepare_phonetic_script("mi go tu de xip")
    # mi -> mee, tu -> too
    assert "mee" in adapted.lower()
    assert "too" in adapted.lower()


def test_save_wav(tmp_path):
    tts = SpeechSynthesizer()
    wav_path = str(tmp_path / "test_speech.wav")
    ok = tts.save_wav("halo, min nem is Alex.", wav_path)
    if os.name == "nt":
        # On Windows, PowerShell SAPI should generate the WAV file
        assert ok is True
        assert os.path.exists(wav_path)
        assert os.path.getsize(wav_path) > 100

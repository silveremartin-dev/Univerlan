"""Unit tests for the Speech-to-Text (STT) module."""

import pytest
from source.stt import SpeechTranscriber, HAS_SR


def test_stt_initialization():
    stt = SpeechTranscriber(language="en-US")
    assert stt.language == "en-US"
    if HAS_SR:
        assert stt.recognizer is not None


def test_stt_missing_file():
    stt = SpeechTranscriber()
    if HAS_SR:
        with pytest.raises(FileNotFoundError):
            stt.transcribe_file("non_existent_audio_file.wav")

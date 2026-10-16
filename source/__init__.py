"""Univerlan: The Interstellar Rationalized Conlang Engine.

A constructed language designed for 23rd-century interstellar commerce
and unambiguous communication, inspired by John Wilkins, Basic English,
and bijective phonetic orthography.
"""

__version__ = "1.0.0"
__author__ = "Univerlan Contributors"
__license__ = "MIT"

from source.phonetics import PhoneticTranscriber, to_ipa, phonetic_cleanse
from source.morphology import Regularizer
from source.wilkins import WilkinsDecomposer
from source.translator import UniverlanTranslator
from source.tts import SpeechSynthesizer
from source.stt import SpeechTranscriber

__all__ = [
    "PhoneticTranscriber",
    "to_ipa",
    "phonetic_cleanse",
    "Regularizer",
    "WilkinsDecomposer",
    "UniverlanTranslator",
    "SpeechSynthesizer",
    "SpeechTranscriber",
]

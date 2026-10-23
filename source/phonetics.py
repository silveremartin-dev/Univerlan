"""Phonetics module for Univerlan.

Implements the bijective 1:1 grapheme-to-phoneme conversion, English orthography
regularization, and IPA generation.
"""

from __future__ import annotations
import re
import unicodedata
from typing import Dict, List, Tuple

# Mapping from Univerlan graphemes to International Phonetic Alphabet (IPA) symbols
UNIVERLAN_TO_IPA: Dict[str, str] = {
    # Vowels & Diphthongs
    "ai": "aɪ",
    "au": "aʊ",
    "ei": "eɪ",
    "oi": "ɔɪ",
    "a": "a",
    "e": "ɛ",
    "i": "i",
    "o": "ɔ",
    "u": "u",
    # Consonants
    "b": "b",
    "c": "tʃ",
    "d": "d",
    "f": "f",
    "g": "ɡ",
    "h": "h",
    "j": "dʒ",
    "k": "k",
    "l": "l",
    "m": "m",
    "n": "n",
    "p": "p",
    "r": "r",
    "s": "s",
    "t": "t",
    "v": "v",
    "w": "w",
    "x": "ʃ",
    "y": "j",
    "z": "z",
}

# Core English phonetic cleanse rules applied in strict sequence
PHONETIC_CLEANSE_RULES: List[Tuple[str, str]] = [
    # 1. Resolve English 'x' [ks] before introducing 'x' for [ʃ]
    (r"\bx([aeiou])", r"z\1"),
    (r"\bx", "eks"),
    (r"x", "ks"),
    # 2. Initial silent consonants
    (r"\bkn", "n"),
    (r"\bwr", "r"),
    (r"\bps", "s"),
    (r"\bpn", "n"),
    (r"\bgn", "n"),
    (r"\bwh", "w"),
    # 3. Silent b and p
    (r"mb\b", "m"),
    (r"bt\b", "t"),
    (r"pt\b", "t"),
    # 4. English 'ph' -> 'f'
    (r"ph", "f"),
    # 5. Soft English 'c' -> 's' when followed by e, i, y (provided it's not 'ch')
    (r"(?<!c)c(?=[eiy])", "s"),
    # 6. English 'ch' -> Univerlan 'c' [tʃ]
    (r"ch", "c"),
    # 7. Remaining English 'c' (hard) -> 'k'
    (r"c(?=[aouklmnprtvwz]|\b)", "k"),
    # 8. English 'sh' -> Univerlan 'x' [ʃ]
    (r"sh", "x"),
    # 9. Suffixes -tion / -sion -> -xun
    (r"[st]ion\b", "xun"),
    (r"[st]ions\b", "xuns"),
    # 10. English 'ck', 'qu', 'q'
    (r"ck", "k"),
    (r"qu", "kw"),
    (r"q", "k"),
    # 11. Voiced dental fricatives in common function words (th -> d)
    (r"\bthe\b", "de"),
    (r"\bthis\b", "dis"),
    (r"\bthat\b", "dat"),
    (r"\bthese\b", "dis"),
    (r"\bthose\b", "dos"),
    (r"\bthere\b", "der"),
    (r"\btheir\b", "deyn"),
    (r"\btheirs\b", "deyn"),
    (r"\bthemselves\b", "deyselfs"),
    (r"\bthey\b", "dey"),
    (r"\bthem\b", "dey"),
    (r"\bthen\b", "den"),
    (r"\bthan\b", "dan"),
    (r"\bwith\b", "wit"),
    # Voiceless th -> t
    (r"th", "t"),
    # 12. Vowels & Diphthongs
    (r"igh", "ai"),
    (r"ight\b", "ait"),
    (r"ee", "i"),
    (r"ea\b", "i"),
    (r"ou", "au"),
    (r"oo", "u"),
    (r"oa", "o"),
    # Magic-e split diphthongs: i_e -> ai (write -> rait, time -> taim)
    (r"i([bdfgjklmnprstvz])e\b", r"ai\1"),
    (r"a([bdfgjklmnprstvz])e\b", r"ei\1"),
    # General silent terminal 'e' after consonants
    (r"([aeiou])([bdfgjklmnprstvz])e\b", r"\1\2"),
    # Double consonant reduction: 'pp' -> 'p', 'tt' -> 't', 'll' -> 'l'
    (r"([bdfgjklmnprstvz])\1+", r"\1"),
]


class PhoneticTranscriber:
    """Handles bijective transcription between Univerlan script and IPA,

    and performs phonetic cleansing of historic irregular spellings.
    """

    @staticmethod
    def cleanse_word(word: str) -> str:
        """Applies phonological rules to convert irregular English spelling

        into an initial phonetically regularized form.
        """
        if not word:
            return ""

        w = unicodedata.normalize("NFKD", word).lower()

        for pattern, replacement in PHONETIC_CLEANSE_RULES:
            w = re.sub(pattern, replacement, w)

        return w

    @staticmethod
    def to_ipa(text: str) -> str:
        """Converts Univerlan text into standard International Phonetic Alphabet (IPA).

        Because Univerlan has a 1:1 bijective orthography, this mapping is deterministic.
        """
        tokens = re.findall(r"[A-Za-z\-]+|[^\w\s]|\s+", text)
        ipa_tokens: List[str] = []

        for token in tokens:
            if not re.match(r"[A-Za-z\-]", token):
                ipa_tokens.append(token)
                continue

            lowered = token.lower()
            idx = 0
            n = len(lowered)
            word_ipa: List[str] = []

            while idx < n:
                if lowered[idx] == "-":
                    word_ipa.append(".")
                    idx += 1
                    continue

                if idx + 1 < n and lowered[idx : idx + 2] in UNIVERLAN_TO_IPA:
                    word_ipa.append(UNIVERLAN_TO_IPA[lowered[idx : idx + 2]])
                    idx += 2
                elif lowered[idx] in UNIVERLAN_TO_IPA:
                    word_ipa.append(UNIVERLAN_TO_IPA[lowered[idx]])
                    idx += 1
                else:
                    word_ipa.append(lowered[idx])
                    idx += 1

            ipa_tokens.append("/" + "".join(word_ipa) + "/")

        return "".join(ipa_tokens)


def to_ipa(text: str) -> str:
    """Helper shortcut to convert text to IPA."""
    return PhoneticTranscriber.to_ipa(text)


def phonetic_cleanse(word: str) -> str:
    """Helper shortcut to cleanse a word phonetically."""
    return PhoneticTranscriber.cleanse_word(word)

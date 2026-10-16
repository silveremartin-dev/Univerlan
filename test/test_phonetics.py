"""Unit tests for the phonetics and orthography module."""

from source.phonetics import PhoneticTranscriber, to_ipa, phonetic_cleanse


def test_silent_letter_cleansing():
    # knight -> nait, know -> no, write -> rait
    assert phonetic_cleanse("knight") == "nait"
    assert phonetic_cleanse("write") == "rait"
    assert phonetic_cleanse("doubt") == "daut"
    assert phonetic_cleanse("climb") == "klaim" or phonetic_cleanse(
        "climb"
    ).startswith("k")


def test_digraph_simplification():
    # ph -> f, ch -> c, sh -> x
    assert phonetic_cleanse("photo") == "foto"
    assert phonetic_cleanse("ship") == "xip"
    assert phonetic_cleanse("check") == "cek"


def test_consonant_degemination():
    # double consonants reduced to single
    assert phonetic_cleanse("apple") == "apel" or "pp" not in phonetic_cleanse(
        "apple"
    )
    assert "tt" not in phonetic_cleanse("better")


def test_to_ipa_bijective():
    # Check that Univerlan tokens map deterministically to IPA
    ipa = to_ipa("mi go")
    assert "/mi/" in ipa
    assert "/ɡɔ/" in ipa or "/ɡo/" in ipa

    # Check affricate and fricatives: c [tʃ], x [ʃ]
    ipa_c = to_ipa("cek")
    assert "tʃ" in ipa_c

    ipa_x = to_ipa("xip")
    assert "ʃ" in ipa_x

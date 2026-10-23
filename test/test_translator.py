"""Unit tests for the end-to-end translation pipeline."""

from source.translator import UniverlanTranslator


def test_basic_svo_translation():
    t = UniverlanTranslator()
    res = t.translate("I go to the station.")
    assert "mi" in res.univerlan_text.lower()
    assert "go" in res.univerlan_text.lower()
    assert "tu" in res.univerlan_text.lower()
    assert "de" in res.univerlan_text.lower()
    assert "stasion" in res.univerlan_text.lower()


def test_irregular_verb_translation():
    t = UniverlanTranslator()
    res = t.translate("He bought five ships yesterday.")
    assert "hi" in res.univerlan_text.lower()
    assert "bayed" in res.univerlan_text.lower()
    assert "xips" in res.univerlan_text.lower()


def test_wilkins_compound_translation():
    t = UniverlanTranslator()
    res = t.translate("Please lift the cargo and push it.")
    assert "mov-up" in res.univerlan_text.lower()
    assert "mov-fro-mi" in res.univerlan_text.lower()
    assert "kargo" in res.univerlan_text.lower()


def test_negation_simplification():
    t = UniverlanTranslator()
    res = t.translate("We do not wait.")
    assert "wi no weit" in res.univerlan_text.lower()

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


def test_french_translation_pipeline():
    t = UniverlanTranslator()
    res = t.translate("L'humain parle avec l'enfant.")
    assert "de man" in res.univerlan_text.lower() or "de human" in res.univerlan_text.lower()
    assert "spik" in res.univerlan_text.lower()
    assert "wit" in res.univerlan_text.lower()
    assert "de cild" in res.univerlan_text.lower()


def test_four_way_symmetry():
    t = UniverlanTranslator()
    fr_src = "Tous les vaisseaux voyagent vers les étoiles."
    en_src = "All ships travel to the stars."
    uv_canonical = "Ol xips travel tu de sters."

    assert t.translate(fr_src, direction="fr_to_uv").univerlan_text == uv_canonical
    assert t.translate(en_src, direction="en_to_uv").univerlan_text == uv_canonical
    assert t.translate(uv_canonical, direction="uv_to_en", target_lang="en").univerlan_text == en_src
    assert t.translate(uv_canonical, direction="uv_to_fr", target_lang="fr").univerlan_text == fr_src


def test_french_negation_and_wilkins():
    t = UniverlanTranslator()
    res = t.translate("Ouvrez la porte et chauffez l'eau.")
    assert "mek-open" in res.univerlan_text.lower()
    assert "dor" in res.univerlan_text.lower()
    assert "mek-hot" in res.univerlan_text.lower()
    assert "wata" in res.univerlan_text.lower()

    res_neg = t.translate("Je ne veux pas mourir dans le vide spatial.")
    assert "mi no wont" in res_neg.univerlan_text.lower()
    assert "dai" in res_neg.univerlan_text.lower()
    assert "vakjum" in res_neg.univerlan_text.lower()


def test_reverse_translation_to_french_and_english():
    t = UniverlanTranslator()
    # Univerlan -> French
    res_fr = t.translate("De kapten luk de xip.", direction="from_univerlan", target_lang="fr")
    assert "capitaine" in res_fr.univerlan_text.lower()
    assert "vaisseau" in res_fr.univerlan_text.lower()

    # Univerlan -> English
    res_en = t.translate("De kapten luk de xip.", direction="from_univerlan", target_lang="en")
    assert "captain" in res_en.univerlan_text.lower()
    assert "ship" in res_en.univerlan_text.lower()

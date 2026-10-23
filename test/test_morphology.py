"""Unit tests for the morphology and regularization module."""

from source.morphology import Regularizer


def test_pronoun_regularization():
    assert Regularizer.regularize_token("i") == "mi"
    assert Regularizer.regularize_token("me") == "mi"
    assert Regularizer.regularize_token("my") == "min"
    assert Regularizer.regularize_token("she") == "xe"
    assert Regularizer.regularize_token("her") == "xe"
    assert Regularizer.regularize_token("they") == "dey"
    assert Regularizer.regularize_token("them") == "dey"
    assert Regularizer.regularize_token("their") == "deyn"


def test_irregular_verbs_elimination():
    # went -> goed
    assert Regularizer.regularize_token("went") == "goed"
    # bought -> bayed
    assert Regularizer.regularize_token("bought") == "bayed"
    # took -> teked
    assert Regularizer.regularize_token("took") == "teked"
    # saw -> sied
    assert Regularizer.regularize_token("saw") == "sied"
    # was -> ised
    assert Regularizer.regularize_token("was") == "ised"


def test_irregular_plurals_regularization():
    assert Regularizer.regularize_token("children") == "cilds"
    assert Regularizer.regularize_token("people") == "mans"
    assert Regularizer.regularize_token("teeth") == "tuts"
    assert Regularizer.regularize_token("feet") == "futs"


def test_regular_plural_suffix():
    assert Regularizer.regularize_plural("planet") == "planets"
    assert Regularizer.regularize_plural("boks") == "bokses"
    assert Regularizer.regularize_plural("stasion") == "stasions"


def test_comparatives():
    assert Regularizer.regularize_token("better") == "mor gud"
    assert Regularizer.regularize_token("best") == "most gud"
    assert Regularizer.regularize_token("worse") == "mor bad"

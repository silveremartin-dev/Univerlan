"""Unit tests for the Wilkinsian conceptual decomposition module."""

from source.wilkins import WilkinsDecomposer


def test_wilkins_vertical_vectors():
    lift_res = WilkinsDecomposer.decompose("lift")
    assert lift_res is not None
    assert lift_res[0] == "mov-up"

    fall_res = WilkinsDecomposer.decompose("fall")
    assert fall_res is not None
    assert fall_res[0] == "mov-don"

    drop_res = WilkinsDecomposer.decompose("drop")
    assert drop_res is not None
    assert drop_res[0] == "mov-don"


def test_wilkins_egocentric_vectors():
    # pull -> mov-tu-mi
    pull_res = WilkinsDecomposer.decompose("pull")
    assert pull_res is not None
    assert pull_res[0] == "mov-tu-mi"

    # push -> mov-fro-mi
    push_res = WilkinsDecomposer.decompose("push")
    assert push_res is not None
    assert push_res[0] == "mov-fro-mi"


def test_wilkins_boundary_vectors():
    enter_res = WilkinsDecomposer.decompose("enter")
    assert enter_res is not None
    assert enter_res[0] == "mov-in"

    exit_res = WilkinsDecomposer.decompose("exit")
    assert exit_res is not None
    assert exit_res[0] == "mov-ut"


def test_wilkins_inflected():
    lifted = WilkinsDecomposer.decompose("lifted")
    assert lifted is not None
    assert lifted[0] == "mov-up-ed"

    pushed = WilkinsDecomposer.decompose("pushed")
    assert pushed is not None
    assert pushed[0] == "mov-fro-mi-ed"

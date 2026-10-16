"""Wilkins module for Univerlan.

Implements the John Wilkins a priori conceptual categorization and semantic
vector decomposition for verbs and state transitions.

As noted in the founding notes:
- lift -> mov-up
- pull -> mov-tu-mi
- push -> mov-fro-mi
- drop/fall -> mov-don
- enter -> mov-in
- exit -> mov-ut
"""

from __future__ import annotations
import re
from typing import Dict, Optional, Tuple

# Mapping of English conceptual verbs to their Wilkinsian Univerlan compounds
# Format: { english_lemma: (univerlan_compound, category) }
WILKINS_VECTOR_MAP: Dict[str, Tuple[str, str]] = {
    # Vertical kinetic vectors
    "lift": ("mov-up", "kinetic.vertical.up"),
    "raise": ("mov-up", "kinetic.vertical.up"),
    "elevate": ("mov-up", "kinetic.vertical.up"),
    "fall": ("mov-don", "kinetic.vertical.down"),
    "drop": ("mov-don", "kinetic.vertical.down"),
    "lower": ("mov-don", "kinetic.vertical.down"),
    "sink": ("mov-don", "kinetic.vertical.down"),
    "descend": ("mov-don", "kinetic.vertical.down"),
    "climb": ("mov-up", "kinetic.vertical.up"),
    "ascend": ("mov-up", "kinetic.vertical.up"),
    # Egocentric kinetic vectors (to/from speaker)
    "pull": ("mov-tu-mi", "kinetic.egocentric.towards"),
    "drag": ("mov-tu-mi", "kinetic.egocentric.towards"),
    "attract": ("mov-tu-mi", "kinetic.egocentric.towards"),
    "push": ("mov-fro-mi", "kinetic.egocentric.away"),
    "shove": ("mov-fro-mi", "kinetic.egocentric.away"),
    "repel": ("mov-fro-mi", "kinetic.egocentric.away"),
    # Boundary kinetic vectors (in/out)
    "enter": ("mov-in", "kinetic.boundary.in"),
    "board": ("mov-in", "kinetic.boundary.in"),
    "embark": ("mov-in", "kinetic.boundary.in"),
    "penetrate": ("mov-in", "kinetic.boundary.in"),
    "exit": ("mov-ut", "kinetic.boundary.out"),
    "leave": ("mov-ut", "kinetic.boundary.out"),
    "disembark": ("mov-ut", "kinetic.boundary.out"),
    # Trajectory kinetic vectors (forward/back)
    "advance": ("mov-fowad", "kinetic.trajectory.forward"),
    "proceed": ("mov-fowad", "kinetic.trajectory.forward"),
    "retreat": ("mov-bak", "kinetic.trajectory.backward"),
    "return": ("mov-bak", "kinetic.trajectory.backward"),
    # Causative state transitions
    "heat": ("mek-hot", "causative.thermal.hot"),
    "warm": ("mek-hot", "causative.thermal.hot"),
    "cool": ("mek-kold", "causative.thermal.cold"),
    "chill": ("mek-kold", "causative.thermal.cold"),
    "open": ("mek-open", "causative.aperture.open"),
    "close": ("mek-klos", "causative.aperture.closed"),
    "shut": ("mek-klos", "causative.aperture.closed"),
    "clean": ("mek-klir", "causative.purity.clean"),
    "clarify": ("mek-klir", "causative.purity.clean"),
    "kill": ("mek-ded", "causative.vitality.terminate"),
}

# Inflected English past forms for Wilkinsian verbs
WILKINS_INFLECTED_MAP: Dict[str, Tuple[str, bool]] = {
    "lifted": ("lift", True),
    "raising": ("raise", False),
    "raised": ("raise", True),
    "elevated": ("elevate", True),
    "fell": ("fall", True),
    "fallen": ("fall", True),
    "dropped": ("drop", True),
    "lowered": ("lower", True),
    "descended": ("descend", True),
    "pulled": ("pull", True),
    "dragged": ("drag", True),
    "pushed": ("push", True),
    "shoved": ("shove", True),
    "entered": ("enter", True),
    "boarded": ("board", True),
    "exited": ("exit", True),
    "advanced": ("advance", True),
    "retreated": ("retreat", True),
    "returned": ("return", True),
    "heated": ("heat", True),
    "cooled": ("cool", True),
    "opened": ("open", True),
    "closed": ("close", True),
    "killed": ("kill", True),
}


class WilkinsDecomposer:
    """Decomposes complex English conceptual verbs into Wilkinsian relational vectors."""

    @staticmethod
    def decompose(word: str) -> Optional[Tuple[str, str]]:
        """Given an English word, returns (univerlan_compound, category_id)

        if a Wilkinsian decomposition exists.
        """
        low = word.lower()

        # Direct lemma match
        if low in WILKINS_VECTOR_MAP:
            return WILKINS_VECTOR_MAP[low]

        # Inflected past forms
        if low in WILKINS_INFLECTED_MAP:
            lemma, is_past = WILKINS_INFLECTED_MAP[low]
            compound, cat = WILKINS_VECTOR_MAP[lemma]
            if is_past:
                return (f"{compound}-ed", cat)
            return (compound, cat)

        # Participle -ing forms
        if low.endswith("ing"):
            stem = re.sub(r"ing$", "", low)
            if stem in WILKINS_VECTOR_MAP:
                compound, cat = WILKINS_VECTOR_MAP[stem]
                return (f"{compound}-ing", cat)
            # handle doubled consonants: dropping -> drop
            if len(stem) > 2 and stem[-1] == stem[-2] and stem[:-1] in WILKINS_VECTOR_MAP:
                compound, cat = WILKINS_VECTOR_MAP[stem[:-1]]
                return (f"{compound}-ing", cat)

        return None

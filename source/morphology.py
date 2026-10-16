"""Morphology module for Univerlan.

Eliminates all English grammatical irregularities:
- Absolute verb regularity (no irregular forms)
- Simplified invariant pronouns with systematic possessive '-n'
- Universal pluralization '-s'/'-es'
- Transparent comparative ('mor') and superlative ('most')
"""

from __future__ import annotations
import re
from typing import Dict, Optional, Tuple

# English irregular verb past & participle mappings to (canonical_root, is_past)
IRREGULAR_VERB_MAP: Dict[str, Tuple[str, bool]] = {
    # be
    "am": ("is", False),
    "is": ("is", False),
    "are": ("is", False),
    "was": ("is", True),
    "were": ("is", True),
    "been": ("is", True),
    "being": ("is", False),
    # go
    "go": ("go", False),
    "goes": ("go", False),
    "went": ("go", True),
    "gone": ("go", True),
    # have
    "have": ("hav", False),
    "has": ("hav", False),
    "had": ("hav", True),
    # do
    "do": ("du", False),
    "does": ("du", False),
    "did": ("du", True),
    "done": ("du", True),
    # say
    "say": ("sei", False),
    "says": ("sei", False),
    "said": ("sei", True),
    # see
    "see": ("si", False),
    "sees": ("si", False),
    "saw": ("si", True),
    "seen": ("si", True),
    # give
    "give": ("giv", False),
    "gives": ("giv", False),
    "gave": ("giv", True),
    "given": ("giv", True),
    # take
    "take": ("tek", False),
    "takes": ("tek", False),
    "took": ("tek", True),
    "taken": ("tek", True),
    # make
    "make": ("mek", False),
    "makes": ("mek", False),
    "made": ("mek", True),
    # come
    "come": ("kom", False),
    "comes": ("kom", False),
    "came": ("kom", True),
    # think
    "think": ("tink", False),
    "thinks": ("tink", False),
    "thought": ("tink", True),
    # know
    "know": ("no", False),
    "knows": ("no", False),
    "knew": ("no", True),
    "known": ("no", True),
    # get
    "get": ("get", False),
    "gets": ("get", False),
    "got": ("get", True),
    "gotten": ("get", True),
    # buy
    "buy": ("bay", False),
    "buys": ("bay", False),
    "bought": ("bay", True),
    # sell
    "sell": ("sel", False),
    "sells": ("sel", False),
    "sold": ("sel", True),
    # find
    "find": ("faind", False),
    "finds": ("faind", False),
    "found": ("faind", True),
    # tell
    "tell": ("tel", False),
    "tells": ("tel", False),
    "told": ("tel", True),
    # speak
    "speak": ("spik", False),
    "speaks": ("spik", False),
    "spoke": ("spik", True),
    "spoken": ("spik", True),
    # write
    "write": ("rait", False),
    "writes": ("rait", False),
    "wrote": ("rait", True),
    "written": ("rait", True),
    # read
    "read": ("rid", False),
    "reads": ("rid", False),
    # send
    "send": ("send", False),
    "sends": ("send", False),
    "sent": ("send", True),
    # build
    "build": ("bild", False),
    "builds": ("bild", False),
    "built": ("bild", True),
    # drive / fly / run
    "drive": ("draiv", False),
    "drove": ("draiv", True),
    "driven": ("draiv", True),
    "fly": ("flai", False),
    "flew": ("flai", True),
    "flown": ("flai", True),
    "run": ("ran", False),
    "ran": ("ran", True),
}

# Pronoun mapping: strictly position-based (no case declension), systematic possessive '-n'
PRONOUN_MAP: Dict[str, str] = {
    # 1st person
    "i": "mi",
    "me": "mi",
    "my": "min",
    "mine": "min",
    "myself": "miself",
    "we": "wi",
    "us": "wi",
    "our": "win",
    "ours": "win",
    "ourselves": "wiselfs",
    # 2nd person
    "you": "yu",
    "your": "yun",
    "yours": "yun",
    "yourself": "yuself",
    "yourselves": "yuselfs",
    # 3rd person masculine
    "he": "hi",
    "him": "hi",
    "his": "hin",
    "himself": "hiself",
    # 3rd person feminine
    "she": "xe",
    "her": "xe",
    "hers": "xen",
    "herself": "xeself",
    # 3rd person neuter
    "it": "it",
    "its": "itn",
    "itself": "itself",
    # 3rd person plural
    "they": "de",
    "them": "de",
    "their": "den",
    "theirs": "den",
    "themselves": "deselfs",
}

# Irregular plural replacements
IRREGULAR_PLURAL_MAP: Dict[str, str] = {
    "children": "cilds",
    "child": "cild",
    "men": "mans",
    "man": "man",
    "women": "womans",
    "woman": "woman",
    "people": "mans",
    "teeth": "tuts",
    "tooth": "tut",
    "feet": "futs",
    "foot": "fut",
    "mice": "mauses",
    "mouse": "maus",
    "oxen": "okses",
    "ox": "oks",
}

# Irregular comparative / superlative replacements
IRREGULAR_COMPARISON_MAP: Dict[str, str] = {
    "better": "mor gud",
    "best": "most gud",
    "worse": "mor bad",
    "worst": "most bad",
    "more": "mor",
    "most": "most",
    "less": "mor smol",
    "least": "most smol",
}


class Regularizer:
    """Provides methods to regularize morphology from English into Univerlan canonical forms."""

    @staticmethod
    def regularize_verb_past(root: str) -> str:
        """Appends the regular past tense suffix '-ed' to a canonical root."""
        if root.endswith("e"):
            return root + "d"
        return root + "ed"

    @staticmethod
    def regularize_plural(noun: str) -> str:
        """Appends regular plural suffix '-s' or '-es'."""
        if re.search(r"[szxc]$", noun):
            return noun + "es"
        return noun + "s"

    @staticmethod
    def regularize_token(token: str) -> Optional[str]:
        """Resolves known irregular forms (verbs, pronouns, plurals, comparatives)."""
        lower = token.lower()

        # Check comparisons
        if lower in IRREGULAR_COMPARISON_MAP:
            return IRREGULAR_COMPARISON_MAP[lower]

        # Check pronouns
        if lower in PRONOUN_MAP:
            return PRONOUN_MAP[lower]

        # Check irregular plurals
        if lower in IRREGULAR_PLURAL_MAP:
            return IRREGULAR_PLURAL_MAP[lower]

        # Check irregular verbs
        if lower in IRREGULAR_VERB_MAP:
            root, is_past = IRREGULAR_VERB_MAP[lower]
            if is_past:
                return Regularizer.regularize_verb_past(root)
            return root

        return None

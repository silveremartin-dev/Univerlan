"""Translator module for Univerlan.

Coordinates the translation pipeline from English to Univerlan:
1. Tokenization & syntactic preprocessing
2. Wilkinsian decomposition
3. Morphological regularization
4. Lexical mapping
5. Bijective phonetic cleansing
"""

from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Dict, List, Optional

from source.phonetics import PhoneticTranscriber, to_ipa
from source.morphology import Regularizer
from source.wilkins import WilkinsDecomposer

# Core English to Univerlan direct lexical mapping (lemmas)
LEXICON_EN_TO_UNIVERLAN: Dict[str, str] = {
    # Pronouns & Articles
    "the": "de",
    "a": "un",
    "an": "un",
    "this": "dis",
    "that": "dat",
    "these": "dis",
    "those": "dos",
    "there": "der",
    "here": "hiar",
    "where": "wer",
    "what": "wat",
    "who": "hu",
    "why": "wai",
    "how": "hau",
    "when": "wen",
    # Connectors & Prepositions
    "and": "and",
    "or": "or",
    "but": "but",
    "if": "if",
    "because": "bikoz",
    "so": "so",
    "then": "den",
    "to": "tu",
    "from": "fro",
    "in": "in",
    "on": "on",
    "at": "at",
    "with": "wit",
    "without": "witut",
    "for": "for",
    "about": "abut",
    "by": "bai",
    "under": "onda",
    "over": "ova",
    "between": "bitwin",
    "through": "tru",
    # Modals & Auxiliaries
    "will": "wil",
    "would": "wud",
    "can": "kan",
    "could": "kud",
    "must": "mas",
    "should": "xud",
    "may": "kan",
    "might": "kud",
    # Common Nouns
    "man": "man",
    "person": "man",
    "people": "mans",
    "woman": "woman",
    "child": "cild",
    "ship": "xip",
    "starship": "stat-xip",
    "station": "stasion",
    "planet": "planet",
    "star": "sta",
    "moon": "lun",
    "cargo": "kargo",
    "trade": "treid",
    "trader": "treider",
    "price": "prais",
    "credit": "kredit",
    "credits": "kredits",
    "money": "kredit",
    "water": "wata",
    "food": "fud",
    "power": "enaji",
    "energy": "enaji",
    "fuel": "fuel",
    "engine": "mov-tul",
    "lever": "lever",
    "door": "dor",
    "hatch": "hac",
    "dock": "dok",
    "outpost": "utpost",
    "radio": "kom-tul",
    "sensor": "vju-tul",
    "screen": "skrin",
    "time": "taim",
    "day": "dei",
    "night": "nait",
    "year": "yiar",
    "system": "sistem",
    "systems": "sistems",
    "crystal": "kristal",
    "crystals": "kristals",
    "medicine": "medisin",
    "ramp": "ramp",
    "bay": "bei",
    "captain": "kapten",
    "doctor": "doktor",
    "friend": "frend",
    "enemy": "enemi",
    # Adjectives & Adverbs
    "good": "gud",
    "well": "gud",
    "bad": "bad",
    "big": "big",
    "large": "big",
    "small": "smol",
    "little": "smol",
    "new": "nu",
    "old": "old",
    "hot": "hot",
    "cold": "kold",
    "fast": "kwik",
    "quick": "kwik",
    "slow": "slo",
    "safe": "saf",
    "danger": "danja",
    "dangerous": "danjas",
    "clean": "klir",
    "clear": "klir",
    "ready": "redi",
    "true": "tru",
    "false": "fols",
    "open": "open",
    "closed": "klos",
    "now": "nau",
    "please": "pliis",
    "thanks": "dank",
    "thank": "dank",
    "yes": "yes",
    "no": "no",
    "not": "no",
    "all": "ol",
    "some": "som",
    "many": "meni",
    "much": "mac",
    "few": "fyu",
    "very": "veri",
    # Verbs
    "be": "is",
    "have": "hav",
    "do": "du",
    "say": "sei",
    "see": "si",
    "hear": "hir",
    "speak": "spik",
    "talk": "spik",
    "tell": "tel",
    "know": "no",
    "think": "tink",
    "take": "tek",
    "give": "giv",
    "buy": "bay",
    "sell": "sel",
    "make": "mek",
    "work": "wok",
    "operate": "operat",
    "help": "help",
    "stop": "stop",
    "start": "stat",
    "begin": "stat",
    "wait": "weit",
    "understand": "andastan",
    "agree": "agri",
    "bring": "bring",
    "find": "faind",
    "repair": "fix",
    "fix": "fix",
}


@dataclass
class TranslationResult:
    """Represents the structured result of an English -> Univerlan translation."""

    english_source: str
    univerlan_text: str
    ipa_transcription: str
    gloss: List[str] = field(default_factory=list)


class UniverlanTranslator:
    """High-level translation engine from English to canonical Univerlan."""

    def __init__(self) -> None:
        self.transcriber = PhoneticTranscriber()
        self.regularizer = Regularizer()
        self.wilkins = WilkinsDecomposer()

    def translate_word(self, word: str) -> Tuple[str, str]:
        """Translates and regularizes a single word.

        Returns (univerlan_word, gloss_info).
        """
        low = word.lower()

        # Step 1: Wilkinsian decomposition (lift -> mov-up, pull -> mov-tu-mi, etc.)
        wilkins_res = self.wilkins.decompose(low)
        if wilkins_res:
            compound, category = wilkins_res
            return (compound, f"{word} -> {compound} [{category}]")

        # Step 2: Irregular grammar and morphology regularization
        reg_res = self.regularizer.regularize_token(low)
        if reg_res:
            return (reg_res, f"{word} -> {reg_res} [regularized]")

        # Step 3: Core lexicon lookup
        if low in LEXICON_EN_TO_UNIVERLAN:
            mapped = LEXICON_EN_TO_UNIVERLAN[low]
            return (mapped, f"{word} -> {mapped} [lexicon]")

        # Step 4: Handle standard plural ending (-s / -es)
        if low.endswith("s") and len(low) > 3:
            stem = low[:-2] if low.endswith("es") else low[:-1]
            if stem in LEXICON_EN_TO_UNIVERLAN:
                mapped_stem = LEXICON_EN_TO_UNIVERLAN[stem]
                plural_form = self.regularizer.regularize_plural(mapped_stem)
                return (plural_form, f"{word} -> {plural_form} [plural]")

        # Step 5: Handle regular past ending (-ed)
        if low.endswith("ed") and len(low) > 3:
            stem = low[:-2]
            if stem in LEXICON_EN_TO_UNIVERLAN:
                mapped_stem = LEXICON_EN_TO_UNIVERLAN[stem]
                past_form = self.regularizer.regularize_verb_past(mapped_stem)
                return (past_form, f"{word} -> {past_form} [past]")

        # Step 6: Fallback: Phonetic cleanse (1:1 orthography)
        cleansed = self.transcriber.cleanse_word(low)
        return (cleansed, f"{word} -> {cleansed} [phonetic]")

    def translate(self, text: str) -> TranslationResult:
        """Translates an English sentence or paragraph into Univerlan."""
        if not text or not text.strip():
            return TranslationResult(
                english_source=text,
                univerlan_text="",
                ipa_transcription="",
                gloss=[],
            )

        # Pre-process English contractions: don't -> no, didn't -> no, isn't -> no is, etc.
        s = text
        s = re.sub(r"\b(don't|do not|doesn't|does not)\b", "no", s, flags=re.IGNORECASE)
        s = re.sub(
            r"\b(didn't|did not)\b", "no did", s, flags=re.IGNORECASE
        )  # or simple past negation
        s = re.sub(r"\b(won't|will not)\b", "no wil", s, flags=re.IGNORECASE)
        s = re.sub(r"\b(can't|cannot)\b", "no kan", s, flags=re.IGNORECASE)
        s = re.sub(r"\b(i'm)\b", "mi is", s, flags=re.IGNORECASE)
        s = re.sub(r"\b(you're)\b", "yu is", s, flags=re.IGNORECASE)
        s = re.sub(r"\b(we're)\b", "wi is", s, flags=re.IGNORECASE)
        s = re.sub(r"\b(they're)\b", "dey is", s, flags=re.IGNORECASE)

        # Tokenize preserving punctuation and whitespace
        tokens = re.findall(r"[A-Za-z\-]+|[0-9]+|[^\w\s]|\s+", s)
        out_tokens: List[str] = []
        gloss_entries: List[str] = []

        for token in tokens:
            if re.match(r"^[A-Za-z\-]+$", token):
                translated_word, gloss_info = self.translate_word(token)
                # Preserve capitalisation if original token started with capital
                if token[0].isupper() and translated_word:
                    translated_word = translated_word[0].upper() + translated_word[1:]
                out_tokens.append(translated_word)
                gloss_entries.append(gloss_info)
            else:
                out_tokens.append(token)

        final_text = "".join(out_tokens)
        ipa = to_ipa(final_text)

        return TranslationResult(
            english_source=text,
            univerlan_text=final_text,
            ipa_transcription=ipa,
            gloss=gloss_entries,
        )

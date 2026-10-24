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
import unicodedata
from typing import Dict, List, Optional, Tuple

from source.phonetics import PhoneticTranscriber, to_ipa
from source.morphology import Regularizer
from source.wilkins import WilkinsDecomposer
from source.pivot_fr import french_to_english, english_to_french
from source.lexicon_data import (
    CORE_LEXICON_EN,
    CORE_LEXICON_FR,
    REVERSE_LEXICON_UV_TO_EN,
    REVERSE_LEXICON_UV_TO_FR,
)


def strip_accents(text: str) -> str:
    """Removes diacritics / accents for robust multilingual matching."""
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )

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
    "starship": "starxip",
    "station": "stasion",
    "planet": "planet",
    "star": "ster",
    "stars": "sters",
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
LEXICON_EN_TO_UNIVERLAN.update(CORE_LEXICON_EN)
# Canonical overrides guaranteed after dictionary merge
LEXICON_EN_TO_UNIVERLAN.update({
    "prince": "prins",
    "little": "litl",
    "small": "smol",
    "live": "liv",
    "lives": "liv",
    "human": "man",
    "humans": "mans",
    "citizen": "sitizen",
    "citizens": "sitizens",
    "galaxy": "galaksi",
    "of": "ov",
    "star": "ster",
    "stars": "sters",
    "starship": "starxip",
    "starships": "starxips",
    "ship": "xip",
    "ships": "xips",
    "travel": "travel",
    "travels": "travel",
    "speak": "spik",
    "speaks": "spik",
    "water": "wata",
    "door": "dor",
    "child": "cild",
    "children": "cilds",
})
REVERSE_LEXICON_UV_TO_EN.update({
    "prins": "prince",
    "litl": "little",
    "smol": "small",
    "liv": "live",
    "man": "human",
    "mans": "humans",
    "sitizen": "citizen",
    "sitizens": "citizens",
    "galaksi": "galaxy",
    "ov": "of",
    "ster": "star",
    "sters": "stars",
    "starxip": "starship",
    "starxips": "starships",
    "xip": "ship",
    "xips": "ships",
    "travel": "travel",
    "spik": "speak",
    "wata": "water",
    "water": "water",
    "dor": "door",
    "cild": "child",
    "cilds": "children",
    "halo": "hello",
})
REVERSE_LEXICON_UV_TO_FR.update({
    "prins": "prince",
    "litl": "petit",
    "smol": "petite",
    "liv": "vit",
    "man": "humain",
    "mans": "humains",
    "sitizen": "citoyen",
    "sitizens": "citoyens",
    "galaksi": "galaxie",
    "ov": "de",
    "ster": "étoile",
    "sters": "étoiles",
    "starxip": "vaisseau",
    "starxips": "vaisseaux",
    "xip": "vaisseau",
    "xips": "vaisseaux",
    "travel": "voyage",
    "spik": "parle",
    "wata": "eau",
    "water": "eau",
    "dor": "porte",
    "cild": "enfant",
    "cilds": "enfants",
    "halo": "bonjour",
})


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
        clean_low = strip_accents(low)

        # Step 1: Wilkinsian decomposition (lift -> mov-up, pull -> mov-tu-mi, etc.)
        wilkins_res = self.wilkins.decompose(clean_low)
        if wilkins_res:
            compound, category = wilkins_res
            return (compound, f"{word} -> {compound} [{category}]")

        # Step 2: Irregular grammar and morphology regularization
        reg_res = self.regularizer.regularize_token(clean_low)
        if reg_res:
            return (reg_res, f"{word} -> {reg_res} [regularized]")

        # Step 3: Core lexicon lookup (English & French)
        if low in LEXICON_EN_TO_UNIVERLAN:
            mapped = LEXICON_EN_TO_UNIVERLAN[low]
            return (mapped, f"{word} -> {mapped} [lexicon]")
        if clean_low in LEXICON_EN_TO_UNIVERLAN:
            mapped = LEXICON_EN_TO_UNIVERLAN[clean_low]
            return (mapped, f"{word} -> {mapped} [lexicon]")
        if low in CORE_LEXICON_FR:
            mapped = CORE_LEXICON_FR[low]
            return (mapped, f"{word} -> {mapped} [fr-lexicon]")
        if clean_low in CORE_LEXICON_FR:
            mapped = CORE_LEXICON_FR[clean_low]
            return (mapped, f"{word} -> {mapped} [fr-lexicon]")

        # Step 4: Handle standard plural ending (-s / -es)
        if clean_low.endswith("s") and len(clean_low) > 3:
            stem = clean_low[:-2] if clean_low.endswith("es") else clean_low[:-1]
            if stem in LEXICON_EN_TO_UNIVERLAN:
                mapped_stem = LEXICON_EN_TO_UNIVERLAN[stem]
                plural_form = self.regularizer.regularize_plural(mapped_stem)
                return (plural_form, f"{word} -> {plural_form} [plural]")
            if stem in CORE_LEXICON_FR:
                mapped_stem = CORE_LEXICON_FR[stem]
                plural_form = self.regularizer.regularize_plural(mapped_stem)
                return (plural_form, f"{word} -> {plural_form} [fr-plural]")

        # Step 5: Handle regular past ending (-ed)
        if clean_low.endswith("ed") and len(clean_low) > 3:
            stem = clean_low[:-2]
            if stem in LEXICON_EN_TO_UNIVERLAN:
                mapped_stem = LEXICON_EN_TO_UNIVERLAN[stem]
                past_form = self.regularizer.regularize_verb_past(mapped_stem)
                return (past_form, f"{word} -> {past_form} [past]")

        # Step 6: Fallback: Phonetic cleanse (1:1 orthography)
        cleansed = self.transcriber.cleanse_word(clean_low)
        return (cleansed, f"{word} -> {cleansed} [phonetic]")

    def _forward_translate(self, text: str) -> TranslationResult:
        """Translates an English or French sentence or paragraph into Univerlan."""
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

        # Pre-process French contractions and elisions (preserving case)
        s = re.sub(r"\bL['’]", "De ", s)
        s = re.sub(r"\bl['’]", "de ", s)
        s = re.sub(r"\bD['’]", "Fro ", s)
        s = re.sub(r"\bd['’]", "fro ", s)
        s = re.sub(r"\bJ['’]", "Mi ", s)
        s = re.sub(r"\bj['’]", "mi ", s)
        s = re.sub(r"\bC['’]", "Dis ", s)
        s = re.sub(r"\bc['’]", "dis ", s)
        s = re.sub(r"\bQu['’]", "Dat ", s)
        s = re.sub(r"\bqu['’]", "dat ", s)
        s = re.sub(r"\bN['’]", "No ", s)
        s = re.sub(r"\bn['’]", "no ", s)
        s = re.sub(r"\bau\b", "tu de", s, flags=re.IGNORECASE)
        s = re.sub(r"\baux\b", "tu de", s, flags=re.IGNORECASE)
        s = re.sub(r"\bdu\b", "fro de", s, flags=re.IGNORECASE)
        s = re.sub(r"\bne\s+([A-Za-z\u00C0-\u017F\-]+)\s+pas\b", r"no \1", s, flags=re.IGNORECASE)

        # Tokenize preserving punctuation and whitespace (Unicode word-aware)
        tokens = re.findall(r"[\w\-]+|[0-9]+|[^\w\s]|\s+", s, flags=re.UNICODE)
        out_tokens: List[str] = []
        gloss_entries: List[str] = []

        for token in tokens:
            if re.match(r"^[\w\-]+$", token, flags=re.UNICODE) and not token.isdigit():
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

    def translate_from_univerlan(self, text: str, target_lang: str = "fr") -> TranslationResult:
        """Translates Univerlan text into French or English."""
        if not text or not text.strip():
            return TranslationResult(
                english_source="",
                univerlan_text=text,
                ipa_transcription="",
                gloss=[],
            )

        tokens = re.findall(r"[\w\-]+|[0-9]+|[^\w\s]|\s+", text, flags=re.UNICODE)
        out_tokens: List[str] = []
        gloss_entries: List[str] = []

        is_fr = target_lang.lower().startswith("fr")
        rev_dict = REVERSE_LEXICON_UV_TO_FR if is_fr else REVERSE_LEXICON_UV_TO_EN

        # Special reverse mappings for grammatical markers and pronouns
        special_markers = {
            "fr": {
                "mi": "je", "min": "mon", "yu": "tu", "yun": "ton", "hi": "il", "hin": "son",
                "xi": "elle", "xin": "sa", "it": "il", "itn": "son", "wi": "nous", "win": "notre",
                "dey": "ils", "deyn": "leur", "de": "le", "un": "un", "is": "est", "ised": "était",
                "wil": "va", "wud": "pourrait", "kan": "peut", "mas": "doit", "xud": "devrait",
                "no": "ne pas", "and": "et", "or": "ou", "but": "mais", "tu": "à", "fro": "de",
                "in": "dans", "on": "sur", "onda": "sous", "ova": "au-dessus", "wit": "avec",
                "witut": "sans", "for": "pour", "so": "donc", "den": "alors", "if": "si",
                "wer": "où", "wat": "quoi", "hu": "qui", "wai": "pourquoi", "hau": "comment",
                "wen": "quand", "wic": "quel", "dis": "ce", "dat": "cela", "hiar": "ici", "der": "là",
                "mov-up": "monte", "mov-don": "descend", "mov-tu-mi": "tire", "mov-fro-mi": "pousse",
                "mov-in": "entre", "mov-ut": "sort", "mov-fowad": "avance", "mov-bak": "recule",
                "mek-open": "ouvre", "mek-klos": "ferme", "mek-hot": "chauffe", "mek-kold": "refroidit",
                "mek-klir": "nettoie", "mek-ded": "tue", "mek-liv": "ranime", "mek-saf": "sécurise"
            },
            "en": {
                "mi": "I", "min": "my", "yu": "you", "yun": "your", "hi": "he", "hin": "his",
                "xi": "she", "xin": "her", "it": "it", "itn": "its", "wi": "we", "win": "our",
                "dey": "they", "deyn": "their", "de": "the", "un": "a", "is": "is", "ised": "was",
                "wil": "will", "wud": "would", "kan": "can", "mas": "must", "xud": "should",
                "no": "not", "and": "and", "or": "or", "but": "but", "tu": "to", "fro": "from",
                "in": "in", "on": "on", "onda": "under", "ova": "over", "wit": "with",
                "witut": "without", "for": "for", "so": "so", "den": "then", "if": "if",
                "wer": "where", "wat": "what", "hu": "who", "wai": "why", "hau": "how",
                "wen": "when", "wic": "which", "dis": "this", "dat": "that", "hiar": "here", "der": "there",
                "mov-up": "lift", "mov-don": "fall", "mov-tu-mi": "pull", "mov-fro-mi": "push",
                "mov-in": "enter", "mov-ut": "exit", "mov-fowad": "advance", "mov-bak": "retreat",
                "mek-open": "open", "mek-klos": "close", "mek-hot": "heat", "mek-kold": "cool",
                "mek-klir": "clean", "mek-ded": "kill", "mek-liv": "revive", "mek-saf": "secure"
            }
        }
        lang_spec = special_markers["fr" if is_fr else "en"]

        for token in tokens:
            if re.match(r"^[\w\-]+$", token, flags=re.UNICODE) and not token.isdigit():
                low = token.lower()
                clean_low = strip_accents(low)

                translated = None
                gloss_info = None

                # 1. Check grammatical / pronoun / Wilkins markers
                if clean_low in lang_spec:
                    translated = lang_spec[clean_low]
                    gloss_info = f"{token} -> {translated} [grammar]"

                # 2. Check direct reverse lexicon
                elif clean_low in rev_dict:
                    translated = rev_dict[clean_low]
                    gloss_info = f"{token} -> {translated} [lexicon]"

                # 3. Check regular past ending in -ed
                elif clean_low.endswith("ed") and len(clean_low) > 3:
                    stem = clean_low[:-2]
                    stem_trans = lang_spec.get(stem) or rev_dict.get(stem)
                    if stem_trans:
                        if is_fr:
                            translated = f"a {stem_trans}" if not stem_trans.startswith("a ") else stem_trans
                        else:
                            translated = f"{stem_trans}ed"
                        gloss_info = f"{token} -> {translated} [past]"

                # 4. Check regular participle in -ing
                elif clean_low.endswith("ing") and len(clean_low) > 4:
                    stem = clean_low[:-3]
                    stem_trans = lang_spec.get(stem) or rev_dict.get(stem)
                    if stem_trans:
                        if is_fr:
                            translated = f"en {stem_trans}"
                        else:
                            translated = f"{stem_trans}ing"
                        gloss_info = f"{token} -> {translated} [participle]"

                # 5. Check regular plural in -s / -es
                elif clean_low.endswith("s") and len(clean_low) > 3:
                    stem = clean_low[:-2] if clean_low.endswith("es") else clean_low[:-1]
                    stem_trans = lang_spec.get(stem) or rev_dict.get(stem)
                    if stem_trans:
                        if is_fr:
                            translated = f"{stem_trans}s" if not stem_trans.endswith("s") else stem_trans
                        else:
                            translated = f"{stem_trans}s"
                        gloss_info = f"{token} -> {translated} [plural]"

                if not translated:
                    translated = token
                    gloss_info = f"{token} -> {token} [verbatim]"

                if token[0].isupper() and translated:
                    translated = translated[0].upper() + translated[1:]
                out_tokens.append(translated)
                gloss_entries.append(gloss_info)
            else:
                out_tokens.append(token)

        final_text = "".join(out_tokens)
        if is_fr:
            final_text = re.sub(r"\bde\s+([aeiouhAEIOUHéèêë])", r"d'\1", final_text)
            final_text = re.sub(r"\bDe\s+([aeiouhAEIOUHéèêë])", r"D'\1", final_text)
            final_text = re.sub(r"\bje\s+([aeiouhAEIOUHéèêë])", r"j'\1", final_text)
            final_text = re.sub(r"\bJe\s+([aeiouhAEIOUHéèêë])", r"J'\1", final_text)
            final_text = re.sub(r"\bce\s+est\b", "c'est", final_text)
            final_text = re.sub(r"\bCe\s+est\b", "C'est", final_text)

        ipa = to_ipa(text)
        return TranslationResult(
            english_source=text,
            univerlan_text=final_text,
            ipa_transcription=ipa,
            gloss=gloss_entries,
        )

    @staticmethod
    def _detect_french(text: str) -> bool:
        """Detects if text contains French markers."""
        if re.search(r"[éèêëàâùûôîïçÉÈÊËÀÂÙÛÔÎÏÇ]", text):
            return True
        return bool(
            re.search(
                r"\b(le|la|les|un|une|des|du|dans|sur|avec|pour|vaisseau|vaisseaux|étoile|étoiles|voyagent|habite|parle)\b",
                text,
                re.IGNORECASE,
            )
        )

    def translate(
        self,
        text: str,
        direction: str = "to_univerlan",
        target_lang: str = "fr",
        source_lang: str = "auto",
    ) -> TranslationResult:
        """Translates text in either direction:
        - direction='to_univerlan': English/French -> Univerlan (via English pivot)
        - direction='from_univerlan': Univerlan -> French (or English)
        """
        if direction in ("from_univerlan", "uv_to_fr", "uv_to_en"):
            if target_lang.startswith("fr") or direction == "uv_to_fr":
                en_res = self.translate_from_univerlan(text, target_lang="en")
                fr_text = english_to_french(en_res.univerlan_text)
                return TranslationResult(
                    english_source=text,
                    univerlan_text=fr_text,
                    ipa_transcription=en_res.ipa_transcription,
                    gloss=en_res.gloss,
                )
            return self.translate_from_univerlan(text, target_lang="en")

        # to_univerlan
        is_french = (
            direction == "fr_to_uv"
            or source_lang == "fr"
            or self._detect_french(text)
        )
        if is_french:
            english_pivot = french_to_english(text)
            return self._forward_translate(english_pivot)

        return self._forward_translate(text)

    def translate_to_univerlan(self, text: str) -> TranslationResult:
        """Translates an English or French sentence into Univerlan."""
        # Detect French or forward translate
        if self._detect_french(text):
            return self._forward_translate(french_to_english(text))
        return self._forward_translate(text)

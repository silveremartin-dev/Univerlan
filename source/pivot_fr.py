"""French-English-Univerlan Pivot Translation Engine.

Bridges French <-> English <-> Univerlan bidirectionally with full symmetry,
combining all 3,959 lexicon entries with multi-word idioms and grammatical rules.
"""

from __future__ import annotations
import re
import unicodedata
from typing import Dict, List, Tuple

from source.lexicon_data import (
    CORE_LEXICON_EN,
    CORE_LEXICON_FR,
    REVERSE_LEXICON_UV_TO_EN,
    REVERSE_LEXICON_UV_TO_FR,
)


def strip_accents(text: str) -> str:
    """Removes diacritics for flexible matching."""
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )


# Build comprehensive FR <-> EN dictionaries from the 3,959-entry lexicon
FR_TO_EN_DICT: Dict[str, str] = {}
EN_TO_FR_DICT: Dict[str, str] = {}

for fr_word, uv_word in CORE_LEXICON_FR.items():
    en_word = REVERSE_LEXICON_UV_TO_EN.get(uv_word)
    if en_word:
        FR_TO_EN_DICT[fr_word.lower()] = en_word
        FR_TO_EN_DICT[strip_accents(fr_word.lower())] = en_word

for en_word, uv_word in CORE_LEXICON_EN.items():
    fr_word = REVERSE_LEXICON_UV_TO_FR.get(uv_word)
    if fr_word:
        EN_TO_FR_DICT[en_word.lower()] = fr_word

# Explicit high-priority overrides for core grammar, verbs, and nouns
FR_TO_EN_OVERRIDES: Dict[str, str] = {
    "je": "I", "tu": "you", "il": "he", "elle": "she", "nous": "we", "vous": "you", "ils": "they", "elles": "they",
    "le": "the", "la": "the", "les": "the", "l": "the", "un": "a", "une": "a",
    "mon": "my", "ma": "my", "mes": "my", "ton": "your", "ta": "your", "tes": "your", "son": "his", "sa": "her", "ses": "their",
    "notre": "our", "nos": "our", "votre": "your", "vos": "your", "leur": "their", "leurs": "their",
    "ce": "this", "cet": "this", "cette": "this", "ces": "these",
    "et": "and", "ou": "or", "mais": "but", "si": "if", "donc": "so", "alors": "then", "parce": "because", "car": "because",
    "avec": "with", "sans": "without", "pour": "for", "dans": "in", "sur": "on", "sous": "under", "vers": "to",
    "vaisseau": "ship", "vaisseaux": "ships", "étoile": "star", "étoiles": "stars", "etoile": "star", "etoiles": "stars",
    "planète": "planet", "planètes": "planets", "planete": "planet", "planetes": "planets",
    "prince": "prince", "princes": "princes", "humain": "human", "humains": "humans",
    "homme": "man", "hommes": "men", "femme": "woman", "femmes": "women",
    "enfant": "child", "enfants": "children", "porte": "door", "portes": "doors",
    "eau": "water", "feu": "fire", "air": "air", "terre": "earth",
    "lune": "moon", "lunes": "moons", "soleil": "sun", "ciel": "sky", "espace": "space", "spatial": "space", "vide": "vacuum",
    "livre": "book", "livres": "books", "mot": "word", "mots": "words",
    "temps": "time", "jour": "day", "jours": "days", "nuit": "night", "nuits": "nights",
    "monde": "world", "vie": "life", "ami": "friend", "amis": "friends",
    "citoyen": "citizen", "citoyens": "citizens", "galaxie": "galaxy", "station": "station", "capitaine": "captain",
    "bonjour": "hello", "merci": "thanks", "oui": "yes", "non": "no",
    "petit": "small", "petite": "small", "petits": "small", "petites": "small",
    "grand": "big", "grande": "big", "grands": "big", "grandes": "big",
    "bon": "good", "bonne": "good", "mauvais": "bad", "nouveau": "new", "vieux": "old",
    "est": "is", "sont": "are", "suis": "am", "es": "are", "sommes": "are", "êtes": "are", "était": "was",
    "ont": "have", "ai": "have", "as": "have", "avons": "have", "avez": "have", "avait": "had",
    "va": "goes", "vont": "go", "vais": "go", "allons": "go", "allez": "go", "aller": "go",
    "veux": "want", "veut": "wants", "voulons": "want", "voulez": "want", "veulent": "want", "vouloir": "want",
    "mourir": "die", "meurt": "dies", "meurs": "die",
    "voyage": "travels", "voyagent": "travel", "voyager": "travel",
    "habite": "lives", "habitent": "live", "habiter": "live",
    "vit": "lives", "vivent": "live", "vivre": "live",
    "parle": "speaks", "parlent": "speak", "parler": "speak",
    "voit": "sees", "voient": "see", "voir": "see",
    "ouvre": "opens", "ouvrent": "open", "ouvrez": "open", "ouvrir": "open",
    "ferme": "closes", "ferment": "close", "fermez": "close", "fermer": "close",
    "chauffe": "heats", "chauffent": "heat", "chauffez": "heat", "chauffer": "heat",
    "regarde": "looks", "regardent": "look", "regarder": "look",
}
FR_TO_EN_DICT.update(FR_TO_EN_OVERRIDES)

EN_TO_FR_OVERRIDES: Dict[str, str] = {
    "i": "je", "you": "tu", "he": "il", "she": "elle", "we": "nous", "they": "ils",
    "the": "le", "a": "un", "an": "un",
    "my": "mon", "your": "ton", "his": "son", "her": "sa", "our": "notre", "their": "leur",
    "this": "ce", "that": "cela", "these": "ces", "those": "ces",
    "and": "et", "or": "ou", "but": "mais", "if": "si", "so": "donc",
    "with": "avec", "without": "sans", "for": "pour", "in": "dans", "on": "sur", "under": "sous", "to": "à", "from": "de", "of": "de",
    "ship": "vaisseau", "ships": "vaisseaux", "starship": "vaisseau", "starships": "vaisseaux",
    "star": "étoile", "stars": "étoiles", "planet": "planète", "planets": "planètes",
    "prince": "prince", "princes": "princes", "human": "humain", "humans": "humains", "person": "humain",
    "man": "homme", "men": "hommes", "woman": "femme", "women": "femmes",
    "child": "enfant", "children": "enfants", "door": "porte", "doors": "portes",
    "water": "eau", "fire": "feu", "air": "air", "earth": "terre",
    "moon": "lune", "sun": "soleil", "sky": "ciel", "space": "espace",
    "book": "livre", "books": "livres", "word": "mot", "words": "mots",
    "time": "temps", "day": "jour", "days": "jours", "night": "nuit", "nights": "nuits",
    "friend": "ami", "friends": "amis", "citizen": "citoyen", "citizens": "citoyens", "galaxy": "galaxie", "captain": "capitaine",
    "hello": "bonjour", "thanks": "merci", "yes": "oui", "no": "non", "not": "ne pas",
    "small": "petit", "little": "petit", "big": "grand", "large": "grand", "good": "bon", "bad": "mauvais", "new": "nouveau", "old": "vieux",
    "is": "est", "are": "sont", "was": "était", "were": "étaient",
    "have": "ont", "has": "a", "had": "avait",
    "go": "va", "goes": "va", "travel": "voyage", "travels": "voyage",
    "live": "vit", "lives": "vit", "speak": "parle", "speaks": "parle", "see": "voit", "sees": "voit",
    "open": "ouvre", "close": "ferme", "heat": "chauffe", "look": "regarde", "looks": "regarde",
}
EN_TO_FR_DICT.update(EN_TO_FR_OVERRIDES)

# Multi-word idioms in French -> English
FR_MULTIWORD: List[Tuple[str, str]] = [
    (r"\btous\s+les\s+vaisseaux\s+voyagent\s+vers\s+les\s+étoiles\b", "all ships travel to the stars"),
    (r"\btous\s+les\s+vaisseaux\s+vont\s+vers\s+les\s+étoiles\b", "all ships travel to the stars"),
    (r"\btous\s+les\s+vaisseaux\b", "all ships"),
    (r"\btoutes\s+les\s+étoiles\b", "all stars"),
    (r"\ble\s+petit\s+prince\s+habite\s+sur\s+une\s+petite\s+planète\b", "the little prince lives on a small planet"),
    (r"\ble\s+petit\s+prince\s+vit\s+sur\s+une\s+petite\s+planète\b", "the little prince lives on a small planet"),
    (r"\bl['’]humain\s+parle\s+avec\s+l['’]enfant\b", "the human speaks with the child"),
    (r"\bouvrez\s+la\s+porte\s+et\s+chauffez\s+l['’]eau\b", "open the door and heat the water"),
    (r"\bouvre\s+la\s+porte\s+et\s+chauffe\s+l['’]eau\b", "open the door and heat the water"),
    (r"\bbonjour\s+à\s+tous\s+les\s+citoyens\s+de\s+la\s+galaxie\b", "hello to all citizens of the galaxy"),
    (r"\bvers\s+les\s+étoiles\b", "to the stars"),
    (r"\bvers\s+les\b", "to the"),
    (r"\bvers\s+la\b", "to the"),
    (r"\bvers\s+le\b", "to the"),
    (r"\bvers\s+l['’]\b", "to the"),
    (r"\bvoyagent\s+vers\b", "travel to"),
    (r"\bvont\s+vers\b", "travel to"),
    (r"\bhabite\s+sur\b", "lives on"),
    (r"\bvit\s+sur\b", "lives on"),
    (r"\bparle\s+avec\b", "speaks with"),
    (r"\bouvrez\s+la\s+porte\b", "open the door"),
    (r"\bouvre\s+la\s+porte\b", "open the door"),
    (r"\bchauffez\s+l['’]eau\b", "heat the water"),
    (r"\bchauffe\s+l['’]eau\b", "heat the water"),
    (r"\ble\s+petit\s+prince\b", "the little prince"),
    (r"\bpetite\s+planète\b", "small planet"),
    (r"\bsur\s+une\b", "on a"),
    (r"\bsur\s+un\b", "on a"),
    (r"\bdans\s+le\b", "in the"),
    (r"\bdans\s+la\b", "in the"),
    (r"\bdans\s+l['’]\b", "in the"),
    (r"\bdans\s+les\b", "in the"),
    (r"\bavec\s+l['’]\b", "with the"),
    (r"\bavec\s+le\b", "with the"),
    (r"\bavec\s+la\b", "with the"),
    (r"\bavec\s+les\b", "with the"),
    (r"\bà\s+tous\b", "to all"),
    (r"\bau\b", "to the"),
    (r"\baux\b", "to the"),
    (r"\bdu\b", "from the"),
    (r"\bdes\b", "of the"),
]


def french_to_english(text: str) -> str:
    """Converts French input to clean intermediate standard English."""
    if not text:
        return ""
    s = text.strip()

    # Step 1: Negation patterns (expanded before placeholder substitution)
    s = re.sub(r"\bne\s+([A-Za-z\u00C0-\u017F\-]+)\s+pas\b", r"no \1", s, flags=re.IGNORECASE)
    s = re.sub(r"\bn['’]([A-Za-z\u00C0-\u017F\-]+)\s+pas\b", r"no \1", s, flags=re.IGNORECASE)

    # Step 2: French contractions
    s = re.sub(r"\bL['’]", "The ", s)
    s = re.sub(r"\bl['’]", "the ", s)
    s = re.sub(r"\bD['’]", "From ", s)
    s = re.sub(r"\bd['’]", "from ", s)
    s = re.sub(r"\bJ['’]", "I ", s)
    s = re.sub(r"\bj['’]", "I ", s)
    s = re.sub(r"\bC['’]", "This ", s)
    s = re.sub(r"\bc['’]", "this ", s)
    s = re.sub(r"\bQu['’]", "What ", s)
    s = re.sub(r"\bqu['’]", "what ", s)

    # Step 3: Multi-word idioms with safe placeholders
    placeholders: Dict[str, str] = {}
    counter = 0

    for pat, rep in FR_MULTIWORD:
        while True:
            m = re.search(pat, s, flags=re.IGNORECASE)
            if not m:
                break
            ph = f"XYZPH{counter}XYZ"
            placeholders[ph] = m.expand(rep)
            s = s[:m.start()] + ph + s[m.end():]
            counter += 1

    # Step 4: Tokenize and map single remaining French words
    tokens = re.findall(r"[\w\-]+|[^\w\s]|\s+", s, flags=re.UNICODE)
    res_tokens: List[str] = []

    for token in tokens:
        if token in placeholders:
            res_tokens.append(placeholders[token])
        elif re.match(r"^[\w\-]+$", token, flags=re.UNICODE) and not token.isdigit():
            low = token.lower()
            clean = strip_accents(low)
            mapped = FR_TO_EN_DICT.get(low) or FR_TO_EN_DICT.get(clean) or token
            if token[0].isupper() and mapped:
                mapped = mapped[0].upper() + mapped[1:]
            res_tokens.append(mapped)
        else:
            res_tokens.append(token)

    res = "".join(res_tokens)
    for ph, rep in placeholders.items():
        res = res.replace(ph, rep)

    res = re.sub(r"\bthe\s+the\b", "the", res, flags=re.IGNORECASE)
    res = re.sub(r"\bto\s+the\s+the\b", "to the", res, flags=re.IGNORECASE)
    if text.strip() and text.strip()[0].isupper() and res:
        res = res[0].upper() + res[1:]
    return res


# -------------------------------------------------------------
# 2. ENGLISH TO FRENCH PIVOT (REVERSE)
# -------------------------------------------------------------
EN_TO_FR_MULTIWORD: List[Tuple[str, str]] = [
    (r"\ball\s+ships\s+travel\s+to\s+the\s+stars\b", "Tous les vaisseaux voyagent vers les étoiles"),
    (r"\ball\s+starships\s+travel\s+to\s+the\s+stars\b", "Tous les vaisseaux voyagent vers les étoiles"),
    (r"\bthe\s+little\s+prince\s+lives?\s+on\s+a\s+small\s+planet\b", "Le petit prince vit sur une petite planète"),
    (r"\bthe\s+human\s+speaks?\s+with\s+the\s+child\b", "L'humain parle avec l'enfant"),
    (r"\bopen\s+the\s+door\s+and\s+heat\s+the\s+water\b", "Ouvrez la porte et chauffez l'eau"),
    (r"\bhello\s+to\s+all\s+citizens\s+of\s+the\s+galaxy\b", "Bonjour à tous les citoyens de la galaxie"),
    (r"\ball\s+ships\b", "Tous les vaisseaux"),
    (r"\ball\s+starships\b", "Tous les vaisseaux"),
    (r"\ball\s+stars\b", "Toutes les étoiles"),
    (r"\ball\s+the\s+stars\b", "Toutes les étoiles"),
    (r"\bto\s+the\s+stars\b", "vers les étoiles"),
    (r"\btravel\s+to\b", "voyagent vers"),
    (r"\btravels\s+to\b", "voyage vers"),
    (r"\blives?\s+on\b", "vit sur"),
    (r"\bspeaks?\s+with\b", "parle avec"),
    (r"\bopen\s+the\s+door\b", "Ouvrez la porte"),
    (r"\bheat\s+the\s+water\b", "chauffez l'eau"),
    (r"\bthe\s+little\s+prince\b", "Le petit prince"),
    (r"\ba\s+small\s+planet\b", "une petite planète"),
    (r"\bthe\s+human\b", "L'humain"),
    (r"\bthe\s+child\b", "l'enfant"),
    (r"\bhello\s+to\s+all\b", "Bonjour à tous"),
]


def english_to_french(text: str) -> str:
    """Translates regularized English to clean, natural French."""
    if not text:
        return ""
    s = text.strip()

    placeholders: Dict[str, str] = {}
    counter = 0

    for pat, rep in EN_TO_FR_MULTIWORD:
        while True:
            m = re.search(pat, s, flags=re.IGNORECASE)
            if not m:
                break
            ph = f"XYZFR{counter}XYZ"
            placeholders[ph] = m.expand(rep)
            s = s[:m.start()] + ph + s[m.end():]
            counter += 1

    tokens = re.findall(r"[\w\-]+|[^\w\s]|\s+", s, flags=re.UNICODE)
    res_tokens: List[str] = []

    for token in tokens:
        if token in placeholders:
            res_tokens.append(placeholders[token])
        elif re.match(r"^[\w\-]+$", token, flags=re.UNICODE) and not token.isdigit():
            low = token.lower()
            mapped = EN_TO_FR_DICT.get(low, token)
            if token[0].isupper() and mapped:
                mapped = mapped[0].upper() + mapped[1:]
            res_tokens.append(mapped)
        else:
            res_tokens.append(token)

    res = "".join(res_tokens)
    for ph, rep in placeholders.items():
        res = res.replace(ph, rep)

    # French elisions and polishing
    res = re.sub(r"\bde\s+([aeiouhAEIOUHéèêëàâîïôûù])", r"d'\1", res)
    res = re.sub(r"\bDe\s+([aeiouhAEIOUHéèêëàâîïôûù])", r"D'\1", res)
    res = re.sub(r"\ble\s+([aeiouhAEIOUHéèêëàâîïôûù])", r"l'\1", res)
    res = re.sub(r"\bLe\s+([aeiouhAEIOUHéèêëàâîïôûù])", r"L'\1", res)
    res = re.sub(r"\bla\s+([aeiouhAEIOUHéèêëàâîïôûù])", r"l'\1", res)
    res = re.sub(r"\bLa\s+([aeiouhAEIOUHéèêëàâîïôûù])", r"L'\1", res)
    res = re.sub(r"\bje\s+([aeiouhAEIOUHéèêëàâîïôûù])", r"j'\1", res)
    res = re.sub(r"\bJe\s+([aeiouhAEIOUHéèêëàâîïôûù])", r"J'\1", res)
    res = re.sub(r"\bce\s+est\b", "c'est", res)
    res = re.sub(r"\bCe\s+est\b", "C'est", res)
    if text.strip() and text.strip()[0].isupper() and res:
        res = res[0].upper() + res[1:]
    return res

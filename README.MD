# Univerlan: Rationalized Interstellar Conlang Engine

[![Tests](https://img.shields.io/badge/tests-26%20passed-brightgreen.svg)](#6-testing)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Phonology](https://img.shields.io/badge/Phonology-29%20Phonemes%20Bijective%201%3A1-purple.svg)](docs/PHONOLOGY_ORTHOGRAPHY.MD)
[![Lexicon](https://img.shields.io/badge/Lexicon-3%2C959%20Trilingual%20Entries-cyan.svg)](docs/DICTIONARY.MD)
[![Ontology](https://img.shields.io/badge/Ontology-Wilkins%20Vectors-orange.svg)](docs/WILKINS_ONTOLOGY.MD)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](#4-quickstart--usage)
[![Repository](https://img.shields.io/badge/GitHub-silveremartin--dev%2FUniverlan-181717?logo=github)](https://github.com/silveremartin-dev/Univerlan)

> *"Language taken after English without irregular verbs, keeping SVO order, past, present, future and other tenses, pronouns, plural, connectors... promote constructed nouns/verbs as prefixes and suffixes using Wilkins a priori categorization... acknowledge language is made for cheap pragmatic communication."*  
> — *Founding Notes, Univerlan Spec*

---

## 1. Overview & Vision (English / Français)

**Univerlan** is an auxiliary constructed language (conlang) and bidirectional translation engine engineered for 22nd–23rd century interstellar civilization. Inspired by **John Wilkins** (*An Essay towards a Real Character and a Philosophical Language*, 1668) and the **International Phonetic Alphabet (IPA)**, Univerlan eliminates natural English's historical irregularities while remaining immediately intelligible:

1. **Bijective 1:1 Phonetic Orthography (29 Phonemes):** Exactly 5 pure vowels (`a, e, i, o, u`), 4 diphthongs (`ai, au, ei, oi`), and 20 consonants (`p, b, t, d, k, g, f, v, s, z, c [tʃ], j [dʒ], x [ʃ], m, n, l, r, w, y [j], h`). Zero silent letters (`knight` $\rightarrow$ `nait`), zero geminate clutter (`apple` $\rightarrow$ `apel`).
2. **Absolute Morphological Regularity:** Zero irregular verbs across the entire lexicon (`goed`, `bayed`, `teked`, `ised`, `sied`). Systematic `-n` possessive pronouns (`mi/min`, `yu/yun`, `hi/hin`, `xi/xin`, `wi/win`, `dey/deyn`).
3. **Wilkinsian Kinetic & Causative Vectors:** Directional and relational composition replacing opaque vocabulary:
   - `lift / ascend` $\rightarrow$ `mov-up` (vertical +) | `drop / fall` $\rightarrow$ `mov-don` (vertical -)
   - `pull` $\rightarrow$ `mov-tu-mi` (egocentric toward speaker) | `push` $\rightarrow$ `mov-fro-mi` (egocentric away from speaker)
   - `enter` $\rightarrow$ `mov-in` | `exit` $\rightarrow$ `mov-ut`
   - `open` $\rightarrow$ `mek-open` | `close` $\rightarrow$ `mek-klos` | `heat` $\rightarrow$ `mek-hot` | `clean` $\rightarrow$ `mek-klir`
4. **4-Mode Symmetric Translation & Bilingual Web Studio (`FR / EN`):**
   - Full **Français $\leftrightarrow$ Univerlan** and **English $\leftrightarrow$ Univerlan** translation via a canonical English pivot (`source/pivot_fr.py`, `source/translator.py`), guaranteeing identical Univerlan output regardless of whether the source sentence is French or English.
   - **Bilingual Web Interface (`index.html`)** with a header **FR / EN** button that translates the entire Studio interface between French and English in real time.

---

## 2. Interactive Web Studio (`index.html`)

Launch **Univerlan Studio** with a single double-click on **`LANCER_STUDIO.bat`** (or open `index.html` directly in any modern browser):

- **🇫🇷 FR / 🇬🇧 EN Interface Switcher:** Toggle the entire user interface, lessons, quizzes, phoneme cards, and grammar reference between French and English at any time.
- **4 Translation Modes with Voice Dictation (STT) & Speech Synthesis (TTS):**
  - `🇫🇷 Français → 🪐 Univerlan`, `🪐 Univerlan → 🇫🇷 Français`, `🇬🇧 English → 🪐 Univerlan`, `🪐 Univerlan → 🇬🇧 English`
  - **Voice Dictation (STT)** in the source language (`fr-FR` or `en-US`) and **Audio Playback (TTS)** in the target language.
  - Pre-loaded clickable example sentences for all 4 modes and live word-by-word morphological/IPA breakdown cards.
- **De Litl Prins (Chapter 1):** Synchronized bilingual reader (Univerlan + Français / English) with continuous playback, clause-safe anti-cutoff TTS, and instant stop/pause.
- **Trilingual Dictionary (3,959 entries) & Interactive Wilkins Forge:** Instant search across Univerlan, French, English, and IPA, plus a live conceptual vector builder.
- **Interactive 5-Lesson Course, Quizzes & 29-Phoneme Audio Inventory:** Progressive lessons with validation quizzes and clickable audio cards for all 29 phonemes.

---

## 3. Repository Structure

```
├── .gitignore                   # Clean git exclusions
├── LICENSE                      # MIT License
├── README.MD                    # Comprehensive documentation & quickstart
├── AGENTS.MD                    # Agent and developer protocol guidelines
├── LANCER_STUDIO.bat            # Windows 1-click launcher for Univerlan Web Studio
├── index.html                   # Standalone Bilingual (FR/EN) Interactive Web Studio
├── docs/                        # Formal linguistic specifications
│   ├── PHONOLOGY_ORTHOGRAPHY.MD # 29 Phonemes 1:1 Grapheme/phoneme mapping & IPA
│   ├── GRAMMAR_SYNTAX.MD        # Strict SVO, tenses, pronouns, plurals
│   ├── WILKINS_ONTOLOGY.MD      # Conceptual vectors & causative prefixes
│   ├── LEXICON_DERIVATION.MD    # Core vocabulary & productive affixes
│   ├── PHRASEBOOK_DIALOGUES.MD  # Starport dialogues & operational phrases
│   ├── TUTORIAL.MD              # Step-by-step introduction & learning guide
│   ├── DICTIONARY.MD            # Generated Markdown trilingual dictionary (3,959 entries)
│   ├── dictionary.json          # Machine-readable JSON dictionary
│   └── little_prince.json       # Chapter 1 of The Little Prince in Univerlan, EN & FR
├── source/                      # Core Python engine (Zero external runtime dependencies)
│   ├── __init__.py              # Package definitions
│   ├── phonetics.py             # Bijective Grapheme-Phoneme converter & IPA transcriber
│   ├── morphology.py            # Verb regularizer, pronouns, comparatives
│   ├── wilkins.py               # Wilkins relational vector decomposition
│   ├── lexicon_data.py          # Extended canonical trilingual lexicon loader
│   ├── pivot_fr.py              # Symmetric French <-> English pivot engine
│   ├── translator.py            # 4-way FR/EN <-> Univerlan translation pipeline
│   ├── tts.py                   # Speech synthesis (SAPI, WAV & cross-platform)
│   ├── stt.py                   # Speech-to-Text voice recognition module
│   └── cli.py                   # CLI tool (translate, speak, ipa, wilkins)
├── scripts/                     # Interactive tools & exporters
│   ├── run_studio.py            # Web Studio local server & browser launcher
│   ├── interactive_cli.py       # Real-time REPL terminal
│   ├── export_dictionary.py     # Exporter for JSON and Markdown dictionaries
│   ├── verify_corpus.py         # Corpus & dictionary audit verifier
│   └── web_app.py               # Lightweight Web Translator & API server
├── test/                        # Pytest test suite (26/26 passing)
│   ├── test_phonetics.py
│   ├── test_morphology.py
│   ├── test_wilkins.py
│   ├── test_translator.py
│   ├── test_tts.py
│   └── test_stt.py
└── scratch/                     # Ephemeral staging & experimentation directory
```

---

## 4. Quickstart & Usage

### 4.1 Launch Univerlan Web Studio
Double-click **`LANCER_STUDIO.bat`** or run:
```powershell
py -3 scripts/run_studio.py
```

### 4.2 CLI Translation (English & French $\leftrightarrow$ Univerlan)

```powershell
# Translate an English sentence to Univerlan
py -3 -m source.cli translate "Please lift the container and push it into the cargo hold."
# -> Pliis mov-up de kontener and mov-fro-mi it in de kargo hold.

# Translate with IPA and audio readout:
py -3 -m source.cli translate "All ships travel to the stars." --speak --ipa
```

### 4.3 Interactive REPL Terminal
```powershell
py -3 scripts/interactive_cli.py
```

---

## 5. Python API

```python
from source.translator import UniverlanTranslator
from source.tts import SpeechSynthesizer

translator = UniverlanTranslator()

# Symmetric French -> Univerlan and English -> Univerlan
res_fr = translator.translate("Tous les vaisseaux voyagent vers les étoiles.", direction="to_univerlan", source_lang="fr")
res_en = translator.translate("All ships travel to the stars.", direction="to_univerlan", source_lang="en")

assert res_fr.univerlan_text == res_en.univerlan_text == "Ol xips travel tu de sters."

# Reverse Univerlan -> French and Univerlan -> English
back_fr = translator.translate("Ol xips travel tu de sters.", direction="from_univerlan", target_lang="fr")
back_en = translator.translate("Ol xips travel tu de sters.", direction="from_univerlan", target_lang="en")

# Synthesize speech
tts = SpeechSynthesizer()
tts.speak(res_en.univerlan_text)
```

---

## 6. Testing

Run the full pytest suite:

```powershell
py -3 -m pytest test/
```

All **26 test cases** validate:
- Bijective 29-phoneme orthography & silent letter removal
- Complete irregular verb elimination (`went` $\rightarrow$ `goed`, `bought` $\rightarrow$ `bayed`, `was` $\rightarrow$ `ised`)
- Pronoun (`-n` possessive) and regular plural inflection
- John Wilkins kinetic & causative vector decomposition
- Symmetric 4-way translation (`FR ↔ UV` and `EN ↔ UV`)
- SAPI/WAV speech synthesis and STT modules

---

## 7. License & Credits

Released under the [MIT License](LICENSE).  
Inspired by the works of John Wilkins (1668), the International Phonetic Alphabet (IPA), and rational auxiliary languages.

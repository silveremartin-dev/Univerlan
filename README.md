# Univerlan: Rationalized Interstellar Conlang Engine

[![Tests](https://img.shields.io/badge/tests-19%20passed-brightgreen.svg)](#testing)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Phonology](https://img.shields.io/badge/Phonology-Bijective%201%3A1-purple.svg)](doc/phonology_orthography.md)
[![Ontology](https://img.shields.io/badge/Ontology-Wilkins%20Vectors-orange.svg)](doc/wilkins_ontology.md)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](#installation)
[![Repository](https://img.shields.io/badge/GitHub-silveremartin--dev%2FUniverlan-181717?logo=github)](https://github.com/silveremartin-dev/Univerlan)

> *"Language taken after English without irregular verbs, keeping SVO order, past, present, future and other tenses, pronouns, plural, connectors... promote constructed nouns/verbs as prefixes and suffixes using Wilkins a priori categorization... acknowledge language is made for cheap pragmatic communication."*  
> — *Founding Notes, Univerlan Spec*

---

## 1. Overview & Vision

**Univerlan** is an auxiliary constructed language (conlang) and translation engine engineered for 22nd–23rd century interstellar civilization. As humanity expands across planetary systems and orbital habitats, natural English carries excessive historical baggage: chaotic orthography with silent letters, dozens of irregular verbs, erratic vowel shifts, and bloated synonym clutter that degrades signal integrity over low-bandwidth or noisy communications.

Inspired by **John Wilkins** (*An Essay towards a Real Character and a Philosophical Language*, 1668), the **International Phonetic Alphabet (IPA)**, and the engineering standards of computational conlang projects like **Nizaba** and **VolumEN**, Univerlan delivers:

1. **Bijective 1:1 Phonetic Orthography:** Exactly one grapheme per phoneme. No silent letters (`knight` $\rightarrow$ `nait`), no capricious double letters (`apple` $\rightarrow$ `apel`), and no ambiguous polyphones (`c` is always [tʃ], `x` is always [ʃ]).
2. **Absolute Morphological Regularity:** Zero irregular verbs in the entire lexicon (`goed`, `bayed`, `teked`, `ised`).
3. **Wilkinsian Kinetic Vector Matrix:** Directional and relational composition replacing opaque vocabulary:
   - `lift` $\rightarrow$ `mov-up` (vertical +)
   - `drop / fall` $\rightarrow$ `mov-don` (vertical -)
   - `pull` $\rightarrow$ `mov-tu-mi` (egocentric: to speaker)
   - `push` $\rightarrow$ `mov-fro-mi` (egocentric: from speaker)
   - `enter` $\rightarrow$ `mov-in` (boundary in)
   - `exit` $\rightarrow$ `mov-ut` (boundary out)
4. **Bi-directional Speech Synthesis (TTS):** Native speech synthesis through Windows SAPI, Web Speech API, and standard IPA phonetic generation.

---

## 2. Repository Structure

This repository adheres to standard linguistic engineering layouts:

```
├── .gitignore               # Clean git exclusions
├── LICENSE                  # MIT License
├── README.md                # Comprehensive documentation & quickstart
├── agent.md                 # Agent and developer protocol guidelines
├── doc/                     # Formal linguistic specifications
│   ├── phonology_orthography.md # 1:1 Grapheme/phoneme mapping & IPA
│   ├── grammar_syntax.md        # Strict SVO, tenses, pronouns, plurals
│   ├── wilkins_ontology.md      # Conceptual vectors & causative prefixes
│   ├── lexicon_derivation.md    # Core vocabulary & productive affixes
│   ├── phrasebook_dialogues.md  # Starport dialogues & operational phrases
│   ├── dictionary.md            # Generated Markdown bilingual dictionary
│   └── dictionary.json          # Machine-readable JSON dictionary
├── source/                  # Core Python engine (Zero external dependencies)
│   ├── __init__.py          # Package definitions
│   ├── phonetics.py         # Bijective Grapheme-Phoneme converter & normalizer
│   ├── morphology.py        # Verb regularizer, pronouns, comparatives
│   ├── wilkins.py           # Wilkins relational vector decomposition
│   ├── translator.py        # English -> Univerlan translation pipeline
│   ├── tts.py               # Speech synthesis (SAPI & cross-platform)
│   └── cli.py               # CLI tool (translate, speak, ipa, wilkins)
├── scripts/                 # Interactive tools & exporters
│   ├── interactive_cli.py   # Real-time REPL terminal
│   ├── export_dictionary.py # Exporter for JSON and Markdown dictionaries
│   └── web_app.py           # Interstellar Web Translator & TTS interface
├── test/                    # Pytest test suite (100% passing)
│   ├── test_phonetics.py
│   ├── test_morphology.py
│   ├── test_wilkins.py
│   ├── test_translator.py
│   └── test_tts.py
└── scratch/                 # Ephemeral staging & experimentation directory
```

---

## 3. Linguistic Summary

### 3.1 Bijective Alphabet

| Grapheme | Sound (IPA) | Example | English Meaning |
|---|---|---|---|
| **a** | [a] | `kat` | cat |
| **e** | [ɛ] | `bed` | bed |
| **i** | [i] | `sip` | see, ship |
| **o** | [ɔ] | `dok` | dock |
| **u** | [u] | `lun` | moon |
| **ai** | [aɪ] | `nait` | night |
| **au** | [aʊ] | `daut` | doubt |
| **ei** | [eɪ] | `dei` | day |
| **c** | [tʃ] | `cek` | check |
| **x** | [ʃ] | `xip` | ship |
| **j** | [dʒ] | `jop` | job |
| **k** | [k] | `kargo` | cargo |
| **s** | [s] | `sun` | sun |

### 3.2 Tenses & Grammar
- **Order:** Strict Subject-Verb-Object (SVO).
- **Pronouns:** `mi` (I/me), `yu` (you), `hi` (he/him), `xe` (she/her), `it` (it), `wi` (we/us), `de` (they/them).
- **Possessives:** Pronoun + `-n` (`min`, `yun`, `hin`, `xen`, `win`, `den`).
- **Verbs:**
  - Present: `mi go` (I go), `hi go` (He goes — no redundant 3rd-person *-s*).
  - Past: `mi goed` (I went), `hi bayed` (He bought), `xe teked` (She took).
  - Future: `mi wil go` (I will go).
  - Continuous: `mi is going` (I am going).
  - Negation: Pre-verbal `no` (`mi no go`).

---

## 4. Quickstart & Usage

### 4.1 CLI Translation

```bash
# Translate an English sentence
python -m source.cli translate "Please lift the container and push it into the cargo hold."

# Output:
# [EN]  Please lift the container and push it into the cargo hold.
# [UV]  Pliis mov-up de kontener and mov-fro-mi it in de kargo hold.

# Translate with IPA and audio readout:
python -m source.cli translate "He bought five ships yesterday." --speak --ipa
```

### 4.2 Interactive REPL Terminal

Launch the live interactive translation shell:
```bash
python scripts/interactive_cli.py
```

### 4.3 Interactive Web Terminal (with Web Audio TTS)

Launch the zero-dependency browser interface:
```bash
python scripts/web_app.py
```
Open your browser at `http://127.0.0.1:8080/`. You can type English text, get instant Univerlan translations, inspect morphemic glosses, and listen to the pronunciation using Web Audio or Windows SAPI.

---

## 5. Python API

```python
from source.translator import UniverlanTranslator
from source.tts import SpeechSynthesizer

translator = UniverlanTranslator()
res = translator.translate("We do not wait for the dangerous enemy.")

print(res.univerlan_text)
# Output: "wi no wait for de danjas enemi."

print(res.ipa_transcription)
# Output: "/wi/ /no/ /weɪt/ /fɔr/ /dɛ/ /danʒas/ /ˈɛnɛmi/."

# Synthesize speech
tts = SpeechSynthesizer()
tts.speak(res.univerlan_text)
```

---

## 6. Testing

Run the full pytest suite:

```bash
python -m pytest test/
```

All 19 test cases validate:
- Silent letter removal & phonetic cleansing
- Irregular verb elimination (`went` $\rightarrow$ `goed`, `bought` $\rightarrow$ `bayed`, etc.)
- Pronoun and regular plural inflection
- John Wilkins kinetic vector decomposition
- SAPI/WAV speech synthesis audio generation

---

## 7. License & Credits

Released under the [MIT License](LICENSE).  
Inspired by the works of John Wilkins (1668), constructed auxiliary languages, and computational language projects (Nizaba, VolumEN).

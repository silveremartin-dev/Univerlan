# Agent Protocol & Guidelines for Univerlan

Welcome to the **Univerlan** development and research environment. This document outlines the design tenets, architectural rules, code hygiene, and linguistic constraints expected of human developers and autonomous AI agents working on this codebase.

## 1. Project Philosophy & Vision
*Univerlan* is an interstellar auxiliary conlang (constructed language) designed for 22nd-to-23rd century interstellar commerce and pragmatic cross-planetary communication.
It is an **"English++" / rationalized lingua franca** inspired by John Wilkins (*An Essay towards a Real Character and a Philosophical Language*), Basic English, and phonetic scripts (IPA).

### Core Linguistic Directives:
1. **Bijective Phonology (1 sign = 1 sound):**
   - Strictly no silent letters (`knight` -> `nait`, `though` -> `do`).
   - No gratuitous geminates/double consonants (`apple` -> `apl`).
   - No ambiguous multi-sound graphs without unique 1:1 mapping.
2. **Deterministic Regularity:**
   - **Zero irregular verbs** in the entire lexicon. All past tense forms, plurals, and participles follow uniform generative morphological rules.
   - Fixed syntactic order: **SVO (Subject - Verb - Object)**.
3. **Wilkinsian Semantic Composition:**
   - Replace opaque, redundant lexical clutter with transparent directional and categorical affixes.
   - Example: *lift* = `mov-up`, *pull* = `mov-tu-mi`, *push* = `mov-fro-mi`, *fall* = `mov-don`.
4. **Pragmatic Economy:**
   - Words are designed for low acoustic confusion across noisy transmission channels (radio, subspace coms, noisy starports).

---

## 2. Repository Layout

```
├── .gitignore
├── LICENSE                   # MIT License
├── README.md                 # Project Overview & Quickstart
├── agent.md                  # This file (Agent Instructions & Architectural Spec)
├── doc/                      # Formal Linguistic Specifications (English)
│   ├── phonology_orthography.md
│   ├── grammar_syntax.md
│   ├── lexicon_derivation.md
│   └── wilkins_ontology.md
├── source/                   # Core Python Engine
│   ├── __init__.py
│   ├── phonetics.py          # Bijective Grapheme-Phoneme converter & normalizer
│   ├── morphology.py         # Regular inflections, pronouns, affixes
│   ├── wilkins.py            # Conceptual decomposition engine
│   ├── translator.py         # English <-> Univerlan translation pipeline
│   ├── tts.py                # Speech synthesis integration
│   └── cli.py                # Command-line interface
├── scripts/                  # Utilities, REPL, Interactive Web App, Dictionary exporters
│   ├── interactive_cli.py
│   ├── export_dictionary.py
│   └── web_app.py
├── test/                     # Pytest suite with 100% core coverage
│   ├── test_phonetics.py
│   ├── test_morphology.py
│   ├── test_wilkins.py
│   ├── test_translator.py
│   └── test_tts.py
└── scratch/                  # Ephemeral experiments & staging area
```

---

## 3. Engineering & Linguistic Rigor (Nizaba / VolumEN standard)

- **Determinism:** Translating an English sentence twice must produce identical, canonical Univerlan text.
- **Bi-directional Transparency:** Where possible, provide morphological breakdowns (glosses) for learners and automated checkers.
- **Test-Driven Refinements:** Whenever a new lexical rule, Wilkins vector, or phonetic edge case is introduced, a corresponding test must be added to `/test`.
- **Zero Third-party Requirement for Core:** The core phonetic, morphological, and translation algorithms in `/source` must execute with Python standard library modules (`re`, `unicodedata`, `dataclasses`, `typing`, `json`) to guarantee zero-dependency portability across any platform.
- **Audio & TTS Compatibility:** The phonology must directly output valid IPA and phonetic tokens compatible with standard Speech Synthesis engines (SAPI, eSpeak, Web Speech API).

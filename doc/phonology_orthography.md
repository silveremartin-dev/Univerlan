# Univerlan Phonology & Orthography Specification

Version: 1.0  
Status: Canonical  
Standard: 1 Grapheme = 1 Phoneme (Bijective Latin Orthography)

---

## 1. Design Principles

Univerlan eliminates the orthographic chaos of historical English (silent letters, multi-letter digraphs with five different pronunciations, capricious vowel shifts) while remaining 100% typeable on standard keyboards and immediately legible to human and machine transceivers.

- **Strict Bijection:** Every written letter corresponds to exactly one sound.
- **Zero Silent Letters:** `knight` $\rightarrow$ `nait`, `receipt` $\rightarrow$ `resit`, `doubt` $\rightarrow$ `daut`.
- **Zero Geminates:** Consonants are never doubled arbitrarily (`better` $\rightarrow$ `beter`, `apple` $\rightarrow$ `apel`).
- **No Ambiguous Polyphones:** The letter `c` is always [tʃ] (as in *cheers*), never [k] or [s]. The letter `x` is always [ʃ] (as in *ship*). The letter `j` is always [dʒ] (as in *joy*). The letter `k` represents [k], and `s` represents [s].

---

## 2. Phonemic Inventory

### 2.1 Vowels

Univerlan uses a balanced, universally pronounceable 5-vowel system plus 4 transparent diphthongs:

| Grapheme | IPA | Univerlan Example | English Source / Equivalent |
|---|---|---|---|
| **a** | [a] | `kat` | cat, father |
| **e** | [e] / [ɛ] | `bed` | bed, send |
| **i** | [i] | `sip` | see, ship, machine |
| **o** | [o] / [ɔ] | `dok` | dock, law, note |
| **u** | [u] | `lun` | moon, blue, put |

#### Transparent Diphthongs
| Grapheme | IPA | Example | Meaning / Origin |
|---|---|---|---|
| **ai** | [aɪ] | `nait` | night, light, my |
| **au** | [aʊ] | `daut` | doubt, out, down (`don` / `daut`) |
| **ei** | [eɪ] | `dei` | day, trade |
| **oi** | [ɔɪ] | `joi` | joy, voice |

---

### 2.2 Consonants

| Grapheme | IPA | Phonetic Role | Example |
|---|---|---|---|
| **p** | [p] | Voiceless bilabial plosive | `pan` |
| **b** | [b] | Voiced bilabial plosive | `big` |
| **t** | [t] | Voiceless alveolar plosive | `tel` (tell) |
| **d** | [d] | Voiced alveolar plosive | `dei` (day) |
| **k** | [k] | Voiceless velar plosive (replaces English *c* and *q*) | `kargo` (cargo) |
| **g** | [g] | Voiced velar plosive (always hard) | `go` (go), `giv` (give) |
| **f** | [f] | Voiceless labiodental fricative (replaces *ph*) | `foto` (photo) |
| **v** | [v] | Voiced labiodental fricative | `vek` (vector) |
| **s** | [s] | Voiceless alveolar fricative (always sharp [s]) | `sun` (sun), `sent` (cent) |
| **z** | [z] | Voiced alveolar fricative | `zon` (zone) |
| **c** | [tʃ] | Voiceless postalveolar affricate (*ch*) | `cek` (check), `cild` (child) |
| **j** | [dʒ] | Voiced postalveolar affricate (*j*, soft *g*) | `joi` (joy), `jop` (job) |
| **x** | [ʃ] | Voiceless postalveolar fricative (*sh*) | `xip` (ship), `stat-xip` (starship) |
| **m** | [m] | Bilabial nasal | `man` (human, person) |
| **n** | [n] | Alveolar nasal | `nu` (new) |
| **l** | [l] | Alveolar lateral approximant | `laif` (life) |
| **r** | [r] / [ɹ] | Alveolar tap or approximant | `red` (red) |
| **w** | [w] | Labial-velar approximant | `we` (way) |
| **y** | [j] | Palatal approximant (semivowel) | `yes` (yes) |
| **h** | [h] | Voiceless glottal fricative | `hot` (hot) |

*Note on dental fricatives:* The historic English `th` sound is simplified to `t` for voiceless (*think* $\rightarrow$ `tink`) and `d` for voiced (*the* $\rightarrow$ `de`, *this* $\rightarrow$ `dis`, *that* $\rightarrow$ `dat`).

---

## 3. Punctuation & Numeric Symbols

- Standard punctuation is retained for international computer readability: `.`, `,`, `?`, `!`, `:`, `;`, `-`.
- Hyphen `-` indicates semantic compound boundaries (e.g. `mov-up`, `mov-tu-mi`).
- Numbers use standard decimal Hindu-Arabic numerals: `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`.
- Numeric convenience names:
  - 0: `ziro`
  - 1: `un`
  - 2: `tu`
  - 3: `tri`
  - 4: `for`
  - 5: `faiv`
  - 6: `siks`
  - 7: `seven`
  - 8: `eit`
  - 9: `nain`
  - 10: `ten`
  - 100: `hondred`
  - 1000: `tauzend`

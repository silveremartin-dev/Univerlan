# Univerlan Grammar & Syntax Specification

Version: 1.0  
Status: Canonical

---

## 1. Sentence Architecture: Strict SVO

Univerlan maintains a strict **Subject - Verb - Object** order in all affirmative, negative, and interrogative declarative sentences.

```
[Subject] + [Verbal Modifiers] + [Verb] + [Object] + [Adverbial / Prepositional Phrases]
```

### Examples:
- *English:* "The trader sells crystals to the colony."
- *Univerlan:* `De treder sel kristals tu de koloni.`
- *Word-by-word:* The [de] trader [treder] sells [sel] crystals [kristals] to [tu] the [de] colony [koloni].

Questions are marked either by the interrogative particle `ku` at the sentence head, or simply with a rising intonation and standard punctuation `?`:
- `Ku yu hav de kargo?` ("Do you have the cargo?")
- `Yu hav de kargo?` ("You have the cargo?")

---

## 2. Pronominal System

Personal pronouns are completely invariant for case (subject vs. object). The role is determined solely by position in the SVO sequence.

| Person | Singular | Plural | Possessive Suffix (`-n`) |
|---|---|---|---|
| **1st person** | `mi` (I / me) | `wi` (we / us) | `min` (my/mine), `win` (our/ours) |
| **2nd person** | `yu` (you) | `yus` (you all / y'all) | `yun` (your/yours), `yusn` (your-pl) |
| **3rd person (animate/masc)** | `hi` (he / him) | `dey` (they / them) | `hin` (his), `deyn` (their/theirs) |
| **3rd person (animate/fem)** | `xe` (she / her) | `dey` (they / them) | `xen` (her/hers), `deyn` (their/theirs) |
| **3rd person (inanimate/neutral)**| `it` (it) | `deys` / `dey` (they) | `itn` (its), `deyn` (theirs) |
| **Reflexive marker** | `-self` (`miself`, `yuself`, `hiself`, `xeself`, `itself`, `wiself`, `deyselfs`) |

---

## 3. Verbal System: Complete Regularity

There are **zero irregular verbs** in Univerlan. The historical chaos of *be/was/been*, *go/went/gone*, *buy/bought/bought* is completely abolished.

### 3.1 Base Form
The base root acts as the infinitive and the general/present tense:
- `mi go` = "I go"
- `hi go` = "He goes" (no superfluous `-s` agreement ending!)
- `dey go` = "They go"

### 3.2 Tenses and Aspect Markers

| Tense / Aspect | Formation Rule | Example with `go` | Example with `bay` (buy) |
|---|---|---|---|
| **Present / Habitual** | `[Root]` | `mi go` (I go) | `hi bay` (He buys) |
| **Past (Definite)** | `[Root] + -ed` | `mi goed` (I went) | `hi bayed` (He bought) |
| **Future** | `wil + [Root]` | `mi wil go` (I will go) | `hi wil bay` (He will buy) |
| **Conditional / Intent**| `wud + [Root]` | `mi wud go` (I would go) | `hi wud bay` (He would buy) |
| **Continuous / Aspect**| `is + [Root]-ing` or `[Root]-ing` | `mi is going` | `hi is baying` |
| **Completed / Perfect** | `hav + [Root]-ed` | `mi hav goed` (I have gone) | `hi hav bayed` (He has bought) |
| **Obligation / Modal** | `mas + [Root]` (must) / `kan + [Root]` (can) | `mi mas go` | `yu kan bay` |

### 3.3 The Copula (`be` / `is`)
In Univerlan, `is` is the universal present copula:
- `mi is redi` = "I am ready"
- `yu is redi` = "You are ready"
- `dey is redi` = "They are ready"
- Past: `ised` (or `beed`): `mi ised redi` ("I was ready")
- Future: `wil be`: `mi wil be redi` ("I will be ready")

### 3.4 Negation
Place `no` directly before the verb:
- `mi no no` = "I do not know" (`no` = not, `no` [v.] = know)
- `hi no goed tu de stasion` = "He did not go to the station"
- `wi no wil weit` = "We will not wait"

---

## 4. Nominal Morphology: Plurality & Articles

### 4.1 Plural Suffix: `-s` (or `-es`)
All nouns form their plural by appending `-s` (or `-es` after sibilants `s`, `z`, `x`, `c`):
- `cild` (child) $\rightarrow$ `cilds` (children)
- `man` (person/man) $\rightarrow$ `mans` (people/men)
- `tut` (tooth) $\rightarrow$ `tuts` (teeth)
- `boks` (box) $\rightarrow$ `bokses` (boxes)

### 4.2 Definite and Indefinite Articles
- **Definite:** `de` (invariant: "the")
- **Indefinite:** `un` (invariant: "a" / "an")

---

## 5. Modifiers: Adjectives & Adverbs

### 5.1 Position
Adjectives precede the noun:
- `big xip` = "big ship"
- `kwik transakxun` = "quick transaction"

### 5.2 Adverbial Derivation: `-li`
Append `-li` to any adjective to produce the corresponding manner adverb:
- `kwik` (quick) $\rightarrow$ `kwikli` (quickly)
- `klir` (clear) $\rightarrow$ `klirli` (clearly)
- `saf` (safe) $\rightarrow$ `safli` (safely)

### 5.3 Comparison
Comparison is 100% regular using `mor` and `most`:
- Positive: `gud` (good)
- Comparative: `mor gud` (better - no irregular *better*!)
- Superlative: `most gud` (best)
- Equal comparison: `as gud as` (as good as)

---

## 6. Logical Connectors

- `and` : and
- `or` : or
- `but` : but
- `so` : so / therefore
- `bikoz` : because
- `if` : if
- `den` : then

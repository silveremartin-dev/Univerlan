# Reddit launch post — Univerlan

## Suggested subreddits

- **r/conlangs**: the main audience. Use the flair for auxlangs / feedback, lead with the design goals and the known inconsistencies, and ask for critique. Check the sub's rules on self-promotion and links.
- **r/auxlangs**: Univerlan is explicitly an auxiliary language ("rationalized English"), so this sub can judge it against Basic English, Globish, Novial, etc.
- **r/linguistics**: only if framed as a question (e.g. Wilkins-style a priori compounding in an a posteriori language). Keep it short and non-promotional.
- **r/Python** (Showcase flair): the zero-dependency engine (translator, IPA, TTS fallback) for developers.

---

**Title:** Univerlan: an experimental "rationalized English" auxlang (one letter = one sound, no irregular verbs, Wilkins-style compounds) with a small Python translator. Feedback wanted, especially on the inconsistencies

---

Hi all,

I've open-sourced **Univerlan**, a hobby project that asks: *what if English kept its vocabulary and SVO grammar, but dropped its historical baggage?* It's an a posteriori auxlang built on English, with a small zero-dependency Python engine that translates English into it. It's a prototype, and I'd value critique more than praise.

### Design goals

1. **Bijective spelling**: one grapheme ↔ one phoneme. `knight → nait`, `ship → xip`, `check → cek` (`c` = [tʃ], `x` = [ʃ], `j` = [dʒ]).
2. **No irregular morphology**: `went → goed`, `bought → bayed`, `took → teked`; no 3rd-person `-s` (`hi go`); negation is pre-verbal `no` (`mi no go`).
3. **Wilkins-inspired transparent compounds** (after John Wilkins' *Essay towards a Real Character*, 1668), mainly for motion and relations: `lift → mov-up`, `drop → mov-don`, `pull → mov-tu-mi`, `push → mov-fro-mi`, `enter → mov-in`, `exit → mov-ut`.
4. **Pragmatism over purity**: keep recognizable English roots so an English speaker can almost read it cold.

Example from the CLI:

> EN: *Please lift the container and push it into the cargo hold.*
> UV: *Pliis mov-up de kontener and mov-fro-mi it in de kargo hold.*

### What's in the repo

- Python engine with no external dependencies (standard library only): phonetic normalizer, verb regularizer and pronoun system, Wilkins decomposition, English → Univerlan translator, IPA output.
- TTS through Windows SAPI, the Web Speech API in the browser, or a dependency-free formant fallback.
- CLI, interactive REPL and a small local web UI.
- Specs (phonology, grammar, ontology, derivation), a tutorial, a phrasebook, a generated dictionary (~225 entries, JSON + Markdown) and a short *Little Prince* excerpt.
- 22 pytest tests plus a corpus/lexicon audit script. MIT licence.

### Known limits (I'd rather say them first)

- **Translation is word by word**: lexicon lookup, then morphological rules, then phonetic respelling as a fallback. There's no real parsing, so idioms, phrasal verbs and complex syntax aren't handled.
- **Pronouns & homophones**: `they` has been resolved to `dey` (possessive `deyn`) to avoid collision with `de` ("the") and `den` ("then"), and `wait` is spelled `weit` to match the `/weɪt/` diphthong rule (`ei` = [eɪ]).
- The lexicon is small (~225 core entries), and the motion vectors are the primary part of the Wilkins ontology currently fleshed out.
- No learnability testing with actual speakers; all claims about "easier" are design intentions, not empirical results.
- The README's "interstellar" framing is flavour. The real question is plain auxlang engineering.

### Feedback I'm looking for

- Is "bijective respelling + regularized grammar on an English base" worth pursuing, or does it land in the uncanny valley where English speakers find it harder, not easier?
- Are Wilkins-style compounds like `mov-fro-mi` a good idea for core vocabulary, or should they stay optional and leave `push` as a root?
- Which existing auxlangs or reform proposals (Basic English, Globish, SoundSpel, Novial…) should I compare against more seriously?

Repo: https://github.com/silveremartin-dev/Univerlan

Thanks for reading. All criticism welcome.

— Silvère Martin-Michiellot

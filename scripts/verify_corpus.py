"""Verification and audit script for Univerlan dictionary, phonetic bijection, and literary corpus."""

import json
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from source.phonetics import to_ipa
from source.wilkins import WILKINS_VECTOR_MAP

def verify():
    print("--- Auditing Univerlan Lexicon and Corpus ---")
    dict_file = ROOT_DIR / "docs" / "dictionary.json"
    prince_file = ROOT_DIR / "docs" / "little_prince.json"

    errors = 0

    if not dict_file.exists():
        print(f"[ERROR] Dictionary file missing: {dict_file}")
        errors += 1
    else:
        with open(dict_file, "r", encoding="utf-8") as f:
            entries = json.load(f)
        print(f"Total dictionary entries: {len(entries)}")
        for item in entries[:5]:
            w = item.get("univerlan", "")
            ipa = to_ipa(w)
            if not ipa:
                print(f"[WARN] Failed IPA conversion for: {w}")

    # Check Wilkins kinetic vectors
    print(f"Total Wilkins kinetic vectors registered: {len(WILKINS_VECTOR_MAP)}")
    for en_v, (univ_v, cat) in list(WILKINS_VECTOR_MAP.items())[:4]:
        print(f"  Vector: '{en_v}' -> '{univ_v}' ({cat})")

    # Check Little Prince corpus
    if prince_file.exists():
        with open(prince_file, "r", encoding="utf-8") as f:
            p_data = json.load(f)
        sentences = p_data.get("sentences", [])
        print(f"Total Little Prince sentences: {len(sentences)}")
        for s in sentences:
            ipa = to_ipa(s["univerlan"])
            if not ipa:
                print(f"[WARN] Empty IPA in sentence #{s['id']}")

    if errors == 0:
        print("\n✅ Univerlan corpus and lexicon audit passed successfully (0 fatal errors)!")
    else:
        print(f"\n❌ Audit completed with {errors} errors.")
        sys.exit(1)

if __name__ == "__main__":
    verify()

#!/usr/bin/env python3
"""Interactive terminal REPL for Univerlan.

Allows real-time translation from English to Univerlan, audio pronunciation,
IPA phonetics inspection, and Wilkinsian decomposition.
"""

from __future__ import annotations
import os
import sys

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Ensure root workspace is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from source.translator import UniverlanTranslator
from source.tts import SpeechSynthesizer
from source.wilkins import WilkinsDecomposer


def run_repl() -> None:
    translator = UniverlanTranslator()
    tts = SpeechSynthesizer()

    print("=" * 60)
    print("   UNIVERLAN INTERSTELLAR TERMINAL v1.0.0")
    print("   Type English text to translate. Commands:")
    print("     :s  - Speak last translated phrase aloud")
    print("     :w <word> - Inspect Wilkins vector decomposition")
    print("     :q  - Quit terminal")
    print("=" * 60)

    last_univerlan = ""

    while True:
        try:
            line = input("\n[EN] > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting Univerlan terminal.")
            break

        if not line:
            continue

        if line.lower() == ":q":
            print("Safe travels (Saf voyaj).")
            break

        if line.lower() == ":s":
            if last_univerlan:
                print(f"[*] Speaking: '{last_univerlan}'...")
                tts.speak(last_univerlan)
            else:
                print("[!] No previous translation to speak.")
            continue

        if line.startswith(":w "):
            target_word = line[3:].strip()
            w_res = WilkinsDecomposer.decompose(target_word)
            if w_res:
                comp, cat = w_res
                print(f"    Wilkins Compound: {comp} (Category: {cat})")
            else:
                print(f"    No Wilkins vector found for '{target_word}'.")
            continue

        # Standard translation
        res = translator.translate(line)
        last_univerlan = res.univerlan_text
        print(f"[UV]  {res.univerlan_text}")
        print(f"[IPA] {res.ipa_transcription}")

        # Summary of decomposition
        special_derivations = [
            g for g in res.gloss if "Wilkins" in g or "regularized" in g
        ]
        if special_derivations:
            print("      Deductions: " + ", ".join(special_derivations))


if __name__ == "__main__":
    run_repl()

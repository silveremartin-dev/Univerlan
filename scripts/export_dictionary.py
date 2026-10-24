#!/usr/bin/env python3
"""Exports the comprehensive Univerlan trilingual dictionary to Markdown and JSON formats."""

from __future__ import annotations
import json
import os
import sys

# Ensure root workspace is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from source.translator import LEXICON_EN_TO_UNIVERLAN
from source.wilkins import WILKINS_VECTOR_MAP
from source.morphology import (
    PRONOUN_MAP,
    IRREGULAR_PLURAL_MAP,
    IRREGULAR_COMPARISON_MAP,
)
from source.lexicon_data import CORE_LEXICON_FR
from source.phonetics import to_ipa


def export_dictionary() -> None:
    doc_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    os.makedirs(doc_dir, exist_ok=True)

    # Build reverse French map: univerlan -> list of french terms
    uv_to_fr = {}
    for fr_word, uv_word in CORE_LEXICON_FR.items():
        if uv_word not in uv_to_fr:
            uv_to_fr[uv_word] = []
        if fr_word not in uv_to_fr[uv_word]:
            uv_to_fr[uv_word].append(fr_word)

    entries = []

    # 1. Core Lexicon
    for en, uv in LEXICON_EN_TO_UNIVERLAN.items():
        fr_list = uv_to_fr.get(uv, [])
        fr_str = ", ".join(fr_list[:3]) if fr_list else "-"
        entries.append(
            {
                "english": en,
                "french": fr_str,
                "univerlan": uv,
                "ipa": to_ipa(uv),
                "type": "lexicon",
                "notes": "Core vocabulary",
            }
        )

    # 2. Wilkinsian vectors
    for en, (uv, cat) in WILKINS_VECTOR_MAP.items():
        if not any(e["english"] == en and e["univerlan"] == uv for e in entries):
            fr_list = uv_to_fr.get(uv, [])
            fr_str = ", ".join(fr_list[:3]) if fr_list else "-"
            entries.append(
                {
                    "english": en,
                    "french": fr_str,
                    "univerlan": uv,
                    "ipa": to_ipa(uv),
                    "type": "wilkins_vector",
                    "notes": f"Wilkins ontology: {cat}",
                }
            )

    # 3. Pronouns
    for en, uv in PRONOUN_MAP.items():
        if not any(e["english"] == en and e["univerlan"] == uv for e in entries):
            fr_list = uv_to_fr.get(uv, [])
            fr_str = ", ".join(fr_list[:3]) if fr_list else "-"
            entries.append(
                {
                    "english": en,
                    "french": fr_str,
                    "univerlan": uv,
                    "ipa": to_ipa(uv),
                    "type": "pronoun",
                    "notes": "Pronominal system",
                }
            )

    # Sort alphabetically by english
    entries.sort(key=lambda x: x["english"].lower())

    # Export JSON
    json_path = os.path.join(doc_dir, "dictionary.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    print(f"Exported {len(entries)} entries to {json_path}")

    # Export Markdown
    md_path = os.path.join(doc_dir, "DICTIONARY.MD")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Univerlan Complete Trilingual Dictionary\n\n")
        f.write(
            f"Total canonical entries: **{len(entries)}** | Trilingual: English &bull; Français &bull; Univerlan\n\n"
        )
        f.write("| English | Français | Univerlan | IPA | Category | Notes |\n")
        f.write("|---|---|---|---|---|---|\n")
        for e in entries:
            f.write(
                f"| **{e['english']}** | *{e['french']}* | `{e['univerlan']}` | {e['ipa']} | {e['type']} | {e['notes']} |\n"
            )
    print(f"Exported Markdown dictionary to {md_path}")


if __name__ == "__main__":
    export_dictionary()

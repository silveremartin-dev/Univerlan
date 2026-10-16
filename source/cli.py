"""Command Line Interface (CLI) for Univerlan.

Usage:
  python -m source.cli translate "Sentence to translate" [--speak] [--ipa]
  python -m source.cli ipa "Univerlan text"
  python -m source.cli wilkins "English verb"
  python -m source.cli speak "Univerlan text" [--save file.wav]
"""

from __future__ import annotations
import argparse
import sys

from source.translator import UniverlanTranslator
from source.phonetics import to_ipa
from source.wilkins import WilkinsDecomposer
from source.tts import SpeechSynthesizer


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="univerlan",
        description="Univerlan: The Interstellar Rationalized Conlang Engine",
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # translate command
    trans_p = subparsers.add_parser(
        "translate", help="Translate English to Univerlan"
    )
    trans_p.add_argument("text", help="English text to translate")
    trans_p.add_argument(
        "--speak", action="store_true", help="Speak the translated text aloud"
    )
    trans_p.add_argument(
        "--ipa", action="store_true", help="Display IPA transcription"
    )
    trans_p.add_argument(
        "--gloss",
        action="store_true",
        help="Display morpheme-by-morpheme gloss",
    )

    # ipa command
    ipa_p = subparsers.add_parser(
        "ipa", help="Generate IPA transcription for Univerlan text"
    )
    ipa_p.add_argument("text", help="Univerlan text")

    # wilkins command
    wilk_p = subparsers.add_parser(
        "wilkins", help="Decompose an English verb using Wilkins vectors"
    )
    wilk_p.add_argument("word", help="English verb or action word")

    # speak command
    speak_p = subparsers.add_parser("speak", help="Synthesize Univerlan speech")
    speak_p.add_argument("text", help="Univerlan text to pronounce")
    speak_p.add_argument(
        "--save", metavar="FILE", help="Save speech as .wav file"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "translate":
        translator = UniverlanTranslator()
        res = translator.translate(args.text)
        print(f"\n[EN]  {res.english_source}")
        print(f"[UV]  {res.univerlan_text}")
        if args.ipa:
            print(f"[IPA] {res.ipa_transcription}")
        if args.gloss:
            print("\n--- Gloss & Decomposition ---")
            for item in res.gloss:
                print(f"  * {item}")
        if args.speak:
            tts = SpeechSynthesizer()
            tts.speak(res.univerlan_text)

    elif args.command == "ipa":
        print(to_ipa(args.text))

    elif args.command == "wilkins":
        res = WilkinsDecomposer.decompose(args.word)
        if res:
            compound, cat = res
            print(f"Word: {args.word}")
            print(f"Univerlan Compound: {compound}")
            print(f"Wilkins Category:   {cat}")
        else:
            print(f"No Wilkinsian decomposition found for '{args.word}'.")

    elif args.command == "speak":
        tts = SpeechSynthesizer()
        if args.save:
            ok = tts.save_wav(args.text, args.save)
            if ok:
                print(f"Audio saved successfully to {args.save}")
            else:
                print(f"Failed to save audio to {args.save}", file=sys.stderr)
        else:
            tts.speak(args.text)


if __name__ == "__main__":
    main()

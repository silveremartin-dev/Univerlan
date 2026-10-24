#!/usr/bin/env python3
"""Launcher and local web server for Univerlan Studio.

Serves the interactive web interface, handles translation and TTS API endpoints,
and automatically opens the default web browser.
"""

from __future__ import annotations
import http.server
import json
import os
import socket
import socketserver
import sys
import webbrowser
from pathlib import Path

# Ensure workspace root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from source.translator import UniverlanTranslator
from source.wilkins import WilkinsDecomposer
from source.phonetics import to_ipa
from source.tts import SpeechSynthesizer

DEFAULT_PORT = 8080


def find_available_port(start_port: int = DEFAULT_PORT, max_attempts: int = 20) -> int:
    """Finds an open TCP port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start_port


class UniverlanStudioHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler serving root files and API endpoints."""

    translator = UniverlanTranslator()
    tts = SpeechSynthesizer()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT_DIR), **kwargs)

    def do_GET(self) -> None:
        if self.path in ("/", ""):
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self) -> None:
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        try:
            data = json.loads(body)
        except Exception:
            data = {}

        if self.path == "/api/translate":
            text = data.get("text", "")
            direction = data.get("direction", "to_univerlan")
            target_lang = data.get("target_lang", "fr")
            res = self.translator.translate(text, direction=direction, target_lang=target_lang)
            resp = {
                "english": res.english_source,
                "univerlan": res.univerlan_text,
                "ipa": res.ipa_transcription,
                "gloss": res.gloss,
            }
            self.send_json_response(resp)
        elif self.path == "/api/speak":
            text = data.get("text", "")
            lang = data.get("lang", "uv")
            self.tts.speak(text, lang=lang)
            self.send_json_response({"status": "ok"})
        else:
            self.send_response(404)
            self.end_headers()

    def send_json_response(self, data: dict) -> None:
        payload = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args) -> None:
        # Suppress routine request spam in console
        pass


def main() -> None:
    port = find_available_port(DEFAULT_PORT)
    url = f"http://localhost:{port}/index.html"

    print("========================================================")
    print("  🚀 Univerlan Studio — Navigateur & Studio Interstellaire")
    print(f"  URL : {url}")
    print("  Appuyez sur Ctrl+C pour arrêter le serveur.")
    print("========================================================\n")

    try:
        webbrowser.open(url)
    except Exception:
        pass

    with socketserver.TCPServer(("127.0.0.1", port), UniverlanStudioHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nArrêt du serveur Univerlan Studio.")


if __name__ == "__main__":
    main()

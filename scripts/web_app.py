#!/usr/bin/env python3
"""Interactive Web Translator & Audio Synthesizer for Univerlan.

Serves an interstellar-styled user interface for real-time translation,
phonetic breakdown, Wilkinsian vector inspection, and multi-mode TTS.
Zero external dependencies required (uses standard library http.server).
"""

from __future__ import annotations
import http.server
import json
import os
import sys
import urllib.parse

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from source.translator import UniverlanTranslator
from source.wilkins import WilkinsDecomposer
from source.phonetics import to_ipa
from source.tts import SpeechSynthesizer

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>UNIVERLAN - Interstellar Conlang Terminal</title>
  <style>
    :root {
      --bg: #0b0f19;
      --card-bg: #111827;
      --border: #1f2937;
      --text: #f3f4f6;
      --muted: #9ca3af;
      --primary: #38bdf8;
      --primary-hover: #0284c7;
      --accent: #10b981;
      --warning: #f59e0b;
      --font-mono: 'Consolas', 'Courier New', monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    header {
      background: rgba(17, 24, 39, 0.85);
      border-bottom: 1px solid var(--border);
      padding: 1.25rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      backdrop-filter: blur(8px);
    }
    .logo {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      color: var(--primary);
      font-size: 1.2rem;
    }
    .badge {
      background: rgba(56, 189, 248, 0.15);
      color: var(--primary);
      padding: 0.2rem 0.6rem;
      border-radius: 9999px;
      font-size: 0.75rem;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }
    main {
      flex: 1;
      max-width: 1100px;
      width: 100%;
      margin: 2rem auto;
      padding: 0 1.5rem;
      display: grid;
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .card h2 {
      font-size: 1.1rem;
      color: var(--primary);
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .translator-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
    }
    @media (max-width: 768px) {
      .translator-grid { grid-template-columns: 1fr; }
    }
    textarea {
      width: 100%;
      height: 160px;
      background: #070a12;
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      font-family: inherit;
      font-size: 1rem;
      padding: 1rem;
      resize: vertical;
      transition: border-color 0.2s;
    }
    textarea:focus {
      outline: none;
      border-color: var(--primary);
    }
    .output-box {
      width: 100%;
      height: 160px;
      background: #070a12;
      border: 1px solid var(--border);
      border-radius: 8px;
      color: #38bdf8;
      font-size: 1.05rem;
      padding: 1rem;
      overflow-y: auto;
      font-weight: 500;
    }
    .ipa-badge {
      font-family: var(--font-mono);
      color: #a78bfa;
      font-size: 0.9rem;
      margin-top: 0.5rem;
      background: rgba(167, 139, 250, 0.1);
      padding: 0.4rem 0.8rem;
      border-radius: 6px;
      display: inline-block;
    }
    .actions {
      display: flex;
      gap: 0.75rem;
      margin-top: 1rem;
      flex-wrap: wrap;
    }
    button {
      background: var(--primary);
      color: #0b0f19;
      border: none;
      padding: 0.6rem 1.2rem;
      border-radius: 6px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      transition: background 0.15s, transform 0.1s;
    }
    button:hover {
      background: var(--primary-hover);
    }
    button:active {
      transform: scale(0.98);
    }
    button.secondary {
      background: #1f2937;
      color: var(--text);
      border: 1px solid #374151;
    }
    button.secondary:hover {
      background: #374151;
    }
    .presets {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
      margin-top: 1rem;
    }
    .preset-pill {
      background: #1e293b;
      color: #94a3b8;
      padding: 0.35rem 0.75rem;
      border-radius: 9999px;
      font-size: 0.8rem;
      cursor: pointer;
      border: 1px solid #334155;
      transition: all 0.2s;
    }
    .preset-pill:hover {
      color: var(--text);
      border-color: var(--primary);
    }
    .gloss-list {
      margin-top: 1rem;
      font-size: 0.85rem;
      color: var(--muted);
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
    }
    .gloss-item {
      background: #0f172a;
      border: 1px solid #1e293b;
      padding: 0.25rem 0.5rem;
      border-radius: 4px;
      font-family: var(--font-mono);
    }
    footer {
      text-align: center;
      padding: 1.5rem;
      border-top: 1px solid var(--border);
      color: var(--muted);
      font-size: 0.85rem;
    }
  </style>
</head>
<body>
  <header>
    <div class="logo">
      <span>UNIVERLAN</span>
      <span class="badge">INTERSTELLAR CONLANG 2230+</span>
    </div>
    <div style="font-size: 0.85rem; color: var(--muted);">
      Bijective Phonology &bull; John Wilkins Matrix &bull; SVO
    </div>
  </header>

  <main>
    <section class="card">
      <h2>&#9881; English &rarr; Univerlan Rationalized Translator</h2>
      
      <div class="translator-grid">
        <div>
          <label style="display:block; font-size:0.85rem; color:var(--muted); margin-bottom:0.5rem;">
            English Source:
          </label>
          <textarea id="englishInput" placeholder="Type or paste English sentence here... (e.g. Please lift the cargo and push it into the starship.)"></textarea>
          <div class="presets">
            <span class="preset-pill" onclick="setPreset('Please lift the cargo and push it into the ship.')">Lift & Push cargo</span>
            <span class="preset-pill" onclick="setPreset('He bought five ships yesterday and went to the station.')">Irregular verbs</span>
            <span class="preset-pill" onclick="setPreset('Children and people have many goods.')">Irregular plurals</span>
            <span class="preset-pill" onclick="setPreset('We do not wait for the dangerous enemy.')">Negation & Modifiers</span>
          </div>
        </div>

        <div>
          <label style="display:block; font-size:0.85rem; color:var(--muted); margin-bottom:0.5rem;">
            Univerlan Canonical Output:
          </label>
          <div id="univerlanOutput" class="output-box">Translation will appear here in real time...</div>
          <div id="ipaDisplay" class="ipa-badge" style="display:none;"></div>
        </div>
      </div>

      <div class="actions">
        <button onclick="handleTranslate()">Translate &amp; Analyze</button>
        <button class="secondary" onclick="speakBrowser()">&#128266; Speak (Web Audio)</button>
        <button class="secondary" onclick="speakBackend()">&#128266; Speak (Windows SAPI)</button>
      </div>

      <div id="glossContainer" class="gloss-list"></div>
    </section>

    <section class="card">
      <h2>&#128506; John Wilkins Conceptual Matrix (Founding Principle)</h2>
      <p style="color:var(--muted); font-size:0.9rem; line-height:1.5; margin-bottom:1rem;">
        Univerlan replaces arbitrary English vocabulary with transparent, directional and relational vectors.
      </p>
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:1rem;">
        <div style="background:#070a12; padding:0.75rem; border-radius:6px; border:1px solid #1f2937;">
          <strong style="color:#38bdf8;">lift / raise</strong> &rarr; <code>mov-up</code><br>
          <small style="color:var(--muted);">Vertical kinetic vector (+)</small>
        </div>
        <div style="background:#070a12; padding:0.75rem; border-radius:6px; border:1px solid #1f2937;">
          <strong style="color:#38bdf8;">drop / fall</strong> &rarr; <code>mov-don</code><br>
          <small style="color:var(--muted);">Vertical kinetic vector (-)</small>
        </div>
        <div style="background:#070a12; padding:0.75rem; border-radius:6px; border:1px solid #1f2937;">
          <strong style="color:#38bdf8;">pull</strong> &rarr; <code>mov-tu-mi</code><br>
          <small style="color:var(--muted);">Egocentric vector (to me)</small>
        </div>
        <div style="background:#070a12; padding:0.75rem; border-radius:6px; border:1px solid #1f2937;">
          <strong style="color:#38bdf8;">push</strong> &rarr; <code>mov-fro-mi</code><br>
          <small style="color:var(--muted);">Egocentric vector (from me)</small>
        </div>
      </div>
    </section>
  </main>

  <footer>
    Univerlan Open Source Project &bull; MIT License &bull; Inspired by John Wilkins, IPA &amp; Rational Lingua Francas
  </footer>

  <script>
    let currentUniverlan = "";

    function setPreset(text) {
      document.getElementById('englishInput').value = text;
      handleTranslate();
    }

    async function handleTranslate() {
      const text = document.getElementById('englishInput').value.trim();
      if (!text) {
        document.getElementById('univerlanOutput').innerText = "";
        document.getElementById('ipaDisplay').style.display = "none";
        document.getElementById('glossContainer').innerHTML = "";
        return;
      }

      try {
        const resp = await fetch('/api/translate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        });
        const data = await resp.json();
        currentUniverlan = data.univerlan;
        document.getElementById('univerlanOutput').innerText = data.univerlan;
        
        const ipaEl = document.getElementById('ipaDisplay');
        ipaEl.innerText = "IPA: " + data.ipa;
        ipaEl.style.display = "inline-block";

        const glossEl = document.getElementById('glossContainer');
        glossEl.innerHTML = "";
        data.gloss.forEach(item => {
          const span = document.createElement('span');
          span.className = 'gloss-item';
          span.innerText = item;
          glossEl.appendChild(span);
        });
      } catch (err) {
        console.error("Translation failed", err);
      }
    }

    // Auto translate as user types with debounce
    let debounceTimer;
    document.getElementById('englishInput').addEventListener('input', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(handleTranslate, 250);
    });

    function speakBrowser() {
      if (!currentUniverlan) return;
      if (!('speechSynthesis' in window)) {
        alert("Web Speech API not supported in this browser.");
        return;
      }
      // Prepare speech phonetic script for browser
      const clean = currentUniverlan.replace(/-/g, ' ');
      const utterance = new SpeechSynthesisUtterance(clean);
      utterance.rate = 0.9;
      speechSynthesis.speak(utterance);
    }

    async function speakBackend() {
      if (!currentUniverlan) return;
      await fetch('/api/speak', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: currentUniverlan })
      });
    }
  </script>
</body>
</html>
"""


class UniverlanHandler(http.server.BaseHTTPRequestHandler):

    translator = UniverlanTranslator()
    tts = SpeechSynthesizer()

    def do_GET(self) -> None:
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self) -> None:
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8")
        data = json.loads(body) if body else {}

        if self.path == "/api/translate":
            text = data.get("text", "")
            res = self.translator.translate(text)
            resp_data = {
                "english": res.english_source,
                "univerlan": res.univerlan_text,
                "ipa": res.ipa_transcription,
                "gloss": res.gloss,
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp_data).encode("utf-8"))

        elif self.path == "/api/speak":
            text = data.get("text", "")
            self.tts.speak(text)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        else:
            self.send_response(404)
            self.end_headers()


def run_server(port: int = 8080) -> None:
    server_address = ("127.0.0.1", port)
    httpd = http.server.HTTPServer(server_address, UniverlanHandler)
    print(f"[*] Univerlan Web Terminal running at http://127.0.0.1:{port}/")
    print("[*] Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        httpd.server_close()


if __name__ == "__main__":
    run_server()

#!/usr/bin/env python3
"""Interactive Web Translator, Audio Synthesizer, Speech-to-Text, and Grammar Portal for Univerlan.

Serves an interstellar-styled user interface for:
- Real-time translation (English -> Univerlan)
- Speech-to-Text (voice dictation into translator)
- Text-to-Speech (native Web Speech API & Windows SAPI)
- Interactive Grammar, Phonology, and Wilkins ontology explorer
Zero external dependencies required (uses standard library http.server).
"""

from __future__ import annotations
import http.server
import json
import os
import sys

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
  <title>UNIVERLAN - Interstellar Conlang Terminal & Grammar Portal</title>
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
      --danger: #ef4444;
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
    nav.tabs {
      display: flex;
      gap: 1rem;
      max-width: 1100px;
      width: 100%;
      margin: 1.5rem auto 0;
      padding: 0 1.5rem;
    }
    .tab-btn {
      background: #111827;
      border: 1px solid var(--border);
      color: var(--muted);
      padding: 0.6rem 1.2rem;
      border-radius: 8px 8px 0 0;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.2s;
    }
    .tab-btn.active {
      background: var(--card-bg);
      color: var(--primary);
      border-bottom: 2px solid var(--primary);
    }
    main {
      flex: 1;
      max-width: 1100px;
      width: 100%;
      margin: 0 auto 2rem;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }
    .tab-pane { display: none; }
    .tab-pane.active { display: block; }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
      margin-bottom: 1.5rem;
    }
    .card h2 {
      font-size: 1.15rem;
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
    button.stt-btn {
      background: #065f46;
      color: #ecfdf5;
      border: 1px solid #059669;
    }
    button.stt-btn.listening {
      background: #dc2626;
      border-color: #ef4444;
      animation: pulse 1.2s infinite;
    }
    @keyframes pulse {
      0% { opacity: 1; }
      50% { opacity: 0.6; }
      100% { opacity: 1; }
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
    table.data-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 1rem;
      font-size: 0.9rem;
    }
    table.data-table th, table.data-table td {
      border: 1px solid var(--border);
      padding: 0.6rem 0.8rem;
      text-align: left;
    }
    table.data-table th {
      background: #1e293b;
      color: var(--primary);
    }
    table.data-table tr:nth-child(even) {
      background: #0d1322;
    }
    code {
      font-family: var(--font-mono);
      background: #070a12;
      padding: 0.15rem 0.4rem;
      border-radius: 4px;
      color: #38bdf8;
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
      <span class="badge">INTERSTELLAR CONLANG TERMINAL</span>
    </div>
    <div style="font-size: 0.85rem; color: var(--muted);">
      Bijective Phonology &bull; John Wilkins Matrix &bull; SVO
    </div>
  </header>

  <nav class="tabs">
    <button class="tab-btn active" onclick="switchTab('translator')">&#128483; Translator, TTS &amp; STT</button>
    <button class="tab-btn" onclick="switchTab('grammar')">&#128214; Grammar &amp; Syntax</button>
    <button class="tab-btn" onclick="switchTab('phonology')">&#127911; Phonology &amp; IPA</button>
    <button class="tab-btn" onclick="switchTab('wilkins')">&#128506; Wilkins Matrix</button>
  </nav>

  <main>
    <!-- TAB 1: TRANSLATOR, TTS & STT -->
    <div id="pane-translator" class="tab-pane active">
      <section class="card">
        <h2>&#9881; English &rarr; Univerlan Rationalized Translation</h2>
        
        <div class="translator-grid">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
              <label style="font-size:0.85rem; color:var(--muted);">English Source:</label>
              <button id="sttBtn" class="stt-btn" onclick="toggleSpeechToText()">&#127908; Dictate (STT)</button>
            </div>
            <textarea id="englishInput" placeholder="Type or speak English sentence here... (e.g. Please lift the cargo and push it into the starship.)"></textarea>
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
          <button onclick="handleTranslate()">&#9881; Translate</button>
          <button class="secondary" onclick="speakBrowser()">&#128266; Read Aloud (Browser TTS)</button>
          <button class="secondary" onclick="speakBackend()">&#128266; Read Aloud (Windows SAPI)</button>
        </div>

        <div id="glossContainer" class="gloss-list"></div>
      </section>
    </div>

    <!-- TAB 2: GRAMMAR & SYNTAX -->
    <div id="pane-grammar" class="tab-pane">
      <section class="card">
        <h2>&#128214; Univerlan Grammar Rules</h2>
        <p style="color:var(--muted); margin-bottom:1rem;">
          Univerlan eliminates all irregular verbs, capricious plurals, and arbitrary grammatical gender.
        </p>
        
        <h3 style="color:#38bdf8; font-size:1rem; margin-top:1rem;">1. Sentence Structure: Strict SVO</h3>
        <p style="color:#d1d5db; font-size:0.9rem; margin-top:0.3rem;">
          Every declarative, interrogative, and negative sentence follows <code>Subject + Modifiers + Verb + Object</code>.
        </p>

        <h3 style="color:#38bdf8; font-size:1rem; margin-top:1rem;">2. Pronominal System</h3>
        <table class="data-table">
          <tr><th>Person</th><th>Singular</th><th>Plural</th><th>Possessive (-n)</th></tr>
          <tr><td>1st</td><td><code>mi</code> (I / me)</td><td><code>wi</code> (we / us)</td><td><code>min</code> (my), <code>win</code> (our)</td></tr>
          <tr><td>2nd</td><td><code>yu</code> (you)</td><td><code>yus</code> (you all)</td><td><code>yun</code> (your)</td></tr>
          <tr><td>3rd (M)</td><td><code>hi</code> (he / him)</td><td><code>dey</code> (they / them)</td><td><code>hin</code> (his), <code>deyn</code> (their)</td></tr>
          <tr><td>3rd (F)</td><td><code>xe</code> (she / her)</td><td><code>dey</code> (they / them)</td><td><code>xen</code> (her), <code>deyn</code> (their)</td></tr>
          <tr><td>3rd (N)</td><td><code>it</code> (it)</td><td><code>dey</code> (they)</td><td><code>itn</code> (its)</td></tr>
        </table>

        <h3 style="color:#38bdf8; font-size:1rem; margin-top:1rem;">3. Verbal System: 100% Regular</h3>
        <table class="data-table">
          <tr><th>Tense / Aspect</th><th>Formation</th><th>Example with <code>go</code></th><th>Example with <code>bay</code> (buy)</th></tr>
          <tr><td>Present / Habitual</td><td><code>[Root]</code></td><td><code>mi go</code> (I go)</td><td><code>hi bay</code> (He buys)</td></tr>
          <tr><td>Definite Past</td><td><code>[Root] + -ed</code></td><td><code>mi goed</code> (I went)</td><td><code>hi bayed</code> (He bought)</td></tr>
          <tr><td>Future</td><td><code>wil + [Root]</code></td><td><code>mi wil go</code> (I will go)</td><td><code>hi wil bay</code> (He will buy)</td></tr>
          <tr><td>Continuous</td><td><code>is + [Root]-ing</code></td><td><code>mi is going</code></td><td><code>hi is baying</code></td></tr>
          <tr><td>Negation</td><td><code>no + [Verb]</code></td><td><code>mi no go</code> (I do not go)</td><td><code>hi no goed</code> (He did not go)</td></tr>
        </table>
      </section>
    </div>

    <!-- TAB 3: PHONOLOGY & IPA -->
    <div id="pane-phonology" class="tab-pane">
      <section class="card">
        <h2>&#127911; Bijective 1:1 Phonology (1 Sign = 1 Sound)</h2>
        <p style="color:var(--muted); margin-bottom:1rem;">
          No silent letters, no capricious geminates, no ambiguity.
        </p>

        <table class="data-table">
          <tr><th>Letter</th><th>IPA Sound</th><th>Standard Word</th><th>Cleaned Historical English</th></tr>
          <tr><td><code>a</code></td><td>[a]</td><td><code>kat</code> (cat)</td><td>father, cat</td></tr>
          <tr><td><code>e</code></td><td>[ɛ]</td><td><code>bed</code> (bed)</td><td>send, bed</td></tr>
          <tr><td><code>i</code></td><td>[i]</td><td><code>sip</code> (ship, see)</td><td>machine, see</td></tr>
          <tr><td><code>o</code></td><td>[ɔ]</td><td><code>dok</code> (dock)</td><td>dock, law</td></tr>
          <tr><td><code>u</code></td><td>[u]</td><td><code>lun</code> (moon)</td><td>moon, blue</td></tr>
          <tr><td><code>c</code></td><td>[tʃ]</td><td><code>cek</code> (check)</td><td>replaces <em>ch</em></td></tr>
          <tr><td><code>x</code></td><td>[ʃ]</td><td><code>xip</code> (ship)</td><td>replaces <em>sh</em></td></tr>
          <tr><td><code>j</code></td><td>[dʒ]</td><td><code>jop</code> (job)</td><td>joy, judge</td></tr>
          <tr><td><code>k</code></td><td>[k]</td><td><code>kargo</code> (cargo)</td><td>replaces hard <em>c</em> &amp; <em>q</em></td></tr>
          <tr><td><code>s</code></td><td>[s]</td><td><code>sun</code> (sun)</td><td>always sharp [s]</td></tr>
        </table>
      </section>
    </div>

    <!-- TAB 4: WILKINS MATRIX -->
    <div id="pane-wilkins" class="tab-pane">
      <section class="card">
        <h2>&#128506; John Wilkins Conceptual Matrix</h2>
        <p style="color:var(--muted); margin-bottom:1rem;">
          Inspiration from John Wilkins (1668): arbitrary verbal roots are decomposed into primary relational atoms.
        </p>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:1rem;">
          <div style="background:#070a12; padding:1rem; border-radius:8px; border:1px solid #1f2937;">
            <strong style="color:#38bdf8;">lift / raise</strong> &rarr; <code>mov-up</code><br>
            <small style="color:var(--muted);">Vertical kinetic vector (+)</small>
          </div>
          <div style="background:#070a12; padding:1rem; border-radius:8px; border:1px solid #1f2937;">
            <strong style="color:#38bdf8;">drop / fall</strong> &rarr; <code>mov-don</code><br>
            <small style="color:var(--muted);">Vertical kinetic vector (-)</small>
          </div>
          <div style="background:#070a12; padding:1rem; border-radius:8px; border:1px solid #1f2937;">
            <strong style="color:#38bdf8;">pull / drag</strong> &rarr; <code>mov-tu-mi</code><br>
            <small style="color:var(--muted);">Egocentric vector (towards self)</small>
          </div>
          <div style="background:#070a12; padding:1rem; border-radius:8px; border:1px solid #1f2937;">
            <strong style="color:#38bdf8;">push / repel</strong> &rarr; <code>mov-fro-mi</code><br>
            <small style="color:var(--muted);">Egocentric vector (away from self)</small>
          </div>
          <div style="background:#070a12; padding:1rem; border-radius:8px; border:1px solid #1f2937;">
            <strong style="color:#38bdf8;">enter / board</strong> &rarr; <code>mov-in</code><br>
            <small style="color:var(--muted);">Boundary vector (inside)</small>
          </div>
          <div style="background:#070a12; padding:1rem; border-radius:8px; border:1px solid #1f2937;">
            <strong style="color:#38bdf8;">exit / disembark</strong> &rarr; <code>mov-ut</code><br>
            <small style="color:var(--muted);">Boundary vector (outside)</small>
          </div>
        </div>
      </section>
    </div>
  </main>

  <footer>
    Univerlan Open Source Project &bull; MIT License &bull; Inspired by John Wilkins, IPA &amp; Rational Lingua Francas
  </footer>

  <script>
    let currentUniverlan = "";
    let isRecording = false;
    let recognition = null;

    function switchTab(tabId) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      event.target.classList.add('active');
      document.getElementById('pane-' + tabId).classList.add('active');
    }

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

    let debounceTimer;
    document.getElementById('englishInput').addEventListener('input', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(handleTranslate, 250);
    });

    // --- Text-to-Speech (TTS) ---
    function speakBrowser() {
      if (!currentUniverlan) return;
      if (!('speechSynthesis' in window)) {
        alert("Web Speech API not supported in this browser.");
        return;
      }
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

    // --- Speech-to-Text (STT) ---
    function toggleSpeechToText() {
      const btn = document.getElementById('sttBtn');
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

      if (!SpeechRecognition) {
        alert("Speech recognition is not supported in this browser. Please use Chrome, Edge, or Safari.");
        return;
      }

      if (isRecording) {
        if (recognition) recognition.stop();
        isRecording = false;
        btn.classList.remove('listening');
        btn.innerHTML = "&#127908; Dictate (STT)";
        return;
      }

      recognition = new SpeechRecognition();
      recognition.lang = 'en-US';
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onstart = () => {
        isRecording = true;
        btn.classList.add('listening');
        btn.innerHTML = "&#9209; Listening...";
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById('englishInput').value = transcript;
        handleTranslate();
      };

      recognition.onerror = (event) => {
        console.error("STT error:", event.error);
        isRecording = false;
        btn.classList.remove('listening');
        btn.innerHTML = "&#127908; Dictate (STT)";
      };

      recognition.onend = () => {
        isRecording = false;
        btn.classList.remove('listening');
        btn.innerHTML = "&#127908; Dictate (STT)";
      };

      recognition.start();
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

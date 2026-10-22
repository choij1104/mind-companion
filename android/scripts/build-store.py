#!/usr/bin/env python3
"""Builds android/www, the Google Play build of Mind Companion, from the repository's index.html.

The web app in the repository root is not modified. The store build differs in these ways only:

  1. Offline. The optional "Conversation" setting (a user-supplied relay address that forwards
     questions to an AI service) is left out: its Settings card is removed and the relay branch in
     handleQuestion() is disabled, so every answer comes from the app's built-in answers and the
     data saved on the device. The web version keeps the feature.
  2. No service worker. Inside the app the files are already on the device.
  3. Native speech and file saving. Android WebView has no Web Speech API, so a small shim
     (scripts/native-shim.js) provides window.SpeechRecognition and window.speechSynthesis on top
     of the @capacitor-community/speech-recognition and text-to-speech plugins, and makes
     <a download> links (backup, report, CSV) open the Android share sheet through
     @capacitor/filesystem and @capacitor/share. In a browser the shim does nothing.
  4. A marker <meta name="mind-companion-build" content="store">.

Every text replacement must match exactly once, or the build fails.
Run `npm ci` in android/ first so @capacitor/core is present.
"""
import os, re, shutil, sys

AND = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(AND)
OUT = os.path.join(AND, "www")

def die(msg):
    sys.exit(f"build-store: {msg}")

def sub1(old, new, s, what):
    n = s.count(old)
    if n != 1:
        die(f"{what}: expected 1 match, found {n}")
    return s.replace(old, new)

t = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

t = sub1('<head>\n<meta charset="UTF-8">', '<head>\n<meta charset="UTF-8">\n<meta name="mind-companion-build" content="store">', t, "charset meta")

# 1. Offline: remove the Conversation card and disable the relay branch.
m = re.search(r'\n    <div class="card">\n      <h3 id="setAiTitle">.*?\n    </div>\n', t, re.S)
if not m or t.count('id="setAiTitle"') != 1:
    die("Conversation settings card not found exactly once")
card = m.group(0)
if card.count('<div class="card">') != 1 or 'relayUrl' not in card:
    die("Conversation card boundaries look wrong")
t = t.replace(card, "\n")
t = sub1("  if (DB.relayUrl){\n    setReply(t().thinking);", "  if (false){ /* store build: no relay */\n    setReply(t().thinking);", t, "relay branch")

# 2. No service worker.
t = sub1("if ('serviceWorker' in navigator && location.protocol.startsWith('http')){",
         "if (false){ /* store build: no service worker */", t, "service worker registration")

# Checks ------------------------------------------------------------------------------
for bad in ('id="relayUrl"', "workers.dev", "fonts.googleapis", "fonts.gstatic", "NAMRU", "TCCC-grade"):
    if bad in t:
        die(f"'{bad}' still present")
if re.search(r'<(script|link|img)[^>]+(src|href)="https?://', t):
    die("external resource reference in index.html")
for lang_key in ("langEn", "langKo", "langEs", "langJa"):
    if f'id="{lang_key}"' not in t:
        die(f"language button {lang_key} missing")

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)

# Capacitor runtime + native shim, loaded before any app script.
cap = os.path.join(AND, "node_modules", "@capacitor", "core", "dist", "capacitor.js")
if not os.path.isfile(cap):
    die("@capacitor/core dist/capacitor.js missing: run npm ci in android/ first")
shutil.copy(cap, os.path.join(OUT, "capacitor.js"))
shutil.copy(os.path.join(AND, "scripts", "native-shim.js"), os.path.join(OUT, "native-shim.js"))
i = t.find("<script")
if i < 0:
    die("no <script> tag")
t = t[:i] + '<script src="capacitor.js"></script>\n<script src="native-shim.js"></script>\n' + t[i:]

open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(t)
for f in ("manifest.json", "icon-192.png", "icon-512.png", "icon-maskable-512.png", "apple-touch-icon.png", "favicon-32.png"):
    p = os.path.join(ROOT, f)
    if os.path.exists(p):
        shutil.copy(p, os.path.join(OUT, f))
print(f"build-store: Mind Companion written to {OUT} ({len(t)} bytes)")

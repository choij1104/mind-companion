#!/usr/bin/env python3
"""Mind Companion — release guards.

Checks the things that are easy to get wrong and expensive to ship wrong:
version stamps that disagree, safety text that has gone missing, a licence
statement that contradicts the LICENSE file, and any new outbound request.

Run from the repository root:  python3 .github/scripts/guards.py
Exit code 1 if any check fails.
"""
import re
import sys

FAILS = []
NOTES = []


def read(p):
    try:
        return open(p, encoding="utf-8").read()
    except FileNotFoundError:
        FAILS.append(f"{p} is missing from the repository")
        return ""


def check_versions(index, sw):
    app = re.search(r"APP_VERSION\s*=\s*'([^']+)'", index)
    foot = re.search(r"Mind Companion v([0-9.]+)", index)
    cache = re.search(r"CACHE\s*=\s*'mind-companion-v([0-9.]+)'", sw)
    if not app:
        FAILS.append("APP_VERSION not found in index.html")
    if not foot:
        FAILS.append("no 'Mind Companion v…' version string in the page footer")
    if not cache:
        FAILS.append("CACHE in sw.js is not named 'mind-companion-v…'")
    if app and foot and cache:
        v = {app.group(1), foot.group(1), cache.group(1)}
        if len(v) != 1:
            FAILS.append(
                f"version stamps disagree — APP_VERSION={app.group(1)}, "
                f"footer={foot.group(1)}, sw.js cache={cache.group(1)}. "
                "A release that forgets the sw.js bump leaves old files on phones.")
        else:
            NOTES.append(f"version {app.group(1)} consistent across index.html and sw.js")


def check_safety_text(index):
    # every language table must carry these, non-empty
    keys = ["disclaimer", "frTitle", "frOk", "medDisclaim", "wDisclaim", "wCrisis",
            "wResultHigh", "wResultLow", "call911"]
    langs = ["en", "ko", "es", "ja"]
    blocks = {}
    for lang in langs:
        m = re.search(r"(?m)^\s*" + lang + r"\s*:\s*\{", index)
        if not m:
            FAILS.append(f"language table '{lang}' is missing")
            continue
        depth, i, in_s, q, esc = 0, m.end() - 1, False, "", False
        while i < len(index):
            c = index[i]
            if in_s:
                if esc: esc = False
                elif c == "\\": esc = True
                elif c == q: in_s = False
            elif c in "'\"`": in_s, q = True, c
            elif c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    blocks[lang] = index[m.end() - 1:i]
                    break
            i += 1
    for lang, body in blocks.items():
        for k in keys:
            hit = re.search(r"(?<![\w$])" + k + r"\s*:\s*(['\"`])(.*?)(?<!\\)\1", body, re.S)
            if not hit:
                FAILS.append(f"safety text '{k}' is missing from the {lang} table")
            elif not hit.group(2).strip():
                FAILS.append(f"safety text '{k}' is empty in the {lang} table")
    if not FAILS:
        NOTES.append(f"safety text present in all {len(blocks)} languages")

    for token, what in [("911", "the emergency number"), ("988", "the crisis line")]:
        if token not in index:
            FAILS.append(f"{what} ({token}) no longer appears anywhere in the app")


def check_licence(readme, licence):
    if "PROPRIETARY" not in licence.upper():
        FAILS.append("LICENSE no longer reads as proprietary — confirm this is intended")
    if re.search(r"\bMIT\b", readme):
        FAILS.append(
            "README calls the licence MIT while LICENSE is proprietary. "
            "MIT would permit copying, modifying and commercial use.")
    if "HAKOYA" not in readme and "Jae Hyek Choi" not in readme:
        FAILS.append("README no longer carries the copyright line")


def check_no_external(index):
    bad = []
    for m in re.finditer(r'(?:src|href)\s*=\s*["\'](https?://[^"\']+)', index):
        url = m.group(1)
        if url.startswith("http"):
            bad.append(url)
    if bad:
        FAILS.append("external resource referenced in index.html: " + ", ".join(sorted(set(bad))))
    for pat, what in [(r"googletagmanager|google-analytics|gtag\(", "analytics"),
                      (r"cdn\.jsdelivr|unpkg\.com|cdnjs\.", "a CDN script")]:
        if re.search(pat, index, re.I):
            FAILS.append(f"{what} found in index.html — the app must make no third-party requests")
    if not bad:
        NOTES.append("no external resources referenced")


def check_privacy_matches_storage(index, privacy):
    """If the app stores a new kind of information, the privacy policy has to say so."""
    pairs = [("DB.mood", "mood"), ("DB.checks", "check"), ("DB.counselor", "counselor")]
    for token, word in pairs:
        if token in index and word.lower() not in privacy.lower():
            FAILS.append(
                f"the app stores {token.split('.')[1]} but PRIVACY.md never mentions '{word}'")
    NOTES.append("privacy policy covers what the app stores")


index = read("index.html")
sw = read("sw.js")
readme = read("README.md")
licence = read("LICENSE")
privacy = read("PRIVACY.md")

if index:
    check_versions(index, sw)
    check_safety_text(index)
    check_no_external(index)
    check_privacy_matches_storage(index, privacy)
check_licence(readme, licence)

for n in NOTES:
    print(f"  ok   {n}")
if FAILS:
    print()
    for f in FAILS:
        print(f"  FAIL {f}")
    print(f"\n{len(FAILS)} guard(s) failed.")
    sys.exit(1)
print("\nAll guards passed.")

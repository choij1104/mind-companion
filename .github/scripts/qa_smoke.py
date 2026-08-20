#!/usr/bin/env python3
"""Headless smoke test for Mind Companion.

Usage: python3 qa_smoke.py path/to/index.html [--lang ko] [--shots DIR] [--width 390]

Loads the app in Chromium, accepts the first-run notice, visits every view in
every requested language, and reports console errors, page errors, failed network
requests, undersized touch targets, untranslated element text, and horizontal
overflow. Writes one screenshot per view per language when --shots is given.
Exit code 1 if any error-level finding is present.
"""
import argparse
import json
import os
import pathlib
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("playwright is not installed: pip install playwright --break-system-packages")

VIEWS = ["home", "meds", "contacts", "notes", "well", "sos", "settings"]
MIN_TAP = 44


def run(path, langs, shots, width, height):
    url = pathlib.Path(path).resolve().as_uri()
    findings = {"errors": [], "warnings": [], "views_visited": []}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": width, "height": height},
                                  device_scale_factor=2, locale="en-US")
        page = ctx.new_page()
        page.on("console", lambda m: findings["errors"].append(
            {"type": "console", "text": m.text}) if m.type == "error" else None)
        page.on("pageerror", lambda e: findings["errors"].append(
            {"type": "pageerror", "text": str(e)}))
        page.on("requestfailed", lambda r: findings["warnings"].append(
            {"type": "requestfailed", "text": f"{r.url} — {r.failure}"}))

        page.goto(url)
        page.wait_for_timeout(600)

        # first-run notice
        try:
            page.click("#frOk", timeout=2500)
            page.wait_for_timeout(300)
        except Exception:
            pass

        for lang in langs:
            page.evaluate(f"window.setLang && setLang('{lang}')")
            page.wait_for_timeout(400)
            for v in VIEWS:
                page.evaluate(f"go('{v}')")
                page.wait_for_timeout(300)
                findings["views_visited"].append(f"{lang}/{v}")

                sec = page.query_selector(f"#v-{v}")
                if not sec or not sec.is_visible():
                    findings["errors"].append({"type": "view", "text": f"{lang}/{v} did not render"})
                    continue

                small = page.evaluate("""(sel) => {
                    const out = [];
                    document.querySelectorAll(sel + ' button, ' + sel + ' select, ' + sel + ' input[type=button]')
                      .forEach(b => {
                        const r = b.getBoundingClientRect();
                        if (r.width === 0 && r.height === 0) return;
                        if (r.height < %d || r.width < %d)
                          out.push({t: (b.innerText||b.id||'').trim().slice(0,40),
                                    w: Math.round(r.width), h: Math.round(r.height)});
                      });
                    return out;
                }""" % (MIN_TAP, MIN_TAP), f"#v-{v}")
                for s in small:
                    findings["warnings"].append(
                        {"type": "tap-target", "text": f"{lang}/{v}: \"{s['t']}\" {s['w']}x{s['h']}px < {MIN_TAP}"})

                overflow = page.evaluate(
                    "() => document.documentElement.scrollWidth > window.innerWidth + 1")
                if overflow:
                    findings["errors"].append(
                        {"type": "overflow", "text": f"{lang}/{v} scrolls horizontally at {width}px"})

                # Latin-script check only makes sense for non-Latin interfaces
                if lang in ("ko", "ja"):
                    stray = page.evaluate("""(sel) => {
                        const out = [];
                        const skip = new Set(['datestr','clock','relayUrl','heardTxt','replyTxt']);
                        document.querySelectorAll(sel + ' [id]').forEach(el => {
                          if (skip.has(el.id)) return;
                          const txt = (el.childNodes.length === 1 && el.firstChild.nodeType === 3)
                            ? el.textContent.trim() : '';
                          if (txt && /^[\\x20-\\x7E]+$/.test(txt) && /[A-Za-z]{4,}/.test(txt)
                              && txt.length > 12) out.push({id: el.id, t: txt.slice(0,60)});
                        });
                        return out;
                    }""", f"#v-{v}")
                    for s in stray:
                        findings["warnings"].append(
                            {"type": "untranslated?", "text": f"{lang}/{v} #{s['id']}: {s['t']}"})

                if shots:
                    os.makedirs(shots, exist_ok=True)
                    page.screenshot(path=os.path.join(shots, f"{lang}-{v}.png"), full_page=True)

        browser.close()
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--lang", action="append", default=None,
                    help="repeatable; default en ko es ja")
    ap.add_argument("--shots", default=None)
    ap.add_argument("--width", type=int, default=390)
    ap.add_argument("--height", type=int, default=844)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    f = run(a.path, a.lang or ["en", "ko", "es", "ja"], a.shots, a.width, a.height)

    if a.json:
        print(json.dumps(f, ensure_ascii=False, indent=2))
    else:
        print(f"visited {len(f['views_visited'])} view/language combinations at {a.width}px")
        if f["errors"]:
            print(f"\nERRORS ({len(f['errors'])})")
            for e in f["errors"]:
                print(f"  [{e['type']}] {e['text']}")
        if f["warnings"]:
            print(f"\nwarnings ({len(f['warnings'])})")
            for w in f["warnings"]:
                print(f"  [{w['type']}] {w['text']}")
        if not f["errors"] and not f["warnings"]:
            print("clean — no console errors, overflow, or undersized targets.")
    sys.exit(1 if f["errors"] else 0)


if __name__ == "__main__":
    main()

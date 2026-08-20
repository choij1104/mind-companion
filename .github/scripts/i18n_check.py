#!/usr/bin/env python3
"""Check translation-table parity in Mind Companion's index.html.

Usage: python3 i18n_check.py path/to/index.html [--json]

Reports, per language: missing keys, extra keys, empty values, type mismatches
against the English source table, and strings far longer than their English
counterpart (a layout risk on small screens).
Exit code 1 if any hard problem (missing/extra/empty/type) is found.
"""
import json
import re
import sys

LANGS = ["en", "ko", "es", "ja"]
SOURCE = "en"
LENGTH_RATIO = 1.8   # flag translations this many times longer than English
LENGTH_FLOOR = 24    # ...but only for strings at least this long in English


def find_table(src):
    m = re.search(r"\bconst\s+T\s*=\s*\{", src)
    if not m:
        sys.exit("could not find `const T = {` in the file")
    return m.end() - 1


def block(src, start):
    """Return (body, end_index) for the object literal opening at src[start]=='{'."""
    depth, i, n = 0, start, len(src)
    in_s, quote, esc = False, "", False
    while i < n:
        c = src[i]
        if in_s:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == quote:
                in_s = False
        elif c in "'\"`":
            in_s, quote = True, c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return src[start + 1:i], i
        i += 1
    sys.exit("unbalanced braces while parsing the translation table")


def lang_blocks(src):
    t_start = find_table(src)
    body, _ = block(src, t_start)
    out = {}
    for lang in LANGS:
        m = re.search(r"(?m)^\s*" + lang + r"\s*:\s*\{", body)
        if not m:
            continue
        b, _ = block(body, m.end() - 1)
        out[lang] = b
    return out


def entries(body):
    """Top-level key -> raw value text, for one language block."""
    res, i, n = {}, 0, len(body)
    depth = 0
    in_s, quote, esc = False, "", False
    key, val_start = None, None
    while i < n:
        c = body[i]
        if in_s:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == quote:
                in_s = False
            i += 1
            continue
        if c in "'\"`":
            in_s, quote = True, c
            i += 1
            continue
        if c in "{[(":
            depth += 1
        elif c in "}])":
            depth -= 1
        elif depth == 0:
            if key is None:
                m = re.match(r"([A-Za-z_$][\w$]*)\s*:", body[i:])
                if m:
                    key = m.group(1)
                    i += m.end()
                    val_start = i
                    continue
            elif c == ",":
                res[key] = body[val_start:i].strip()
                key, val_start = None, None
        i += 1
    if key is not None:
        res[key] = body[val_start:].strip()
    return res


def kind(v):
    v = v.strip()
    if v.startswith("["):
        return "array"
    if "=>" in v.split("`")[0].split("'")[0].split('"')[0] or v.startswith("function"):
        return "function"
    return "string"


def plain_len(v):
    return len(re.sub(r"\$\{[^}]*\}", "", v).strip("`'\" "))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    as_json = "--json" in sys.argv
    src = open(path, encoding="utf-8").read()
    blocks = lang_blocks(src)

    missing_langs = [l for l in LANGS if l not in blocks]
    tables = {l: entries(b) for l, b in blocks.items()}
    base = tables.get(SOURCE, {})

    report = {"languages_found": list(tables), "missing_language_tables": missing_langs,
              "key_counts": {l: len(t) for l, t in tables.items()}, "problems": {}, "warnings": {}}

    for lang, tab in tables.items():
        probs, warns = [], []
        if lang != SOURCE:
            for k in base:
                if k not in tab:
                    probs.append({"key": k, "issue": "missing"})
            for k in tab:
                if k not in base:
                    probs.append({"key": k, "issue": "not in English table"})
        for k, v in tab.items():
            if v.strip() in ("''", '""', "``", ""):
                probs.append({"key": k, "issue": "empty value"})
            if lang != SOURCE and k in base and kind(v) != kind(base[k]):
                probs.append({"key": k, "issue": f"type {kind(v)} != English {kind(base[k])}"})
            if lang != SOURCE and k in base and kind(v) == "string":
                el, tl = plain_len(base[k]), plain_len(v)
                if el >= LENGTH_FLOOR and tl > el * LENGTH_RATIO:
                    warns.append({"key": k, "issue": f"{tl} chars vs {el} in English — layout risk"})
                if v.strip() == base[k].strip() and el >= LENGTH_FLOOR:
                    warns.append({"key": k, "issue": "identical to English — possibly untranslated"})
        if probs:
            report["problems"][lang] = probs
        if warns:
            report["warnings"][lang] = warns

    hard = bool(missing_langs) or bool(report["problems"])
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"languages: {', '.join(report['languages_found'])}")
        for l, c in report["key_counts"].items():
            print(f"  {l}: {c} keys")
        if missing_langs:
            print(f"MISSING LANGUAGE TABLES: {', '.join(missing_langs)}")
        for l, ps in report["problems"].items():
            print(f"\nPROBLEMS [{l}] ({len(ps)})")
            for p in ps:
                print(f"  {p['key']}: {p['issue']}")
        for l, ws in report["warnings"].items():
            print(f"\nwarnings [{l}] ({len(ws)})")
            for w in ws:
                print(f"  {w['key']}: {w['issue']}")
        if not hard:
            print("\nOK — all four tables have identical key sets, no empty or mistyped values.")
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()

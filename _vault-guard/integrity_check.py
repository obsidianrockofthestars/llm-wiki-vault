#!/usr/bin/env python3
"""Vault integrity check.

Mechanical enforcement of the rules that matter:

  CRITICAL  missing tail sentinel on a wiki page (the truncation detector)
  CRITICAL  required file missing (CLAUDE.md, wiki/index.md, wiki/digest.md, wiki/log.md)
  CRITICAL  empty (0 byte) file anywhere in a scanned dir
  WARN      wiki page missing a **Summary** line
  WARN      wiki page name not lowercase-with-hyphens
  WARN      orphan wiki page (no inbound [[link]] from any other wiki page)

Exit code 0 = clean or warnings only. Exit code 1 = at least one CRITICAL.
A session that sees exit 1 repairs from the newest snapshot before doing
anything else. Prose is not a gate; this script is.
"""

import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
SCAN_DIRS = ["Raw", "wiki"]
REQUIRED = ["CLAUDE.md", "wiki/index.md", "wiki/digest.md", "wiki/log.md"]
SENTINEL = "<!-- vault-guard: eof -->"
# Files under wiki/ that are logs or rollups rather than pages still carry
# the sentinel. Everything under wiki/ is checked, no exceptions: an
# exception list is where truncations go to hide.

criticals = []
warnings = []


def check_required():
    for rel in REQUIRED:
        p = VAULT / rel
        if not p.is_file():
            criticals.append(f"required file missing: {rel}")


def check_empty_files():
    for d in SCAN_DIRS:
        base = VAULT / d
        if not base.is_dir():
            criticals.append(f"scan dir missing: {d}/")
            continue
        for p in sorted(base.rglob("*")):
            if p.is_file() and p.stat().st_size == 0:
                criticals.append(f"empty file: {p.relative_to(VAULT)}")


def check_wiki_pages():
    wiki = VAULT / "wiki"
    if not wiki.is_dir():
        return
    pages = sorted(wiki.rglob("*.md"))
    all_text = {}
    for p in pages:
        rel = p.relative_to(VAULT)
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            criticals.append(f"not valid UTF-8: {rel}")
            continue
        all_text[p] = text
        if text.rstrip().split("\n")[-1].strip() != SENTINEL:
            criticals.append(f"missing tail sentinel: {rel}")
        if p.name not in ("log.md",) and "**Summary**" not in text:
            warnings.append(f"no **Summary** line: {rel}")
        if not re.fullmatch(r"[a-z0-9][a-z0-9\-]*\.md", p.name):
            warnings.append(f"page name not lowercase-with-hyphens: {rel}")

    # Orphan detection. index.md, digest.md and log.md are hubs, not orphans.
    hubs = {"index.md", "digest.md", "log.md"}
    link_re = re.compile(r"\[\[([^\]|#]+)")
    linked = set()
    for p, text in all_text.items():
        for m in link_re.finditer(text):
            linked.add(m.group(1).strip().lower())
    for p in all_text:
        if p.name in hubs:
            continue
        stem = p.stem.lower()
        if stem not in linked:
            warnings.append(f"orphan page (no inbound [[link]]): {p.relative_to(VAULT)}")


def main():
    check_required()
    check_empty_files()
    check_wiki_pages()

    print(f"vault: {VAULT}")
    for c in criticals:
        print(f"CRITICAL  {c}")
    for w in warnings:
        print(f"WARN      {w}")
    if criticals:
        print(f"\nRESULT: {len(criticals)} CRITICAL, {len(warnings)} warnings. "
              "Repair from the newest clean snapshot before other work.")
        return 1
    print(f"\nRESULT: CLEAN ({len(warnings)} warnings).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Session start gate.

Run this FIRST in every AI session, before trusting or building on any
vault content. One pass does two jobs:

  1. GATE      runs integrity_check.py; a CRITICAL blocks the session
  2. CONTEXT   prints the Tier-0 digest, the head of the index, and the
               last three session logs INTO the transcript, so the session
               provably loaded its context

A session may not claim a clean start without this output present in its
transcript. That sentence is the point: the gate produces evidence, not
just a feeling.

Exit code 0 = gate passed. Exit code 1 = repair from the newest snapshot
before doing anything else.
"""

import subprocess
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
BAR = "=" * 72


def section(title):
    print(f"\n{BAR}\n{title}\n{BAR}")


def show_file(path, max_lines=None):
    if not path.is_file():
        print(f"[missing: {path.relative_to(VAULT)}]")
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    if max_lines is not None:
        lines = lines[:max_lines]
    print("\n".join(lines))


def main():
    section("STEP 1  INTEGRITY GATE  (_vault-guard/integrity_check.py)")
    check = subprocess.run(
        [sys.executable, str(VAULT / "_vault-guard" / "integrity_check.py")]
    )
    if check.returncode != 0:
        section("GATE RESULT")
        print("FAIL. Do not build on this vault. Repair the CRITICAL files from")
        print("the newest clean snapshot in _vault-guard/snapshots/ (selected by")
        print("filename timestamp), re-run this script, then log the repair.")
        return 1

    section("STEP 2  TIER-0 DIGEST  (wiki/digest.md)")
    show_file(VAULT / "wiki" / "digest.md")

    section("STEP 3  MOST RECENT WIKI ACTIVITY  (head of wiki/index.md)")
    show_file(VAULT / "wiki" / "index.md", max_lines=40)

    section("STEP 4  LAST 3 SESSION LOGS  (Raw/03 - Session Logs/)")
    logs_dir = VAULT / "Raw" / "03 - Session Logs"
    logs = sorted(
        (p for p in logs_dir.glob("*.md")) if logs_dir.is_dir() else [],
        key=lambda p: p.name,
        reverse=True,
    )[:3]
    if logs:
        for p in logs:
            print(f"  {p.name}")
        print("\n  ^ open any of these BEFORE building on prior state. A stale")
        print("    assumption about what a previous session decided is the most")
        print("    expensive kind of mistake here.")
    else:
        print("  (no session logs yet)")

    section("GATE RESULT")
    print("PASS. Integrity clean, and the context above is now IN the transcript.")
    print("A session may not claim a clean start without this output present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

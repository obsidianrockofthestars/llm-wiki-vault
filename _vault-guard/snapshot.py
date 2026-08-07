#!/usr/bin/env python3
"""Vault snapshot.

Creates a timestamped tar.gz of the vault's content layers (CLAUDE.md,
Raw/, wiki/, templates/, docs/) in _vault-guard/snapshots/ and prunes to
the newest KEEP snapshots.

Run before any bulk operation and at the end of every session. Snapshots
are the repair path when the integrity gate fails: cheap insurance, taken
often, pruned automatically.
"""

import tarfile
import time
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
SNAP_DIR = VAULT / "_vault-guard" / "snapshots"
INCLUDE = ["CLAUDE.md", "Raw", "wiki", "templates", "docs"]
KEEP = 14


def main():
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y-%m-%d_%H%M%S")
    out = SNAP_DIR / f"vault_{stamp}.tar.gz"

    with tarfile.open(out, "w:gz") as tar:
        for rel in INCLUDE:
            p = VAULT / rel
            if p.exists():
                tar.add(p, arcname=rel)

    size_kb = out.stat().st_size / 1024
    print(f"snapshot written: {out.relative_to(VAULT)} ({size_kb:.0f} KB)")

    snaps = sorted(SNAP_DIR.glob("vault_*.tar.gz"), key=lambda p: p.name)
    while len(snaps) > KEEP:
        victim = snaps.pop(0)
        victim.unlink()
        print(f"pruned old snapshot: {victim.name}")

    print(f"snapshots kept: {len(snaps)} (max {KEEP})")


if __name__ == "__main__":
    main()

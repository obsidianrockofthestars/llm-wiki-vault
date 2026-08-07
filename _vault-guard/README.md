# _vault-guard

The mechanical layer. Three scripts, no dependencies beyond the Python 3 standard library.

| Script | When | What |
|---|---|---|
| `session_start.py` | FIRST action of every AI session | Runs the integrity gate, then prints the digest, index head, and last 3 session logs into the transcript. Exit 1 blocks the session. |
| `integrity_check.py` | Inside the gate, and before sign-off | Tail sentinels on every wiki page, required files present, no empty files, format warnings, orphan detection. Exit 1 on any CRITICAL. |
| `snapshot.py` | Before bulk ops and at session end | Timestamped tar.gz of the content layers into `snapshots/`, keeps the newest 14. |

## Why this exists

An LLM agent working in long sessions will eventually truncate a file mid-write, forget an end-of-session step, or log work that did not land on disk. Not maliciously, statistically. Rules written as prose fail exactly when they are needed. Rules written as scripts with non-zero exits do not.

The tail sentinel (`<!-- vault-guard: eof -->` as the last line of every wiki page) is the cheapest truncation detector there is: if a write gets cut off, the sentinel is the first thing missing, and the next session's gate catches it before anyone builds on a half-file.

## Repair procedure

When the gate fails:

1. Read the CRITICAL lines. They name exact files.
2. Find the newest snapshot in `snapshots/` by filename timestamp.
3. Extract ONLY the damaged files from it (do not blanket-restore; another session may have written newer, valid content elsewhere):
   `tar -xzf _vault-guard/snapshots/vault_<stamp>.tar.gz wiki/damaged-page.md`
4. Re-run `session_start.py` until it passes.
5. Log the incident: what broke, what was restored, what rule change prevents a repeat.

# Lessons: the failure modes we hit so you don't have to

Every rule in this repo exists because something broke. These are the generalized war stories from months of running an LLM-maintained vault daily, personal details stripped, mechanics intact. Each lesson ends with the rule it produced.

## 1. Prose is not a gate

Early on, the vault's rules lived as paragraphs in the instructions file: "always verify writes," "always end the session with a checkpoint." Every one of them was eventually skipped, not through malice, but because a long session's attention is statistical. The rules that stopped failing are the ones that became scripts with non-zero exit codes.

**Rule:** when a rule matters, give it a script. An instruction is a request; an exit code is a gate.

## 2. Files truncate silently

File-writing tools, especially over network mounts, occasionally cut a long write short and report success. A wiki built on a half-written page compounds the damage every session that reads it. The fix costs one line: every page ends with a fixed sentinel comment, and the integrity check treats a missing sentinel as CRITICAL.

**Rule:** tail-sentinel every generated file, verify line counts after non-trivial writes.

## 3. The agent will log work that did not happen

A log entry is generated text like any other; nothing about writing "updated wiki/x.md" requires wiki/x.md to have actually changed. We hit a case where a stale temp file from a previous session got filed as fresh work, and the checker said OK because it checked consistency, not truth.

**Rule:** verify before you log. A checkpoint reports what IS on disk, never what was intended. Where possible, make the checker compare the log against reality, not against itself.

## 4. A checker that runs its own generator can never fail

We once had a verification sweep that regenerated the thing it was checking and then diffed. Green every time, informative never. The same trap wears many costumes: a test that mocks the component under test, an audit prompt that asks the author to grade itself.

**Rule:** the instrument must be able to fail. If you cannot describe the input that would make the check go red, the check is decoration.

## 5. Green tests do not mean a working product

A large suite passed while three user-facing defects shipped, because the tests verified internals and nobody asked what a user actually sees. One human question ("walk me through what the customer sees") caught all three in minutes.

**Rule:** surface verification is its own step. After the mechanical checks, describe the user-visible result and check THAT.

## 6. Snapshot before bulk, restore surgically

Bulk operations (mass renames, restructures, big ingests) are where one bad regex eats a folder. Snapshots made this survivable. But a blanket restore has its own failure mode: it can overwrite newer valid work with older files, especially when more than one session touches the vault.

**Rule:** snapshot before every bulk operation. On failure, restore ONLY the damaged files from the newest clean snapshot, never the whole vault.

## 7. Two writers, one file, silent loss

Two AI sessions appending to the same log concurrently produced a false "truncation" alarm, and the obvious repair would have destroyed the other session's newer entries. The file was not damaged; the reader's assumption was stale.

**Rule:** re-read a file immediately before repairing it, and prefer append-only structures for anything two sessions might touch.

## 8. Immutability is what makes the wiki safe to be wrong

The wiki layer can afford aggressive synthesis and the occasional bad merge precisely because Raw/ is untouchable. Every mistake above was recoverable because the source layer could not be edited by the agent at all.

**Rule:** the agent never modifies Raw/. Derived layers may be rebuilt; sources may not.

## 9. Distant rewards do not change behavior (yes, this applies to the vault too)

The maintenance steps that survive are the ones that pay off inside the same session (the gate prints your context while it verifies, so running it is never pure overhead). Steps that only pay off someday get skipped. Design your own guard rails so the compliant path is also the convenient path.

**Rule:** bundle verification with something the session wants anyway.

## 10. Record things so they can be acted on, not just remembered

A record that says "31 events were created" is half a record if acting on it later requires re-finding all 31 by hand. Store the identifiers, paths, and exact commands next to the prose.

**Rule:** every log entry should let a future session act without re-research. Prose plus pointers, always.

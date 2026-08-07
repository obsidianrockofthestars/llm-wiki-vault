# LLM Wiki Vault, Operating Manual

A living knowledge system built on Andrej Karpathy's LLM Wiki pattern. This file is the operating manual for any AI session working in this vault. Read it first, follow it exactly.

## Purpose

This vault is the shared nervous system between the human and their AI agent. Raw experience, decisions, calibration data, and creative work flow in from the human. The wiki layer synthesizes, cross-links, and surfaces patterns across projects. The agent reads the wiki to generate ideas, push back, and build, then the results feed back into Raw as session logs, completing the cycle.

**The loop:** the human creates, Raw captures, the wiki synthesizes, the agent generates, the human validates, Raw captures the delta, repeat.

## Folder structure

```
Raw/                    source documents (IMMUTABLE, never modify these)
  00 - Core/            identity, priorities, decision style
  01 - Projects/        one note per active project
  02 - Calibration/     raw Q&A calibration data (source of truth)
  03 - Session Logs/    chronological record of AI session outputs
  Templates/            note templates for Raw documents
wiki/                   synthesized, interlinked pages maintained by the agent
  index.md              table of contents for the entire wiki
  digest.md             Tier-0 rollup, read this first
  log.md                append-only record of all wiki operations
templates/              wiki page templates
_vault-guard/           integrity machinery (gate, checks, snapshots)
```

## Startup sequence (for any AI session)

**Step 0 (do this FIRST, before trusting or building on any vault content):** run `python _vault-guard/session_start.py`. It runs the integrity check AND prints the Tier-0 digest, the head of the index, and the last three session log filenames into the transcript in one pass. If it reports any CRITICAL, repair the affected file(s) from the newest clean snapshot (selected by filename timestamp) before doing anything else, then log the repair. This is the backstop that catches a prior session's skipped end-of-session checkpoint.

1. **Read `wiki/digest.md`:** the Tier-0 rollup. This is the cheapest full picture in the vault.
2. **Read `wiki/index.md`:** find relevant wiki pages for the current task.
3. **Read relevant wiki pages:** get synthesized context without burning tokens on full raw files.
4. **Check recent session logs** in `Raw/03 - Session Logs/`, last 2 to 3 for current state.
5. **Deep reference only if needed:** `Raw/02 - Calibration/` for specifics, `Raw/00 - Core/` for full profiles.

The digest plus wiki should give you 80 percent or more of what you need. Go to Raw only for deep dives. Never grep a large operational file for context you could have read from the rollup layer.

## Ingest workflow

When the human adds a new source to `Raw/` and asks you to ingest it:

1. Read the full source document.
2. Discuss key takeaways with the human before writing anything.
3. Create or update wiki pages for each major concept, project, or entity.
4. **Cross-link aggressively.** The value is in connections between ideas, not summaries.
5. Add wiki-links ([[page-name]]) to connect related pages across ALL domains (business, creative, technical, personal).
6. Update `wiki/index.md` with new pages and one-line descriptions.
7. Append an entry to `wiki/log.md` with the date, source name, and what changed.

A single source may touch 10 to 15 wiki pages. That is normal and expected.

### Cross-domain linking examples

These are the connections that make the system more than a filing cabinet:

- A design pattern in one project links to a UX principle in another
- A storytelling rule from creative work links to product onboarding philosophy
- A risk tolerance number from the core profile links to individual purchase decisions
- A pacing ratio from one medium links to loop design in another

**If a concept appears in two domains, it MUST be linked.** That is the whole point.

## Page format

Every wiki page should follow this structure:

```markdown
# Page Title

**Summary**: One to two sentences describing this page.

**Sources**: List of raw source files this page draws from.

**Last updated**: Date of most recent update.

---

Main content goes here. Use clear headings and short paragraphs.

Link to related concepts using [[wiki-links]] throughout the text.

## Cross-domain connections

Where this concept shows up in other projects or domains.

## Related pages

- [[related-concept-1]]
- [[related-concept-2]]

<!-- vault-guard: eof -->
```

## Citation rules

- Every factual claim should reference its source file.
- Use the format (source: Raw/path/to/file.md) after the claim.
- If two sources disagree, note the contradiction explicitly.
- If a claim has no source, mark it as [NEEDS VERIFICATION].
- Session logs are valid sources. They capture real decisions.

## Question answering

When the human asks a question:

1. Read `wiki/digest.md`, then `wiki/index.md`, to find relevant pages.
2. Read those pages and synthesize an answer.
3. Cite specific wiki pages in your response.
4. **Look for cross-domain insights.** The best answers connect things the human has not connected yet.
5. If the answer is not in the wiki, say so clearly.
6. If the answer is valuable, offer to save it as a new wiki page.

Good answers should be filed back into the wiki so they compound over time.

## Session log protocol

After every session where work was done:

1. Create a session log in `Raw/03 - Session Logs/` using the template. Filename form is `YYYY-MM-DD-HHMM - Title.md`, stamped in the human's home timezone.
2. Ingest the session log into the wiki, updating project pages, adding new concepts.
3. Append a `wiki/log.md` entry for the session (newest entry directly under the header; the log is reverse-chronological and append-only by content).
4. Run `python _vault-guard/snapshot.py`, then `python _vault-guard/integrity_check.py`. A non-zero exit blocks sign-off until resolved.

This is how the cycle completes: work done, captured, synthesized, available next session.

## Lint

When the human asks you to lint or audit the wiki:

- Check for contradictions between pages.
- Find orphan pages (no inbound links from other pages).
- **Find missing cross-domain links:** concepts that appear in multiple projects but are not connected.
- Identify concepts mentioned in pages that lack their own page.
- Flag claims that may be outdated based on newer sources or session logs.
- Check that all pages follow the page format above.
- Report findings as a numbered list with suggested fixes.

## Core rules

- **Never modify anything in the `Raw/` folder.** It is immutable source of truth. Adding a new session log to `Raw/03 - Session Logs/` is allowed; rewriting existing documents is not.
- Always update `wiki/index.md` and `wiki/log.md` after changes.
- Keep wiki page names lowercase with hyphens (e.g. `risk-tolerance.md`).
- Every page under `wiki/` ends with the tail sentinel line `<!-- vault-guard: eof -->`. The integrity check treats a missing sentinel as CRITICAL (it is how a truncated write gets caught).
- Cross-link aggressively. Orphan pages are a bug.
- When uncertain about how to categorize something, ask the human.
- Calibration data in `Raw/02 - Calibration/` is sacred. Never delete or modify it.
- **Verify every non-trivial write** (line count and tail check) before trusting it. File tools on some mounts truncate long files silently.
- **Snapshot before any bulk operation.**
- **Verify before you log.** A `log.md` or session log entry must match what actually changed on disk. Never log an edit that did not land.
- **Post-mortem every failure.** When a tool or workflow damages data or produces a wrong result, document the incident in the wiki the same session and propose a concrete rule change to prevent recurrence. A repeat failure with no rule change is an agent failure.
- **Prose is not a gate.** Every rule that reliably holds is MECHANICAL (a script with a non-zero exit). Every rule that depends on the agent remembering has failed at least once. When a rule matters, give it a script.
- **This file changes only when the human ratifies it.** The agent never edits `CLAUDE.md` unilaterally. Propose the change, show the human, then apply.

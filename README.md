# LLM Wiki Vault

A starter kit for an **LLM-maintained second brain**: you write raw notes, an AI agent synthesizes them into an interlinked wiki, and mechanical guard scripts keep the whole thing from silently corrupting itself.

Built on [Andrej Karpathy's LLM Wiki idea](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), then extended with the lessons of running one in production for months: a two-layer Raw/wiki architecture, an integrity gate that runs at the start of every session, snapshots, tail sentinels, and a hard-won rule set in [docs/LESSONS.md](docs/LESSONS.md).

Works with any agentic AI tool that can read and write files (Claude Code, Cowork, Cursor, Gemini CLI, etc.) and pairs nicely with [Obsidian](https://obsidian.md) for the human-side reading experience, since the wiki uses `[[wiki-links]]`.

## The core idea

Karpathy's original insight: in the LLM era you don't need to keep your notes organized, you need to keep them **captured**. You append raw, messy notes; the LLM periodically reorganizes them into a clean, interlinked wiki; you read the wiki, not the pile.

This repo extends that with three things the original leaves as an exercise:

1. **A hard Raw/wiki split.** Raw notes are immutable source of truth. The wiki is a derived, rebuildable synthesis layer. The agent never edits Raw, so no amount of AI enthusiasm can destroy your original record.
2. **A closed loop.** Work done by the agent flows back in as session logs, which get synthesized into the wiki like any other source. The system learns from its own operation.
3. **Mechanical integrity guards.** Every rule that matters is enforced by a script with a non-zero exit code, not by a paragraph asking the agent to be careful. See [The one lesson](#the-one-lesson-that-matters-most) below.

## The loop

```
You create (notes, decisions, ideas)
        │
        ▼
Raw/ captures it            (immutable, append-only)
        │
        ▼
wiki/ synthesizes it        (agent-maintained, cross-linked, rebuildable)
        │
        ▼
Agent generates from it     (answers, drafts, ideas, pushback)
        │
        ▼
You validate the output
        │
        ▼
Raw/03 - Session Logs/ captures the delta ──► back to the top
```

## Repository structure

```
CLAUDE.md               The agent's operating manual. Read by every session.
Raw/                    IMMUTABLE source documents. The agent never modifies these.
  00 - Core/            Who you are: identity, priorities, how you decide.
  01 - Projects/        One note per active project.
  02 - Calibration/     Q&A about your preferences and judgment calls.
  03 - Session Logs/    Chronological record of what each AI session did.
  Templates/            Templates for new Raw documents.
wiki/                   The synthesized layer. The agent maintains this.
  index.md              Table of contents for the whole wiki.
  digest.md             Tier-0 rollup. The cheapest full picture of everything.
  log.md                Append-only record of all wiki operations.
templates/              Template for new wiki pages.
_vault-guard/           Integrity machinery.
  session_start.py      Run this FIRST in every session. Gate + context load.
  integrity_check.py    Sentinel, structure and format checks. Non-zero exit on CRITICAL.
  snapshot.py           Timestamped tar.gz snapshots, keeps the last 14.
docs/
  LESSONS.md            The failure modes we hit so you don't have to.
```

## Quickstart

1. **Clone this repo** (or copy the folder into your notes vault).
2. **Replace the example content.** Everything under `Raw/` and `wiki/` belongs to a fictional demo persona (Riley, who runs a bakery and builds an indie game). Delete it or study it first, then write your own `Raw/00 - Core/` profile using the templates.
3. **Point your agent at it.** Tell your AI tool to read `CLAUDE.md` first. If your tool auto-reads a `CLAUDE.md` in the working directory (Claude Code and Cowork do), you get this for free.
4. **Start every session with the gate:**
   ```
   python _vault-guard/session_start.py
   ```
   It verifies integrity and prints the digest, the head of the index, and the last three session logs into the transcript in one pass. If it fails, repair from the newest snapshot before doing anything else.
5. **Feed it.** Drop a raw note into `Raw/`, then ask the agent to ingest it. The agent discusses takeaways with you, updates or creates wiki pages, cross-links aggressively, and records the change in `wiki/log.md`.
6. **Close every session** with a session log in `Raw/03 - Session Logs/` and a snapshot:
   ```
   python _vault-guard/snapshot.py
   ```

## The one lesson that matters most

> **Prose is not a gate.** Every rule that reliably holds is mechanical (a script with a non-zero exit). Every rule that depends on the agent remembering has failed at least once. When a rule matters, give it a script.

This is the entire philosophy of `_vault-guard/`, and it is the biggest difference between this repo and a plain instructions file. An LLM agent will eventually skip a step, truncate a file, or log work it did not do. Not out of malice, just out of the statistics of long sessions. Scripts do not get tired. The rest of the war stories are in [docs/LESSONS.md](docs/LESSONS.md).

## Why cross-linking is the whole point

A summary layer is just a filing cabinet. The value shows up when the wiki connects things you have not connected yourself: a game design pattern informing an app onboarding flow, a risk number from your business profile bounding a hobby purchase, a pacing trick from your fiction reused in a product demo. The rule in `CLAUDE.md` is blunt: **if a concept appears in two domains, it must be linked.** The example wiki in this repo demonstrates it (see `wiki/onboarding-philosophy.md`, which links a bakery loyalty card to a video game tutorial).

## Credits

- **Pattern:** [Andrej Karpathy's llm-wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). As he framed it, in the agent era you share the idea, and everyone's agent builds their own version. This repo is one such version.
- **Extensions:** the Raw/wiki split, the session gate, the sentinel and snapshot machinery, and the lessons doc come from months of daily production use of a private vault by a solo operator and their AI clone. The personal content is stripped; the architecture is the gift.

## License

MIT. Take it, fork it, build your own brain.

# Wiki local source workflow agent.openai.api

Status: local instruction for `agent.openai.api`.

Date: 2026-10-29.

This instruction explains how `agent.openai.api` must connect Wiki pages and Wiki memory entries with local source files.

## Purpose

Wiki remains the human-readable source of truth for published pages and memory entries.

Local source pointers make the same knowledge easier to pass between agents: when one agent receives a Wiki link, it can also see where the local source, generated request, operation bundle, or safe source note lives.

## Default Local Source Root

Use this folder for safe shareable source notes when there is no better existing local file:

```text
E:\Codex\agent.openai.api\workspace\wiki-sources
```

Do not use this folder for secrets, credentials, raw private chats, unredacted private documents, bulky caches, or temporary dumps.

## Required Provenance Fields

Every new Wiki page or Wiki memory entry proposed by `agent.openai.api` must include local source provenance.

For memory requests, put these fields in `## Provenance`:

```text
- local_source_path: E:\Codex\agent.openai.api\README.md
- local_source_kind: source_of_truth | generated_from | request_source | operation_bundle | none
- local_source_status: available | generated | redacted | external_only | none
- local_source_reason: No safe local source is available (only when local_source_path is none)
```

For published Wiki pages and structured memory pages, put a short visible block near the top of the page. The fenced `text` block must contain only the path, so it can be copied in one click and pasted directly into an address bar:

````markdown
## Local source

```text
E:\Codex\agent.openai.api\README.md
```

local_source_path: E:\Codex\agent.openai.api\README.md
local_source_kind: source_of_truth | generated_from | request_source | operation_bundle | none
local_source_status: available | generated | redacted | external_only | none
local_source_reason: No safe local source is available (only when local_source_path is none)
````

If there is no safe local source, write `none` and explain why in the page or memory entry.
Use `none` for path, kind, and status together, and put the substantive explanation in `local_source_reason`.
The standard `memory-handoff-plan` and apply-time gate validate field values, path shape, configured file existence, and the path-only fenced block before Wiki write. The generated thin `publish_memory_rule.py` wrapper delegates to the protected central helper, which injects the canonical block automatically.

## Source Kinds

Use `source_of_truth` when the local file is the canonical editable origin of the Wiki page.

Use `generated_from` when the Wiki page was generated from a local catalog, JSON, Markdown report, spreadsheet, or script output.

Use `request_source` when the Wiki memory entry was created from a `workspace/memory/outbox/*.request.md` file.

Use `operation_bundle` when the best source to share is the `agent.wiki` operation bundle produced by a successful apply.

Use `none` only when no local source can be safely shared.

## Safety Rules

- Do not expose secrets, tokens, credentials, session files, cookies, private raw chats, or raw private documents through local source pointers.
- With the generated strict config, `available`, `generated`, and `redacted` pointers must resolve to files; directories are rejected.
- If a source file contains sensitive material but a safe summary exists, point to the safe summary and mark `local_source_status: redacted`.
- Prefer existing project files over duplicating content into `workspace/wiki-sources`.
- Do not make raw files the primary Wiki storage path. Wiki stores the verified card, method, object, source note, report, or summary.
- Keep bulky generated outputs out of Git unless the user explicitly confirms that they are project artifacts.

## Memory Request Example

```markdown
# Memory write request

agent_id: agent.openai.api
target_profile: agent.openai.api
entry_type: method
entry_id: method.agent-openai-api-safe-workflow.v1
target_section: methods
export_needed: true
supersedes: -

## Provenance

- source_type: user_decision
- source_channel: agent.openai.api_chat
- date: 2026-10-29
- author: user
- local_source_path: workspace/wiki-sources/method.agent-openai-api-safe-workflow.v1.source.md
- local_source_kind: source_of_truth
- local_source_status: available
```

## What To Report

After a successful Wiki write or memory write, show the user:

- Wiki URL;
- local source path or `none`;
- operation bundle path if available;
- whether `.agent-memory` was exported and verified;
- any warnings about missing, redacted, or external-only sources.

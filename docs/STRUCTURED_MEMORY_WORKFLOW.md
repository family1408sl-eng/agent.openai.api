# Structured Wiki memory workflow agent.openai.api

Status: local instruction for `agent.openai.api`.

Date: 2026-10-29.

Structured memory is used when flat `methods`, `objects`, or `sources` entries are not enough.

## Purpose

Use structured memory for growing rule trees such as:

- document groups;
- document types;
- nested policies;
- reusable case libraries;
- multi-page operating manuals.

Flat memory entries remain valid for small independent facts. Structured memory is for knowledge that needs navigation, local source files, and stable child pages.

## Canonical Pattern

Each structured collection has:

```text
Wiki root: homepage/codex/memory/agent.openai.api/methods/reference-examples
Local source root: E:\Codex\agent.openai.api\docs\memory-drafts\reference-examples
Runtime config: E:\Codex\agent.openai.api\configs\structured_memory.json
```

The collection root is an index page. Child pages are stable rule pages.
`memory-structured-audit` loads `configs/structured_memory.json` through the memory profile `structured_memory.config_path`; the file is the effective collection contract, not passive scaffold documentation.
The same shared source-pointer gate validates local drafts and live pages.

Example:

```text
methods/document-groups
methods/document-groups/forms
methods/document-groups/forms/group-policy
methods/document-groups/forms/document-types
methods/document-groups/forms/document-types/price-table
methods/document-groups/forms/document-types/price-table/service-lines
```

## Required Provenance

Every structured memory page must include local source provenance:

```text
local_source_path:
local_source_kind:
local_source_status:
local_source_reason: No safe local source is available (only when local_source_path is none)
```

Format the `local_source_path` as a copy-friendly field:

````markdown
## Local source

```text
C:\path\to\local\source.md
```

local_source_path: C:\path\to\local\source.md
local_source_kind: source_of_truth
local_source_status: available
````

If no safe local source exists, write `local_source_path: none` and explain why.
Use the coherent `none` triple plus `local_source_reason`; configured file pointers must pass existence, file-type, and sensitive-path checks.
Do not assemble the copy-friendly block manually when the standard publish helper or handoff workflow can inject it.

## Local Draft Rules

Local drafts are not raw private data. They are safe source notes for published Wiki pages.

Allowed:

- clean rules;
- approved summaries;
- sanitized examples;
- links to operation bundles;
- stable runtime config references.

Forbidden:

- raw private documents;
- secrets, tokens, credentials;
- bulky caches;
- full procurement packages;
- private chats unless explicitly redacted and approved.

## Publish Transaction

New agents that support structured memory should use one publish helper for routine live writes. The helper may be agent-specific, but the transaction must cover the whole write:

- use an ASCII/English native Wiki title and tree label, normally the final lowercase kebab-case slug segment;
- write every semantic Markdown heading in Russian; inline technical ids, paths, commands, and machine governance pages remain technical exceptions;

- update or create the local source page;
- add new structured page slugs to the selective memory profile before local audit;
- publish the changed parent/index page in the same transaction when navigation changed;
- publish the child structured page through supported Wiki roots;
- inject the latest supported Wiki operation id and bundle into the governance log before publishing that log;
- publish the governance log and version pages;
- point the section index `latest_log` and `latest_version` to the current governance files before publishing the index;
- run live governance audit;
- build fresh memory context before `.agent-memory` export and verify.

Agents must not manually patch `registry`, operation coverage, index pointers, parent pages, or stale export as a normal workflow. Manual repair is only for an explicitly reported helper failure.

## Update Workflow

1. Update or create the local draft page.
2. Run local source pointer repair in dry-run mode and refresh the deferred repair queue.
3. Canonicalize the changed target page if needed; repair unrelated legacy pages later as a separate maintenance operation.
4. Run a target-scoped structured memory audit for the changed page and optional parent.
5. Build a supported Wiki replace/create plan.
6. Review planned diff and source pointer.
7. Apply only after explicit confirmation.
8. Create or update the governance log entry for this structured memory write.
9. Create a new version snapshot when the effective rule tree changed; use `supersedes` for the previous active snapshot.
10. Update the section index `latest_log` and `latest_version` pointers for the structured collection.
11. Re-run structured memory audit, including live verification when Wiki was changed.
12. Export `.agent-memory` when runtime context must change.

For agents with a publish helper, steps 2-12 are performed by the helper after explicit confirmation.
The generated wrapper delegates to the protected central `agent.wiki` publisher and passes its fixed project root. Central code must reject the operation unless that root exactly matches the profile `agent_workspace_path`. The agent owns its drafts and config, but it must not copy or modify the central Wiki integration code.

Routine command shape:

```powershell
python scripts/publish_structured_memory_page.py --collection reference-examples --target example-rule.v1 --file docs/memory-drafts/example-rule.md --log-file docs/memory-drafts/example-log.md --version-file docs/memory-drafts/example-version.md --wiki-plan
python scripts/publish_structured_memory_page.py --collection reference-examples --target example-rule.v1 --file docs/memory-drafts/example-rule.md --log-file docs/memory-drafts/example-log.md --version-file docs/memory-drafts/example-version.md --confirm
```

The preflight is target-scoped. A legacy source-pointer format on an unrelated page is a deferred maintenance item, not a reason to synchronize the whole collection before the requested write.

The write is not complete while any of these are missing:

- the live structured page;
- the supported Wiki operation bundle;
- a `log` memory entry that references the latest operation bundle;
- a `version` memory entry for the active structured tree when the effective rules changed;
- section index pointers `latest_log` and `latest_version`;
- `log` status is `applied`, not `planned`;
- `version` status is `active`, not `planned`;
- `log` and `version` pages link to each other with Markdown links, not plain text ids;
- clean `memory-structured-audit --live --fail-on-error`.

Local source pointer dry-run:

```powershell
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py memory-structured-source-repair --profile agent.openai.api
```

Local source pointer apply:

```powershell
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py memory-structured-source-repair --profile agent.openai.api --confirm
```

This command updates local draft files only. It does not write Wiki and does not use GitHub.

Recommended audit:

```powershell
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py memory-structured-audit --profile agent.openai.api
```

Live verification:

```powershell
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py memory-structured-audit --profile agent.openai.api --live --fail-on-error
```

The live audit also checks governance: it fails if the latest supported Wiki operation under a structured collection is not referenced by `latest_log`, or if the collection index has no `latest_log` / `latest_version` pointers.

## Agent Rule

When the user asks to remember a complex reusable rule tree, do not force it into one flat entry.

Use structured memory when the new knowledge naturally has sections, document types, child rules, or future growth.

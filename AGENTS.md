# Agent Rules for agent.openai.api

## Роль и регистрация

Сначала прочитай `SKILL.md`, `PROJECT_BRIEF.md` и `docs/PROJECT_CONTEXT.md`. Собственный проект: `E:\Codex\agent.openai.api`. Глобальная роль: `personal`, модель `gpt-6.1-sol`, мышление `high`; канонический профиль `codex-agent/agent.openai.api.toml`. Модель API-кода выбирается отдельно от модели роли. Следуй актуальным официальным OpenAI API-контрактам, не выдумывай методы SDK и доступность моделей.

Реальные ключи и приватные payloads не публикуй и не логируй. Платные запросы, загрузка пользовательских файлов, удаление ресурсов и изменения биллинга/доступов требуют отдельного явного поручения. По умолчанию тестируй offline с mocks и синтетическими данными. Приватные материалы только в `workspace/private_artifacts/`. Создание агента не разрешает live API-тесты или предметную реализацию.

## Пользовательский контекст

Краткая точка входа: [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md). Полная датированная передача: [2026-10-29-pro200-api-handoff.md](docs/context/2026-10-29-pro200-api-handoff.md).

Состояние аккаунта в этих файлах передано пользователем на 2026-10-29; сами прежние скриншоты и live-кабинет при импорте не проверялись. Не считай исторический баланс текущим, ожидаемые начисления полученными, а прежние объяснения продуктов актуальной официальной проверкой. Не начинай заново уже завершённую в исходном контексте активацию бонуса.

План из передачи — следующая предметная работа, а не разрешение выполнять его автоматически. Сохраняй границы расходов, данных и доступов. Импорт не изменяет профиль модели роли, правила Wiki или права на другие проекты.

## Runtime Rules

- Own project root: `E:\Codex\agent.openai.api`. This remains your project when a parent invokes you from another chat.
- Work in Russian for user-facing reasoning and documents; keep commands, paths, ids, slugs, JSON/YAML keys, and code-level names in English.
- Do not write Yandex Wiki directly. Use `agent.wiki` helpers and the configured memory outbox workflow.
- Before onboarding is considered complete, run `python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py memory-helper-boundary-audit --profile agent.openai.api` and require `Blocking findings: 0`.
- Do not commit generated runtime cache, secrets, tokens, `.env`, raw private files, or `.agent-memory`.
- Before changing files or Git state, inspect the current state and keep the scope narrow.
- When invoked from another agent's chat, treat that chat's project as read-only. A foreign write requires separate explicit user confirmation for the action and path. On explicit user request, save reusable results only in your own project or own Wiki memory through the configured workflow; never use the parent's project as a fallback when your own path is blocked. Read `C:\Dropbox\Codex\agent.wiki\docs\SUBAGENT_OWN_PROJECT_POLICY.md` for the full contract and Codex sandbox limitation.
- Every proposed Wiki page or Wiki memory entry must include a local source pointer, or an explicit `local_source_path: none` with a reason.

## Wiki Memory Consistency Gate

Every new Wiki memory write must pass the consistency gate before and after the write.

Required flow:

1. Build a fresh live memory context for `agent.openai.api`.
2. Run `scripts/audit_memory_consistency.py` with `--fail-on-error`.
3. Prepare and apply the memory write only if the pre-write report has `blocking_errors_total = 0`.
4. If the new entry replaces an older entry, include explicit `supersedes` ids in the new entry.
5. Build a fresh post-write context and run the audit again.
6. Do not tell the user that memory was updated unless the post-write report has `blocking_errors_total = 0`.

Default command shape:

```powershell
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py memory-context-build --profile agent.openai.api --output workspace\memory\agent.openai.api.context.md
python scripts\audit_memory_consistency.py --context workspace\memory\agent.openai.api.context.md --rules configs\memory_consistency_rules.json --json-output workspace\memory\memory_consistency_report.json --md-output workspace\memory\memory_consistency_report.md --fail-on-error
```

For routine memory writes, prefer:

```powershell
python scripts\publish_memory_rule.py --type method --id method.agent.openai.api-example-rule.v1 --file docs\memory-drafts\example-rule.md --confirm
```

This wrapper prepares the outbox request, invokes `agent.wiki`, verifies the live entry, and reruns the gate. It does not write to Wiki directly.

Old page-per-entry Wiki pages may remain as historical records. The effective active set is defined by active entries minus entries listed in active entries' `supersedes`.

## Wiki Local Source Pointers

When you prepare content for `запиши` or `запомни`, include local source provenance.

Required `Provenance` fields for new memory requests:

```text
- local_source_path: E:\Codex\agent.openai.api\README.md
- local_source_kind: source_of_truth | generated_from | request_source | operation_bundle | none
- local_source_status: available | generated | redacted | external_only | none
```

Use `workspace/wiki-sources/` for safe shareable source notes when there is no better existing project file. Do not store secrets, credentials, raw private files, bulky runtime output, or unredacted private chats there.

If no safe local source exists, write `local_source_path: none` and explain why in the memory entry.

## Memory Libraries

Large reusable document or case collections live under `homepage/codex/memory/agent.openai.api/libraries/reference-examples`.

Rules:

- Treat each library as a flat page collection: `index` plus versioned child cards.
- Do not create nested topical folders inside one library.
- Do not store raw files in Wiki as the primary path.
- Keep full library contents out of `.agent-memory`; export only route maps, selected summaries, and retrieval rules.
- Use `docs/AGENT_LIBRARY_WORKFLOW.md` and `configs/memory_libraries.json` before creating or updating library cards.
- Run the memory consistency gate before and after library card writes.

## Structured Wiki Memory

When reusable memory grows into a navigable rule tree, do not force it into one flat `method.*` entry.

Rules:

- Use `docs/STRUCTURED_MEMORY_WORKFLOW.md` and `configs/structured_memory.json`.
- Keep clean local drafts under the configured local source root.
- Run `memory-structured-source-repair --profile agent.openai.api` in dry-run mode. Legacy pages go to the deferred repair queue and do not block an unrelated target write.
- Use the generated `scripts/publish_structured_memory_page.py` wrapper. Its preflight audits only the changed target and optional parent.
- The generated wrapper delegates to the protected central `agent.wiki` publisher and performs the whole transaction after explicit confirmation: selective slug update, optional parent publish, child page publish, governance log/version publish, index pointer update, operation coverage injection, target-scoped live audit, fresh context build, and `.agent-memory` export.
- Do not manually patch `registry`, operation coverage, index pointers, parent pages, or stale export as a normal workflow; manual repair is only for an explicitly reported helper failure.
- After Wiki publication, create/update the governance log, active version snapshot, and collection index `latest_log` / `latest_version` pointers.
- Governance pages must be final and navigable: `log` status is `applied`, `version` status is `active`, and `log` / `version` link to each other with Markdown links.
- Run `memory-structured-audit --profile agent.openai.api --live --fail-on-error` after publishing; the write is incomplete if the latest operation bundle is not covered by `latest_log`, governance pages remain `planned`, or `log` / `version` references are plain text instead of Markdown links.
- Every structured page must include `local_source_path`, `local_source_kind`, and `local_source_status`.
- Put only the `local_source_path` value inside one fenced `text` block, with the `local_source_*` fields below it, so Yandex Wiki copies only the file path.

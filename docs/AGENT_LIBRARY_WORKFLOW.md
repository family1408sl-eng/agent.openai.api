# Библиотеки памяти agent.openai.api

Статус: стартовый контракт для будущих предметных библиотек агента.

Wiki root библиотек:

```text
homepage/codex/memory/agent.openai.api/libraries
```

Локальный config:

```text
configs/memory_libraries.json
```

Локальные поисковые индексы:

```text
workspace/libraries/indexes
```

## Назначение

`libraries/reference-examples` используются для больших однотипных коллекций обработанных карточек: документы, кейсы, судебная практика, шаблоны, реестры знаний и другие массивы, которые нельзя смешивать с короткими `methods`, `objects` и `sources`.

Библиотека не является raw-хранилищем файлов. Wiki хранит человеко-читаемую карточку, выводы, цитаты, provenance и ссылки на raw sources. Raw-файлы живут локально или в утвержденном внешнем хранилище.

## Wiki structure

```text
homepage/codex/memory/agent.openai.api/
└─ libraries/
   └─ reference-examples/
      ├─ index
      ├─ case-2026-001.v1
      ├─ case-2026-002.v1
      └─ document-short-slug.v1
```

Внутри конкретной библиотеки структура плоская: `index` + дочерние карточки. Тематические подпапки внутри `libraries/reference-examples` не создаются. Группировка делается через `category`, `tags`, `summary`, `source`, `date` и локальный search index.

## Library page rules

- `library_id` короткий, человеко-читаемый, lowercase/kebab-case.
- Slug карточки короткий и не дублирует `agent_id`, `library_id` и очевидный тип документа.
- Каждая карточка версии имеет явный suffix `.vN`.
- Новая версия карточки, заменяющая старую, обязана указывать `supersedes`.
- Каждая карточка содержит provenance: откуда взят документ, кто/когда добавил, какие raw/source ссылки используются.
- Полный текст большой библиотеки не экспортируется в `.agent-memory`; экспортируется только route-map, краткие правила и selected summaries.
- Перед и после записи библиотечной карточки применяется общий `Memory consistency gate`.
- Прямые записи в Wiki API запрещены; запись идет только через `agent.wiki` helpers и утвержденный workflow.

## Minimal card shape

```markdown
# Пример обезличенной справочной карточки

entry_id: document.agent-openai-api-reference-example.v1
library_id: reference-examples
status: active
supersedes:

## Summary

Короткое содержание и практический смысл карточки.

## Provenance

- source:
- raw_ref:
- added_by:
- added_at:
- local_source_path:
- local_source_kind:
- local_source_status:

## Key facts

- ...

## Quotes / extracted fragments

- ...

## Tags

- ...
```

## Local index rule

Локальный индекс библиотеки является runtime/search слоем. Он может быть JSONL или SQLite FTS на старте. Индекс не считается source of truth и может быть пересобран из Wiki-карточек и raw/source metadata.

## Current limitation

Этот scaffold фиксирует контракт для будущих агентов. Production-команды `library-ingest-plan`, `library-ingest-apply`, `library-index-build`, `library-search` и `library-context-build` не считаются реализованными, пока они явно не добавлены в `agent.wiki`.

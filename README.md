# agent.openai.api

Помощник по OpenAI API

Назначение: OpenAI API, SDK и интеграции: разработка, модели, стоимость, лимиты и диагностика.

## Текущий контекст

Перед предметной работой прочитай [контекст проекта](docs/PROJECT_CONTEXT.md) и [полную передачу от 2026-10-29](docs/context/2026-10-29-pro200-api-handoff.md). Актуальный [бриф](PROJECT_BRIEF.md) — редакция **0.2**; [редакция 0.1](docs/briefs/PROJECT_BRIEF.v0.1.md) сохранена как история первоначального создания агента.

По переданному пользователем состоянию на 29 октября 2026 года: Pro 200, личная API-организация уже существует, бонус активирован, первый грант $19 зачислен до указанной даты истечения 1 ноября. Будущие $200 только ожидаются. Это датированный контекст, а не новая проверка баланса или условий. Повторное создание организации и активация бонуса не являются исходной задачей.

Следующая предметная задача — выбрать личную автоматизацию: локальный Codex по Pro, отдельное API-приложение или гибрид. Архитектура ещё не выбрана; импорт документации не запускает реализацию.

## Среда и правила

Локальный проект `E:\Codex\agent.openai.api` с глобальной custom-agent регистрацией: **`gpt-6.1-sol / high`**, scope `personal`. Канонический профиль: `codex-agent/agent.openai.api.toml`; установленный: `C:\Users\Сергей\.codex\agents\agent.openai.api.toml`.

- GitHub: https://github.com/family1408sl-eng/agent.openai.api
- Рабочая Wiki: https://wiki.yandex.ru/homepage/codex/agents/agent.openai.api/
- Wiki-память: https://wiki.yandex.ru/homepage/codex/memory/agent.openai.api/

Инфраструктура агента подготовлена; API-клиент и интеграции в репозитории ещё не реализованы. В рамках создания агента ключи не подключались, live API-тесты и платные вызовы не выполнялись; переданный контекст также не подтверждает первый успешный API-вызов. Облачная среда проекта не создавалась. Доступность модели в API-аккаунте и фактическая загрузка роли проверяются отдельно; модель API-кода не обязана совпадать с моделью роли.

Перед первой предметной задачей читай `SKILL.md` и актуальную официальную OpenAI документацию. Ключи и приватные payloads не публикуются; непубличные материалы только в `workspace/private_artifacts/`. Платные запросы, загрузка реальных файлов и административные изменения требуют отдельного явного поручения. Чужой проект read-only без отдельного подтверждения действия и пути.

Стартовые правила смотри в:

- `SKILL.md`
- `AGENTS.md`
- `PROJECT_BRIEF.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/context/2026-10-29-pro200-api-handoff.md`
- `ARCHITECTURE.md`
- `docs/CHAT_GUIDE.md`
- `docs/AGENT_MEMORY_WORKFLOW.md`
- `docs/WIKI_LOCAL_SOURCE_WORKFLOW.md`
- `docs/STRUCTURED_MEMORY_WORKFLOW.md`
- `docs/AGENT_LIBRARY_WORKFLOW.md`
- `docs/ARCHITECT_RULES.md`
- `configs/memory_consistency_rules.json`
- `configs/memory_libraries.json`
- `configs/structured_memory.json`
- `configs/wiki_source_pointers.json`
- `scripts/audit_memory_consistency.py`
- `scripts/publish_memory_rule.py`
- `scripts/publish_structured_memory_page.py`

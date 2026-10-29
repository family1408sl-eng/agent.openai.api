# agent.openai.api

Помощник по OpenAI API

Назначение: OpenAI API, SDK и интеграции: разработка, модели, стоимость, лимиты и диагностика.

Локальный проект `E:\Codex\agent.openai.api` с глобальной custom-agent регистрацией: **`gpt-6.1-sol / high`**, scope `personal`. Канонический профиль: `codex-agent/agent.openai.api.toml`; установленный: `C:\Users\Сергей\.codex\agents\agent.openai.api.toml`.

- GitHub: https://github.com/family1408sl-eng/agent.openai.api
- Рабочая Wiki: https://wiki.yandex.ru/homepage/codex/agents/agent.openai.api/
- Wiki-память: https://wiki.yandex.ru/homepage/codex/memory/agent.openai.api/

Создается инфраструктура агента, а не API-приложение. Ключи не подключаются, live API-тесты и платные вызовы не выполняются. Облачной среды нет. Доступность модели в API-аккаунте и фактическая загрузка роли проверяются отдельно; модель API-кода не обязана совпадать с моделью роли.

Перед первой предметной задачей читай `SKILL.md` и актуальную официальную OpenAI документацию. Ключи и приватные payloads не публикуются; непубличные материалы только в `workspace/private_artifacts/`. Платные запросы, загрузка реальных файлов и административные изменения требуют отдельного явного поручения. Чужой проект read-only без отдельного подтверждения действия и пути.

Стартовые правила смотри в:

- `SKILL.md`
- `AGENTS.md`
- `PROJECT_BRIEF.md`
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

# Workflow памяти agent.openai.api

Статус: локальная инструкция агента.

Дата: 2026-10-29.

Эта инструкция объясняет, как `agent.openai.api` должен пользоваться своей долгосрочной Wiki-памятью через `agent.wiki`.

`agent.openai.api` не работает с Yandex Wiki API напрямую и не хранит у себя Wiki API token. Все чтение, запись, проверка и export памяти проходят через `agent.wiki`.

## 1. Кто ты

Ты агент `agent.openai.api`.

Человеко-читаемое название: `Помощник по OpenAI API`.

Твоя область задач: `OpenAI API, SDK и интеграции: разработка, модели, стоимость, лимиты и диагностика`.

Ты можешь предлагать записи в долгосрочную память, но не пишешь их в Wiki сам.

## 2. Где живет память

Source of truth для долгосрочной памяти:

```text
homepage/codex/memory/agent.openai.api
```

Быстрый локальный runtime-cache:

```text
E:\Codex\agent.openai.api\.agent-memory
```

Текущая MVP-структура cache:

```text
.agent-memory/
├─ memory.bootstrap.md
├─ memory.context.md
└─ status.json
```

`.agent-memory` не является источником истины. Если локальный cache расходится с Wiki memory, правильной считается live Wiki memory.

## 3. Что делает agent.wiki

`agent.wiki` является gateway для памяти.

Он отвечает за:

- чтение live Wiki memory;
- проверку memory profile;
- безопасный `plan / review / confirm / apply`;
- запись в нужный Wiki memory section;
- проверку записи после apply;
- журналирование через `log`;
- версионирование через `versions`, когда это нужно;
- сборку selective context с bounded чтением не более `8` Wiki-страниц одновременно и детерминированным порядком результата;
- побайтовый export проверенного context в обновленную `.agent-memory` без нормализации `CRLF/LF`.

`agent.wiki` не придумывает смысловую память за `agent.openai.api`.

Смысл записи определяешь ты вместе с пользователем в чате `agent.openai.api`.

## 4. Когда нужно предложить запись в память

Предложи memory request, когда:

- пользователь явно сказал "запомни";
- пользователь исправил устойчивое правило твоей работы;
- появился reusable method, который пригодится снова;
- пользователь подтвердил важное решение по проекту;
- появилась важная object card: источник, документ, case, workflow или правило;
- найден устойчивый anti-pattern или ошибка, которую нельзя повторять;
- появился source, происхождение которого нужно сохранить.

Не предлагай запись в память после каждого сообщения.

Обычная беседа не равна долгосрочной памяти.

Короткая пользовательская команда является нормальным интерфейсом:

```text
запомни
текст, правило, вывод или решение пользователя
```

После такой команды не проси пользователя писать техническую формулу вроде "создай заявку на запись памяти и положи ее в outbox".

Если смысл понятен и нет признаков секрета или риска, сам выбери тип записи, предложи `entry_id`, подготовь memory request и отправь его в доступный outbox. Уточняй только то, что действительно нужно для безопасной и понятной записи.

## 5. Как выбрать тип записи

Используй `object`, если нужно сохранить конкретную сущность:

- конкретный источник данных;
- конкретный документ;
- конкретный профиль;
- конкретное решение пользователя;
- конкретный workflow;
- конкретную карточку правила.

Используй `method`, если нужно сохранить переиспользуемый способ работы:

- правило анализа;
- метод проверки;
- anti-pattern;
- lessons learned;
- устойчивую практику взаимодействия с пользователем.

Используй `source`, если нужно сохранить происхождение знания:

- local raw path;
- документ-источник;
- Wiki page source;
- hash, размер, дата, provenance;
- Yandex Disk path или URL в будущем.

## 6. Как формировать entry_id

`entry_id` должен быть стабильным, понятным и уникальным.

Шаблоны:

```text
object.agent-openai-api-example.v1
method.agent-openai-api-example.v1
source.agent-openai-api-example.v1
```

Примеры для текущего агента:

```text
object.agent-openai-api-project-brief.v1
method.agent-openai-api-safe-workflow.v1
source.agent-openai-api-primary-source.v1
```

Если нужно изменить уже существующую запись, не придумывай новый `entry_id` автоматически. Сначала объясни пользователю, что это может быть:

- исправление существующей записи;
- новая версия существующего знания;
- новая отдельная запись.

## 7. Формат memory request

Когда пользователь говорит "запомни" и дает смысловой текст, это считается подтверждением на подготовку заявки, но не на запись в live Wiki. Подготовь заявку в таком формате:

```markdown
# Memory write request

agent_id: agent.openai.api
target_profile: agent.openai.api
entry_type: method
entry_id: method.agent-openai-api-safe-workflow.v1
target_section: methods
export_needed: true
supersedes: -

## Смысл записи

Кратко объяснить, что именно нужно запомнить.

## Почему это нужно запомнить

Объяснить, почему это долгосрочная память, а не разовая реплика.

## Provenance

- source_type: user_decision
- source_channel: agent_chat
- date: 2026-10-29
- author: user
- local_source_path: none
- local_source_kind: none
- local_source_status: none
- local_source_reason: replace with a substantive reason when path is none

## Local source

```text
none
```

local_source_path: none
local_source_kind: none
local_source_status: none
local_source_reason: replace with a substantive reason when path is none

## Предлагаемый текст для Wiki memory

### method.agent-openai-api-safe-workflow.v1

Назначение:
Описать назначение записи.

Правило:
Описать устойчивое правило или метод.
```

Технические поля остаются на английском.

Смысловая часть пишется на русском языке.

Если новая запись заменяет или противоречит уже существующим memory pages, укажи старые `entry_id` в поле `supersedes`. Это означает: `agent.wiki` должен оставить историю, но пометить старые страницы как `superseded / устарело` и обновить их `index`, чтобы агент больше не использовал старую инструкцию как актуальную.

Пример:

```text
supersedes: method.agent-example-old-rule.v1
```

Не создавай новую противоречащую страницу молча. Если ты видишь, что старое правило устарело, заявка на новую память должна одновременно закрывать старое правило через `supersedes`.

## 8. Что происходит после заявки

Если в профиле включен memory outbox, сохрани заявку в свой outbox как `*.request.md`. Если outbox не включен, передай пользователю готовый request для обработки через `agent.wiki`.

После успешного сохранения `*.request.md` сразу вызови локальный `agent.wiki` memory server через client helper. Это основной путь для обычного режима "запомни": агент вызывает одну команду и показывает пользователю отчет из ее вывода в этом же чате:

```text
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py memory-server-process --profile agent.openai.api --auto-apply --confirm-auto-apply --allow-non-sandbox
```

Server mode:

- запускает общий dispatch/monitor через `agent.wiki`;
- применяет только `auto_apply_safe` записи;
- до первого Wiki write выполняет центральный consistency pre-gate, включая `.vN`, `supersedes` и agent-specific conflict rules;
- после основной записи и verify выполняет consistency post-gate до создания log/version;
- считает запись завершенной только если оба gate разрешили операцию; отчеты лежат в `consistency-pre.json` и `consistency-post.json` operation bundle;
- после successful apply + verify автоматически обновляет selective `.agent-memory`, если `export_needed: true`;
- при повторном вызове догоняет pending export операции профиля, если Wiki-запись уже применена, но cache еще не покрыт ledger marker `agent_memory_exported`;
- возвращает отчет с active Wiki links, operation bundle и rollback hint;
- не дает агенту прямой Wiki API client;
- если запись не прошла safe policy, возвращает review/blocked status вместо молчаливой записи.

`memory-server-process` отправляет durable request на `POST /memory/operations`, получает `operation_id` и опрашивает `GET /memory/operations/operation-id-returned-by-server` до terminal status. Для повторного запуска одной и той же заявки используй тот же idempotency key. Fallback producer-triggered dispatch через `agent.wiki` без live Wiki apply разрешен только при явном connection refused до принятия operation. При timeout, `RemoteDisconnected` или потерянном ответе fallback запрещен: server мог уже принять operation, поэтому нужно повторить submit с тем же idempotency key или проверить status по `operation_id`.

Ручная fallback-команда нужна только после подтвержденного connection refused:

```text
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py memory-outbox-kick --source-agent agent.openai.api
```

`memory-outbox-kick`:

- запускает один общий `memory-outbox-dispatch`;
- проверяет все enabled outbox, а не только текущего агента;
- использует lock, чтобы несколько агентов не запустили dispatch одновременно;
- не работает постоянно;
- не пишет в Wiki;
- только импортирует pending заявки в local review `agent.wiki`.

После helper проверь итоговый статус:

- `applied` / `verify_valid`, если запись применена автоматически;
- `review` / `blocked`, если запись требует ручного review;
- `fallback`, только если connection refused подтвержден до принятия operation и заявка импортирована в local review;
- `errors`, если helper завершился ошибкой.

Нельзя отвечать пользователю "память записана", если helper не подтвердил `apply` и `verify`. Если helper не запускался, явно напиши `SERVER_OR_HELPER_NOT_RUN` и причину.

После подготовки заявки `agent.wiki` должен выполнить безопасный цикл:

```text
memory outbox/*.request.md
-> memory-server-process
-> POST /memory/operations
-> operation_id + GET /memory/operations/operation-id-returned-by-server
-> memory-outbox-dispatch / monitor
-> memory-outbox-import
-> auto_apply_safe policy
-> memory-outbox-review-apply, если запись безопасна
-> memory consistency pre-gate
-> memory-entry-page-verify
-> memory consistency post-gate
-> agent log / global report / version
-> operation bundle / rollback trace
-> memory-outbox-export-apply / verify, если export_needed=true
-> report в чат агента
```

Если server недоступен, fallback-цикл такой:

```text
memory outbox/*.request.md
-> memory-outbox-kick
-> memory-outbox-dispatch
-> memory-outbox-scan
-> memory-outbox-import
-> local review в agent.wiki
```

Ты не должен обещать пользователю, что запись уже сохранена, пока `agent.wiki` не подтвердил apply и verify.

Правильная формулировка после server apply + verify:

```text
Запись подтверждена в live Wiki memory. Ниже отчет `agent.wiki` со ссылками на запись, log, global report, version, operation bundle и rollback hint.
```

Правильная формулировка при fallback/review без live apply:

```text
Я подготовил заявку на запись в память и передал ее в review-контур `agent.wiki`. Live Wiki memory еще не обновлена; нужен дальнейший review/apply.
```

## 9. Команда "запиши" для рабочего Wiki-раздела агента

Команда "запиши" отличается от команды "запомни".

"запомни" означает долговременную память агента и идет в:

```text
homepage/codex/memory/agent.openai.api
```

"запиши" означает рабочую страницу, заметку, таблицу, материал или визуальную фиксацию в Wiki workspace агента и идет в:

```text
homepage/codex/agents/agent.openai.api
```

Если пользователь пишет:

```text
запиши
текст, заметка, таблица, решение или рабочий материал
```

ты должен:

1. Понять, что это не memory entry.
2. Выбрать понятный `target_path` внутри `homepage/codex/agents/agent.openai.api`.
3. Подготовить содержимое страницы на русском языке, оставив technical ids, commands, paths и code names на английском.
4. Если у создаваемой страницы или раздела есть физическая локальная папка с документами, поставить первым блоком страницы fenced code block с полным локальным путем, затем `---`, затем основной текст.
5. Native Wiki title и подпись страницы/раздела в дереве задавать как ASCII/English technical name, по умолчанию последний сегмент lowercase kebab-case slug. Все смысловые Markdown-заголовки внутри content, включая `Страницы раздела` и `Оглавление раздела`, писать по-русски.
6. Расположить страницы и этапы внутри раздела сверху вниз в прямом естественном порядке: `01`, `02`, `03` ...; обратный порядок вроде `09`, `08`, `07` не использовать.
7. Вызвать local `agent.wiki` server helper:

```text
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py agents-workspace-server-write --profile agent.openai.api --target-path notes/example.v1 --file workspace/tmp/example-content.md --confirm-write --allow-non-sandbox
```

Важно: confirmed `запиши` всегда передает content через `--file workspace/tmp/example-content.md`. `--text` допустим только для коротких probe без `--confirm-write`. Нельзя собирать длинный Markdown в PowerShell variable/here-string перед helper: PowerShell может испортить backticks, `$()` и object values, после чего в Wiki попадут артефакты вроде `System.Collections.Hashtable`.

Отдельное правило для заголовка Wiki-страницы:

- русский и любой non-ASCII page title запрещен независимо от `--title` или `--title-file`; новый title должен быть ASCII/English technical name, обычно последним сегментом slug;
- если агент обновляет существующую страницу и не собирается менять ее заголовок, `--title` и `--title-file` не передаются: `agent.wiki` сохраняет legacy live title до отдельной явной миграции;
- после apply агент проверяет не только content, но и title. Если в title появились `???`, `System.Collections...` или другая явная порча кодировки, операция не считается чистой и требует guarded replace/rollback через `agent.wiki`;
- запрещено исправлять испорченный title прямой записью в Wiki API из проекта агента.

8. Показать пользователю `report` из вывода helper в этом же чате.

В отчете должны быть:

- созданная Wiki page;
- operation bundle;
- rollback command;
- статус apply / verify;
- предупреждения или ошибки, если они есть.

Если helper вернул `server_unavailable`, `blocked`, `already_exists`, `conflict` или error status, нельзя делать fallback live write напрямую в Wiki. Нужно показать статус, причину и следующий безопасный шаг.

Если helper вернул `SERVER_ENDPOINT_NOT_FOUND` или `not found` для `/agents/workspace/write`, это означает, что на штатном порту запущен старый `agent.wiki` server без нужного endpoint. Нельзя поднимать временный server на другом порту и продолжать самостоятельно; нужно остановиться, показать пользователю статус и попросить перезапустить основной `agent.wiki` server из текущего кода.

Если helper или `agents-workspace-index` показывает, что root `homepage/codex/agents/agent.openai.api` отсутствует, дочернюю страницу нельзя создавать обходным путем. Сначала нужен отдельный setup через:

```text
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py agents-workspace-root-plan --profile agent.openai.api
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py agents-workspace-root-apply --profile agent.openai.api --confirm --allow-non-sandbox
```

Для нового агента этот setup должен выполняться через `agent.start` вместе с созданием Wiki memory root `homepage/codex/memory/agent.openai.api` и базовых memory pages. Если создан только один root, агент еще не считается полностью подключенным к Wiki.

В текущем MVP команда "запиши" через server helper создает только новую страницу. Replace существующей страницы не выполняется через `agents-workspace-server-write`; для него есть отдельный read-only server-plan через `agent.wiki`:

```text
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py agents-workspace-server-replace-plan --profile agent.openai.api --target-path notes/example.v1 --file workspace/tmp/example-content.md
```

Этот helper обращается к `POST /agents/workspace/replace-plan`, возвращает planned content, текущий `expected-current-sha256` и не мутирует Wiki. Apply остается отдельным подтверждаемым workflow:

```text
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py agents-workspace-replace-apply --profile agent.openai.api --target-path notes/example.v1 --expected-current-sha256 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef --file workspace/tmp/example-content.md --confirm --allow-non-sandbox
```

`agents-workspace-server-replace-plan` должен быть показан и проверен до apply. `agents-workspace-replace-apply` принимает только `SHA256` из plan, перечитывает live page перед записью и блокируется, если страницу изменили после review. После successful replace apply отчет содержит блок `Operation verify`: внешний агент должен показать его пользователю вместе с apply/verify status. Append в существующую страницу и delete по-прежнему требуют отдельного workflow через `agent.wiki`.

После apply, особенно если страница открывалась или редактировалась в Wiki UI, можно повторно выполнить отложенную read-only проверку operation bundle:

```text
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py agents-workspace-operation-verify --operation-bundle notes/example.v1
```

Если команда показывает `Live matches after snapshot: no`, нельзя считать operation bundle актуальным для дальнейшей записи или отката. Нужно заново читать live Wiki и строить новый replace-plan.

Если пользователь просит откатить рабочую Wiki-страницу, откат не выполняется напрямую. Сначала нужно показать read-only plan:

```text
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py agents-workspace-rollback-plan --operation-bundle notes/example.v1
```

Только если plan показывает `Safe to apply: yes` и пользователь подтверждает откат, можно запускать:

```text
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py agents-workspace-rollback-apply --operation-bundle notes/example.v1 --confirm --allow-non-sandbox
```

Для create-only операции rollback удаляет созданную страницу, если она не менялась после apply. Для replace-операции rollback восстанавливает previous content из `before` snapshot, если live page все еще совпадает с `after` snapshot. После rollback нужно сделать live/read verify и показать пользователю ссылку на страницу, результат apply и warnings/errors.

## 10. Что запрещено

Тебе запрещено:

- писать напрямую в Yandex Wiki API;
- хранить Wiki API token;
- менять `wiki_memory_root`;
- менять структуру памяти без отдельного structure-change workflow;
- считать `.agent-memory` источником истины;
- складывать в `.agent-memory` всю большую библиотеку документов;
- писать память без provenance;
- превращать каждую реплику пользователя в memory request;
- использовать чужой профиль памяти как тестовый пример без отдельного решения.
- делать fallback live write при недоступном `agent.wiki` server;
- заменять существующую страницу через команду "запиши" без отдельного `agents-workspace-server-replace-plan` и подтвержденного `agents-workspace-replace-apply`.
- продолжать follow-up write или rollback по operation bundle, если `agents-workspace-operation-verify` показывает `Live matches after snapshot: no`.
- выполнять rollback рабочей Wiki-страницы без предварительного `agents-workspace-rollback-plan` и явного подтверждения пользователя.

## 11. Как читать быстрый cache

При старте работы, если `.agent-memory` доступен, сначала ориентируйся по:

```text
.agent-memory/memory.bootstrap.md
.agent-memory/memory.context.md
.agent-memory/status.json
```

`status.json` показывает:

- `profile_id`;
- `agent_id`;
- `wiki_memory_root`;
- `source`;
- `build_mode`;
- `export_path`;
- `runtime_connected`;
- `export_status`.

Если cache отсутствует или кажется устаревшим, попроси обновить память через `agent.wiki`, а не пытайся читать Wiki напрямую.

Проверка runtime-cache выполняется через `agent.wiki`:

```text
python scripts/agent_wiki.py memory-runtime-check --profile agent.openai.api --path E:\Codex\agent.openai.api\.agent-memory
python scripts/agent_wiki.py memory-helper-boundary-audit --profile agent.openai.api
```

Новый агент не считается полностью подключенным, пока read-only boundary gate не показывает `Blocking findings: 0`. Gate блокирует direct Wiki write methods, raw API endpoints и копии protected central publishers в production Python-коде агента.

`memory-context-export-verify` должен показать `Matched: 3`, `Extra files: 0`, а `.agent-memory/memory.context.md` должен побайтно совпадать с проверенным source context. `memory-runtime-check` должен показать `Runtime ready: yes`. Если любая из этих проверок не пройдена, не считай `.agent-memory` нормальным рабочим контекстом и попроси обновить export через `agent.wiki`.

Короткий стартовый prompt для чата агента можно получить так:

```text
python scripts/agent_wiki.py memory-agent-prompt --profile agent.openai.api
```

Эта команда не заменяет чтение `.agent-memory`, а дает тебе стартовые правила: кто ты, где твой cache, что является source of truth, что нельзя делать напрямую и как готовить handoff request.

Канонический шаблон заявки на запись памяти можно получить так:

```text
python scripts/agent_wiki.py memory-handoff-template --profile agent.openai.api --type method --id method.agent.openai.api-example.v1
```

The central handoff and apply-time source-pointer gates reject incoherent values, unsafe paths, missing configured files, directories, and a missing path-only fenced block before Wiki write.
For routine writes, use the generated thin wrapper `scripts/publish_memory_rule.py`; its protected central `agent.wiki` implementation injects the canonical `## Local source` block automatically and verifies profile/project identity.

Используй шаблон как каркас. Перед передачей в `agent.wiki` замени placeholder-текст на реальную смысловую запись, которую пользователь увидел и подтвердил.

## 12. Минимальное правило поведения

Если пользователь говорит "запомни", ты должен:

1. Принять текст после "запомни" как смысловую основу будущей записи.
2. Уточнить смысл только если он неоднозначен, есть риск секрета, непонятен `entry_type` или запись конфликтует с существующей памятью.
3. Самостоятельно выбрать `entry_type`.
4. Самостоятельно предложить `entry_id`.
5. Сформулировать русский смысловой текст для Wiki memory.
6. Показать пользователю короткий отчет: что подготовлено, какой `entry_id`, куда отправлена заявка.
7. Сохранить заявку в memory outbox, если он включен.
8. Запустить `memory-server-process` и показать пользователю `report` из вывода helper.
9. Если helper подтвердил `apply` и `verify`, можно написать, что запись сохранена в live Wiki memory, и обязательно показать active links / rollback hint из отчета.
10. Если helper ушел в fallback/review или завершился ошибкой, не писать "память записана"; показать статус, причину и следующий безопасный шаг.
11. Если helper не запускался, явно написать `SERVER_OR_HELPER_NOT_RUN` и причину.
12. Не говорить, что память записана, пока `agent.wiki` не подтвердил apply и verify.
13. Если в отчете helper указал, что `.agent-memory` экспортирована и verify прошел, можно считать быстрый cache обновленным; если export не выполнен или failed, честно показать этот статус и попросить ручной export через `agent.wiki`.

Если пользователь говорит "запиши", ты должен:

1. Не оформлять это как memory request.
2. Выбрать `target_path` внутри `homepage/codex/agents/agent.openai.api`.
3. Подготовить page content.
4. Сохранить page content в `.md` файл и запустить `agents-workspace-server-write` только с `--file`.
5. Использовать только ASCII/English technical page title, обычно последний сегмент slug; русский/non-ASCII title не передавать ни через `--title`, ни через `--title-file`.
6. Показать report с active Wiki link, operation bundle и rollback command.
7. Если root `homepage/codex/agents/agent.openai.api` отсутствует, показать, что нужен отдельный `agents-workspace-root-plan` / `agents-workspace-root-apply`, и не делать обходную запись.
8. Если helper сообщает `SERVER_ENDPOINT_NOT_FOUND`, не запускать временный server на другом порту; попросить перезапустить основной `agent.wiki` server.
9. Не использовать confirmed `--text` для длинного Markdown; если helper блокирует `--text`, пересобрать content через файл.
10. Не писать "страница записана", пока helper не подтвердил apply и verify.
11. Если нужно изменить существующую страницу, не использовать `agents-workspace-server-write`: подготовить `.md` файл, вызвать `agents-workspace-server-replace-plan`, показать пользователю plan/report, получить `expected-current-sha256` из plan и применять только отдельным `agents-workspace-replace-apply --confirm --allow-non-sandbox`.
12. Если после apply нужно убедиться, что операция все еще совпадает с live Wiki, вызвать `agents-workspace-operation-verify --operation-bundle notes/example.v1` и при `Live matches after snapshot: no` не продолжать без нового live read / replace-plan.
13. Если пользователь просит откатить рабочую Wiki-страницу, сначала вызвать `agents-workspace-rollback-plan`, показать результат и выполнять `agents-workspace-rollback-apply` только после подтверждения; после отката прочитать live page и показать итог.

Это правило важнее удобства. Память должна быть проверяемой, понятной и безопасной.

## Memory consistency gate

`scripts/audit_memory_consistency.py` is a thin protected wrapper around `C:\Dropbox\Codex\agent.wiki\scripts\audit_memory_consistency.py`. The agent may edit its local rules config, but must not copy, weaken, or replace the central audit implementation.

Это обязательный gate для новых записей Wiki-памяти агента.

Перед записью новой памяти:

```powershell
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py memory-context-build --profile agent.openai.api --output "E:\Codex\agent.openai.api\workspace\memory\agent.openai.api.context.md"
python "E:\Codex\agent.openai.api\scripts\audit_memory_consistency.py" --context "E:\Codex\agent.openai.api\workspace\memory\agent.openai.api.context.md" --rules "E:\Codex\agent.openai.api\configs\memory_consistency_rules.json" --json-output "E:\Codex\agent.openai.api\workspace\memory\memory_consistency_report.json" --md-output "E:\Codex\agent.openai.api\workspace\memory\memory_consistency_report.md" --fail-on-error
```

После успешного `memory-server-process` или другого штатного apply:

```powershell
python C:\Dropbox\Codex\agent.wiki\scripts\agent_wiki.py memory-context-build --profile agent.openai.api --output "E:\Codex\agent.openai.api\workspace\memory\agent.openai.api.context.md"
python "E:\Codex\agent.openai.api\scripts\audit_memory_consistency.py" --context "E:\Codex\agent.openai.api\workspace\memory\agent.openai.api.context.md" --rules "E:\Codex\agent.openai.api\configs\memory_consistency_rules.json" --json-output "E:\Codex\agent.openai.api\workspace\memory\memory_consistency_report.json" --md-output "E:\Codex\agent.openai.api\workspace\memory\memory_consistency_report.md" --fail-on-error
```

Память считается обновленной только если `blocking_errors_total = 0`.

Если новая запись заменяет старую, новая запись обязана явно содержать `supersedes` со всеми заменяемыми `method.*`, `object.*` или `source.*` id. Старые страницы можно оставлять в Wiki как историю, но effective-active слой должен видеть их неактивными через `supersedes`.

Если gate нашел блокирующее противоречие, агент не пишет пользователю "запомнил" и не считает память обновленной. Нужно исправить новую запись, добавить корректный `supersedes`, обновить agent-specific rules в `configs/memory_consistency_rules.json` или остановиться и спросить пользователя.

## Publish memory rule helper

For routine memory writes, prefer the local wrapper:

```powershell
python scripts\publish_memory_rule.py --type method --id method.agent.openai.api-example-rule.v1 --file docs\memory-drafts\example-rule.md
python scripts\publish_memory_rule.py --type method --id method.agent.openai.api-example-rule.v1 --file docs\memory-drafts\example-rule.md --confirm
```

The wrapper is a short local entrypoint into the standard `agent.wiki` memory workflow. It prepares an outbox request, runs `memory-handoff-plan`, and with `--confirm` runs `memory-server-process`, verifies the live entry page, and reruns the consistency gate.
The local file contains no write logic: it delegates to the protected central `C:\Dropbox\Codex\agent.wiki\scripts\publish_memory_rule.py`, which verifies that the requested profile and project root match the registered `agent_workspace_path`.
It injects the canonical copy-friendly `## Local source` block from the validated source pointer; agents do not assemble that block manually.

Rules:

- The wrapper does not write to Wiki directly.
- `--confirm` is required for live Wiki apply.
- The wrapper derives a stable idempotency key from the agent id, entry id, and exact request content.
- A timeout or lost server response never triggers fallback; retry must reuse the same idempotency key.
- The source file must include the final `entry_id`.
- Use `--supersedes method.agent.openai.api-example-rule.v1` for every older entry replaced by the new rule.
- A real source path must reference a safe local file for `available`, `generated`, or `redacted` status.
- `--source-path none` requires `--source-kind none --source-status none --source-reason no-safe-local-source`.
- Do not report memory as updated unless the wrapper completes without errors.

## Wiki local source pointers

Every new Wiki page or Wiki memory entry proposed by `agent.openai.api` must carry a local source pointer.

Use these fields in `Provenance`:

```text
- local_source_path: E:\Codex\agent.openai.api\README.md
- local_source_kind: source_of_truth | generated_from | request_source | operation_bundle | none
- local_source_status: available | generated | redacted | external_only | none
- local_source_reason: No safe local source is available (only when local_source_path is none)
```

For published Wiki pages and structured memory pages, keep the path itself in a fenced `text` block so the local source can be copied in one click and pasted directly into an address bar. Keep machine-readable fields below it:

```text
E:\Codex\agent.openai.api\README.md
```

local_source_path: E:\Codex\agent.openai.api\README.md
local_source_kind: source_of_truth | generated_from | request_source | operation_bundle | none
local_source_status: available | generated | redacted | external_only | none
local_source_reason: No safe local source is available (only when local_source_path is none)

Default local source folder for prepared shareable source notes:

```text
E:\Codex\agent.openai.api\workspace\wiki-sources
```

Rules:

- If a local file exists and is safe to share between agents, use its path in `local_source_path`.
- If the Wiki page is created from an outbox request, `local_source_path` points to the `*.request.md` file or to the operation bundle reported by `agent.wiki`.
- If the source is secret, raw-private, temporary, missing, or unsafe to share, write `local_source_path: none` and explain the reason in the entry text.
- For `none`, use the coherent `none` triple and put that explanation in `local_source_reason`.
- The central handoff/apply gate validates values, safe path shape, configured file existence, and the path-only fenced block before Wiki write.
- The standard publish helper injects the canonical copy-friendly block automatically.
- Do not put secrets, tokens, credentials, raw private chats, private raw documents, or bulky generated caches into `workspace/wiki-sources`.
- The Wiki page remains the human-readable source of truth; the local pointer is a navigation/provenance aid for other agents.

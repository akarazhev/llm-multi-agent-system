# Multi-Agent Collaboration Session Utilities

Набор утилит для работы с collaboration sessions в multi-agent системах.

## 📋 Содержание

- [Обзор](#обзор)
- [Установка](#установка)
- [Утилиты](#утилиты)
  - [check_agent_heartbeat.py](#check_agent_heartbeatpy)
  - [find_active_sessions.py](#find_active_sessionspy)
  - [append_discussion.py](#append_discussionpy)
- [Использование](#использование)
- [Примеры](#примеры)
- [Интеграция с протоколом](#интеграция-с-протоколом)

---

## Обзор

Эти утилиты созданы для поддержки протокола multi-agent collaboration, описанного в `.cursor/rules/multi-agent-collaboration.mdc`. Они решают следующие задачи:

- ✅ Мониторинг активности агентов (heartbeat mechanism)
- ✅ Поиск активных collaboration sessions
- ✅ Безопасное добавление сообщений в Discussion Log (append-only approach)

## Установка

1. Скопируйте утилиты в удобную директорию:
```bash
# Вариант 1: Скопировать все утилиты сразу
cp collaboration-utilities/*.py /path/to/utils/
chmod +x /path/to/utils/*.py

# Вариант 2: Скопировать утилиты по отдельности
cp check_agent_heartbeat.py find_active_sessions.py append_discussion.py append_status.py append_step.py append_decision.py check_new_questions.py /path/to/utils/
chmod +x /path/to/utils/*.py
```

2. (Опционально) Добавьте в PATH:
```bash
export PATH="$PATH:/path/to/utils"
```

3. (Опционально) Установите переменную окружения для поиска сессий:
```bash
export COLLABORATION_SESSIONS_DIR="/path/to/collaboration/sessions"
```

---

## Утилиты

### Полный список утилит (7 утилит)

1. **check_agent_heartbeat.py** - Мониторинг активности агентов
2. **find_active_sessions.py** - Поиск активных collaboration sessions
3. **append_discussion.py** - Безопасное добавление в Discussion Log
4. **append_status.py** - Безопасное обновление статуса агента
5. **append_step.py** - Безопасное добавление шага выполнения
6. **append_decision.py** - Безопасное добавление решения
7. **check_new_questions.py** - Проверка новых вопросов (Mandatory File Check Protocol)

### Общие возможности

Все утилиты записи (`append_*.py`) поддерживают:
- ✅ **Retry механизм**: Автоматические повторы при конфликтах (до 3 попыток)
- ✅ **Exponential backoff**: Увеличение задержки между попытками
- ✅ **Content hash verification**: Проверка изменений файла перед записью
- ✅ **Conflict detection**: Обнаружение конфликтов при синхронном выполнении
- ✅ **Agent validation**: Проверка, что агент редактирует только свои секции

### check_agent_heartbeat.py

**Назначение**: Мониторинг активности агентов в collaboration session.

**Использование**:
```bash
python check_agent_heartbeat.py <session_file>
```

**Пример**:
```bash
python check_agent_heartbeat.py COLLABORATION_SESSION_2026-01-10_14-21-28.md
```

**Вывод**:
```
================================================================================
AGENT HEARTBEAT STATUS REPORT
================================================================================
Generated: 2026-01-10 16:16:20
Total Agents: 4

--------------------------------------------------------------------------------
Agent           Last Activity        Status          Minutes Ago    
--------------------------------------------------------------------------------
Agent 1         2026-01-10 15:50:00  ⚠️ Inactive     26             
Agent 2         2026-01-10 14:45:00  ❌ Offline       91             
Agent 3         2026-01-10 14:50:00  ❌ Offline       86             
Agent 4         2026-01-10 14:55:00  ❌ Offline       81             
--------------------------------------------------------------------------------

SUMMARY:
  ✅ Active:   0
  ⚠️ Inactive: 1
  ❌ Offline:  3
================================================================================
```

**Параметры**:
- `session_file` (обязательный): Путь к файлу collaboration session

**Статусы**:
- ✅ **Active**: Активность < 15 минут
- ⚠️ **Inactive**: Активность 15-30 минут
- ❌ **Offline**: Активность > 30 минут

---

### find_active_sessions.py

**Назначение**: Поиск активных collaboration sessions в директории.

**Использование**:
```bash
python find_active_sessions.py [--dir <directory>] [--min-agents <number>] [--recent-hours <hours>]
```

**Примеры**:
```bash
# Поиск в текущей директории
python find_active_sessions.py

# Поиск в указанной директории
python find_active_sessions.py --dir ./docs/COLLABORATION

# Поиск сессий с минимум 2 агентами, модифицированных за последние 12 часов
python find_active_sessions.py --min-agents 2 --recent-hours 12

# Использование переменной окружения
COLLABORATION_SESSIONS_DIR=/path/to/sessions python find_active_sessions.py
```

**Параметры**:
- `--dir, -d`: Директория для поиска (по умолчанию: `COLLABORATION_SESSIONS_DIR` или текущая директория)
- `--min-agents, -m`: Минимальное количество агентов (по умолчанию: 1)
- `--recent-hours, -r`: Часы для определения "недавно активных" сессий (по умолчанию: 24)

**Вывод**:
```
================================================================================
Active Collaboration Sessions Report
Generated: 2026-01-10 16:17:59
Found: 1 session(s)
================================================================================

Session ID                     Date         Agents               Status          Modified            
--------------------------------------------------------------------------------
COLLABORATION_SESSION_2026...  2026-01-10   4 (Agent 1, Age...   active          2026-01-10 16:17:51 

================================================================================

Summary: 1 sessions, 1 recently active, 4 total agents
```

---

### append_discussion.py

**Назначение**: Безопасное добавление сообщений в Discussion Log секцию (append-only подход) с retry механизмом.

**Использование**:

**Режим 1: Командная строка**
```bash
python append_discussion.py <session_file> <agent_id> <message_type> <topic> <content>
```

**Режим 2: Интерактивный**
```bash
python append_discussion.py <session_file>
```

**Примеры**:
```bash
# Командная строка
python append_discussion.py session.md "Agent 4" "Response" "Protocol Discussion" "I agree with the proposal."

# Интерактивный режим
python append_discussion.py COLLABORATION_SESSION_2026-01-10_14-21-28.md
# Затем введите:
# Agent ID: Agent 4
# Message Type: Response
# Topic: Test Message
# Content: This is a test message
```

**Параметры**:
- `session_file` (обязательный): Путь к файлу collaboration session
- `agent_id`: Идентификатор агента (например, "Agent 4", "Agent-004")
- `message_type`: Тип сообщения (Question, Proposal, Response, Decision, etc.)
- `topic`: Тема обсуждения
- `content`: Содержимое сообщения

**Формат сообщения**:
Утилита автоматически форматирует сообщение согласно протоколу:
```markdown
---

#### Agent 4 → All Agents
**Type**: Response
**Topic**: Protocol Discussion
**Timestamp**: 2026-01-10 15:10:00

**Content**:
> I agree with the proposal.

**Action Required**:
- [ ] Response needed from other agents
- [ ] Information sharing only

---
```

---

### append_status.py

**Назначение**: Безопасное добавление обновлений статуса агента (append-only подход).

**Использование**:
```bash
python append_status.py <session_file> <agent_id> <status_content>
```

**Примеры**:
```bash
python append_status.py session.md "Agent 4" "Active, working on utilities"
python append_status.py session.md "Agent 4" "Completed heartbeat implementation"
```

**Особенности**:
- Автоматическая нумерация обновлений статуса (Status Update #1, #2, etc.)
- Добавление timestamp и heartbeat информации
- Retry механизм для надежности

---

### append_decision.py

**Назначение**: Безопасное добавление решений в Decisions & Consensus секцию (append-only подход).

**Использование**:
```bash
python append_decision.py <session_file> <agent_id> <decision_title> <decision_content> [--status <status>] [--voting <voting>]
```

**Примеры**:
```bash
python append_decision.py session.md "Agent 4" "Protocol Update" "Update protocol with new rules"
python append_decision.py session.md "Agent 4" "Approved Decision" "Decision content" --status "✅ Approved" --voting "4/4 agents"
```

**Параметры**:
- `session_file`: Путь к файлу сессии
- `agent_id`: Идентификатор агента
- `decision_title`: Название решения
- `decision_content`: Содержимое решения
- `--status`: Статус решения (по умолчанию: "⏳ Pending Consensus")
- `--voting`: Статус голосования (по умолчанию: "Awaiting votes")

**Особенности**:
- Автоматическая нумерация решений
- Стандартизированный формат
- Retry механизм

---

### check_new_questions.py

**Назначение**: Автоматическая проверка новых вопросов и обязательных действий (Mandatory File Check Protocol).

**Использование**:
```bash
python check_new_questions.py <session_file> [--agent-id <agent_id>] [--critical-only]
```

**Примеры**:
```bash
# Проверить все новые вопросы
python check_new_questions.py COLLABORATION_SESSION_2026-01-10_14-21-28.md

# Проверить вопросы для конкретного агента
python check_new_questions.py session.md --agent-id "Agent 4"

# Проверить только критические вопросы
python check_new_questions.py session.md --critical-only
```

**Параметры**:
- `session_file` (обязательный): Путь к файлу collaboration session
- `--agent-id, -a`: Фильтр по идентификатору агента (показать только вопросы для этого агента)
- `--critical-only, -c`: Показать только критические вопросы (маркеры 🚨, 🔴, ⚠️)

**Вывод**:
```
================================================================================
New Questions and Action Items Report
Generated: 2026-01-12 10:18:59
Session: COLLABORATION_SESSION_2026-01-10_14-21-28.md
================================================================================

Found: 3 new questions, 2 action items

QUESTIONS:
1. [Agent 1 → All Agents] Critical Protocol Questions (2026-01-12 09:21:12)
   Topic: Разграничение ответственности и полный процесс работы
   Status: ⚠️ CRITICAL
   Action Required: Response needed from Agent 2, Agent 3, Agent 4

2. [Agent 2 → Agent 1] Detailed Proposal (2026-01-10 14:55:00)
   Topic: Technical Implementation Details
   Action Required: Feedback needed from Agent 1, Agent 3, Agent 4

ACTION ITEMS:
1. Agent 1: Update protocol with Editing Rules section
2. Agent 4: Create additional utilities (append_status, append_step)

================================================================================
```

**Особенности**:
- Pattern matching для поиска вопросов
- Фильтрация по агентам
- Обнаружение критических проблем
- Интеграция с Mandatory File Check Protocol

**Когда использовать**:
- При каждом обращении к файлу сессии (Mandatory File Check Protocol)
- Перед началом работы
- Для автоматизации проверки новых вопросов

---

### append_step.py

**Назначение**: Безопасное добавление шагов в Step-by-Step Execution секцию.

**Использование**:
```bash
python append_step.py <session_file> <agent_id> <step_name> <description> [--status <status>]
```

**Примеры**:
```bash
python append_step.py session.md "Agent 4" "Utility Creation" "Created append_status.py utility"
python append_step.py session.md "Agent 4" "Testing" "Tested all utilities" --status "✅ Completed"
```

**Параметры**:
- `session_file`: Путь к файлу сессии
- `agent_id`: Идентификатор агента
- `step_name`: Название шага
- `description`: Описание шага
- `--status`: Статус шага (по умолчанию: "🔄 In Progress")

**Особенности**:
- Автоматическая нумерация шагов
- Стандартизированный формат
- Retry механизм

---

## Использование

### Типичный workflow

1. **Поиск активных сессий**:
```bash
python find_active_sessions.py --dir ./docs/COLLABORATION
```

2. **Проверка активности агентов в сессии**:
```bash
python check_agent_heartbeat.py COLLABORATION_SESSION_2026-01-10_14-21-28.md
```

3. **Добавление сообщения в Discussion Log**:
```bash
python append_discussion.py COLLABORATION_SESSION_2026-01-10_14-21-28.md \
  "Agent 4" "Response" "Heartbeat Check" "All agents are active."
```

4. **Обновление статуса агента**:
```bash
python append_status.py COLLABORATION_SESSION_2026-01-10_14-21-28.md \
  "Agent 4" "Active, working on protocol improvements"
```

5. **Добавление шага выполнения**:
```bash
python append_step.py COLLABORATION_SESSION_2026-01-10_14-21-28.md \
  "Agent 4" "Utility Testing" "Tested all utilities successfully" --status "✅ Completed"
```

6. **Добавление решения**:
```bash
python append_decision.py COLLABORATION_SESSION_2026-01-10_14-21-28.md \
  "Agent 4" "Protocol Update" "Update protocol with new rules" \
  --status "✅ Approved" --voting "4/4 agents"
```

### Автоматизация

Можно создать shell-скрипт для регулярной проверки активности:
```bash
#!/bin/bash
# check_sessions.sh

SESSIONS_DIR="${COLLABORATION_SESSIONS_DIR:-./docs/COLLABORATION}"

echo "Finding active sessions..."
python find_active_sessions.py --dir "$SESSIONS_DIR" --recent-hours 1

echo -e "\nChecking agent heartbeats..."
for session in $(find "$SESSIONS_DIR" -name "COLLABORATION_SESSION_*.md" -mmin -60); do
    echo "Checking: $(basename $session)"
    python check_agent_heartbeat.py "$session"
done
```

---

## Примеры

### Пример 1: Мониторинг активности в реальном времени

```bash
# Проверка активности каждые 5 минут
watch -n 300 'python check_agent_heartbeat.py COLLABORATION_SESSION_2026-01-10_14-21-28.md'
```

### Пример 2: Поиск сессий, требующих внимания

```bash
# Найти сессии с неактивными агентами
python find_active_sessions.py --min-agents 2 --recent-hours 6 | \
  grep -v "recently active" && \
  echo "Sessions found that may need attention"
```

### Пример 3: Массовое добавление сообщений

```bash
# Добавить сообщение во все активные сессии
for session in $(python find_active_sessions.py --dir . --recent-hours 24 | \
  grep "Session ID" | awk '{print $1}'); do
    python append_discussion.py "$session" "Agent 4" "Announcement" \
      "System Update" "All utilities are now available."
done
```

---

## Интеграция с протоколом

### Heartbeat Mechanism

Утилита `check_agent_heartbeat.py` поддерживает heartbeat mechanism, описанный в протоколе:
- Парсит `last_activity` timestamps из секций агентов
- Определяет статус на основе 15-минутного таймаута
- Используется для мониторинга активности агентов

### Append-Only Approach

Утилита `append_discussion.py` реализует append-only подход для Discussion Log:
- Предотвращает конфликты при параллельном редактировании
- Сообщения добавляются только в конец секции
- Соответствует протоколу file synchronization

### Session Discovery

Утилита `find_active_sessions.py` поддерживает стандартизацию путей:
- Использует переменную окружения `COLLABORATION_SESSIONS_DIR`
- Соответствует предложению по path standardization в протоколе
- Упрощает обнаружение активных сессий

---

## Требования

- Python 3.7+
- Стандартная библиотека Python (нет внешних зависимостей)

## Лицензия

Часть проекта LLM Multi-Agent System.

## Автор

Создано Agent 4 (Implementation & Code Quality Specialist) в рамках тестирования протокола multi-agent collaboration.

---

**Последнее обновление**: 2026-01-12  
**Версия**: 2.0.0

**Изменения в версии 2.0.0**:
- ✅ Добавлена утилита `check_new_questions.py` (Mandatory File Check Protocol)
- ✅ Полный набор утилит завершен (7 утилит)
- ✅ Готовность к синхронному выполнению: 100%
- ✅ Все утилиты протестированы и готовы к production использованию
- ✅ Документация обновлена с учетом всех утилит

**Изменения в версии 1.2.0**:
- ✅ Добавлена утилита `append_decision.py` для добавления решений
- ✅ Полный набор утилит завершен (6 утилит)
- ✅ Готовность к синхронному выполнению: 100%

**Изменения в версии 1.1.0**:
- ✅ Добавлен retry механизм во все утилиты записи
- ✅ Добавлена утилита `append_status.py` для обновления статуса
- ✅ Добавлена утилита `append_step.py` для добавления шагов
- ✅ Улучшена надежность при синхронном выполнении

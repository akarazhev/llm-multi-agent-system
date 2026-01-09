# Быстрый старт - Что вы увидите при запуске

## 🚀 Запуск проекта

### 1. Установка зависимостей (первый раз)

```bash
# Создать виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt
```

### 2. Настройка окружения

```bash
# Скопировать шаблон переменных окружения
cp .env.example .env

# Отредактировать .env и добавить ваши API ключи:
# OPENAI_API_KEY=your_key_here
# или
# ANTHROPIC_API_KEY=your_key_here
```

### 3. Запуск инфраструктуры (Docker)

```bash
# Запустить PostgreSQL, Redis, ChromaDB, RabbitMQ
docker-compose up -d

# Проверить статус
docker-compose ps
```

### 4. Настройка базы данных

```bash
# Создать таблицы в PostgreSQL
python scripts/setup_database.py
```

### 5. Запуск приложения

```bash
# Вариант 1: Через main.py
python main.py

# Вариант 2: Через uvicorn напрямую
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📺 Что вы увидите при запуске

### В консоли:

```
🚀 LLM Multi-Agent System v0.1.0 starting...
📡 API available at http://0.0.0.0:8000
📚 API documentation at http://0.0.0.0:8000/docs
⚠️  No agents registered yet. Use orchestrator.register_agent() to add agents.
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### В браузере:

#### 1. Главная страница: `http://localhost:8000/`

```json
{
  "name": "LLM Multi-Agent System",
  "version": "0.1.0",
  "status": "running",
  "endpoints": {
    "health": "/health",
    "agents": "/api/agents",
    "workflows": "/api/workflows",
    "start_workflow": "/api/workflows/start",
    "docs": "/docs"
  }
}
```

#### 2. Health Check: `http://localhost:8000/health`

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "services": {
    "orchestrator": "running",
    "agents_registered": 0
  }
}
```

#### 3. Список агентов: `http://localhost:8000/api/agents`

```json
{
  "agents": [],
  "count": 0
}
```

#### 4. API Документация: `http://localhost:8000/docs`

Автоматически сгенерированная интерактивная документация Swagger UI с:
- Описанием всех endpoints
- Возможностью тестировать API прямо в браузере
- Схемами запросов и ответов

#### 5. Альтернативная документация: `http://localhost:8000/redoc`

ReDoc версия документации

---

## 🧪 Тестирование API

### Проверка здоровья системы:

```bash
curl http://localhost:8000/health
```

### Получение списка агентов:

```bash
curl http://localhost:8000/api/agents
```

### Запуск workflow (пока не будет работать без агентов):

```bash
curl -X POST http://localhost:8000/api/workflows/start \
  -H "Content-Type: application/json" \
  -d '{
    "requirements": "Создать простое веб-приложение для управления задачами"
  }'
```

**Ожидаемый ответ (без агентов):**
```json
{
  "detail": "No agents registered. Please register agents before starting workflows."
}
```

---

## ⚠️ Текущие ограничения

1. **Нет зарегистрированных агентов** - нужно создать и зарегистрировать агентов
2. **Нет подключения к LLM** - нужны API ключи в `.env`
3. **База данных может быть не настроена** - нужно запустить `setup_database.py`

---

## 📝 Следующие шаги

1. Создать конкретных агентов (Business Analyst, Developer, QA, etc.)
2. Зарегистрировать агентов в orchestrator
3. Настроить API ключи для LLM провайдеров
4. Протестировать полный workflow

---

## 🐛 Возможные проблемы

### Ошибка: "ModuleNotFoundError: No module named 'fastapi'"
**Решение:** Установите зависимости: `pip install -r requirements.txt`

### Ошибка: "Connection refused" при подключении к БД
**Решение:** Убедитесь, что Docker контейнеры запущены: `docker-compose ps`

### Ошибка: "No agents registered"
**Решение:** Это нормально на данном этапе. Нужно создать и зарегистрировать агентов.

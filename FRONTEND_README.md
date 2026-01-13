# 🎨 Frontend UI - Быстрый старт

## ⚡ Запуск за 30 секунд

```bash
cd frontend-ui
npm install          # Только первый раз
./start-mock.sh      # Запуск с моковыми данными
```

Браузер откроется автоматически на `http://localhost:4200` 🚀

---

## 📸 Что вы увидите

### 1. Dashboard
```
┌─────────────────────────────────────────┐
│  📊 Статистика                          │
│  • 5 агентов                            │
│  • 2 активных workflow                  │
│  • 3 завершено сегодня                  │
│  • 6 всего workflow                     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🤖 Агенты                              │
│  • Business Analyst     (IDLE)          │
│  • Developer           (WORKING)        │
│  • QA Engineer         (COMPLETED)      │
│  • DevOps Engineer     (WORKING)        │
│  • Technical Writer    (IDLE)           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  📋 Последние Workflows                 │
│  1. JWT Auth API       (RUNNING)        │
│  2. WebSocket Fix      (COMPLETED)      │
│  3. K8s Setup          (COMPLETED)      │
│  4. API Docs           (COMPLETED)      │
│  5. Chat Feature       (FAILED)         │
└─────────────────────────────────────────┘
```

### 2. Workflows Page
- Таблица всех workflows
- Фильтры и поиск
- Статусы: RUNNING, COMPLETED, FAILED
- Детальный просмотр каждого workflow

### 3. Workflow Detail
- Progress bar (выполнено 2 из 6 шагов)
- Список завершенных шагов
- Созданные файлы (до 8 файлов)
- Логи ошибок (для FAILED workflows)

### 4. Agents Page
- Красивые карточки агентов
- Иконки по ролям
- Счетчики выполненных задач
- Описания ролей

---

## 🎭 Mock Mode - Подробности

### Преимущества
- ✅ Работает БЕЗ backend
- ✅ Реалистичные данные
- ✅ Быстрый старт
- ✅ Отлично для демо
- ✅ Параллельная разработка

### Mock данные включают:

**5 AI Агентов:**
```
ba_001      → Business Analyst     → IDLE      → 15 задач
dev_001     → Developer            → WORKING   → 28 задач
qa_001      → QA Engineer          → COMPLETED → 22 задачи
devops_001  → DevOps Engineer      → WORKING   → 19 задач
writer_001  → Technical Writer     → IDLE      → 12 задач
```

**6 Workflows:**
```
1. JWT Authentication API        → RUNNING    → 30 min назад
2. WebSocket Memory Leak Fix     → COMPLETED  → 45 min назад
3. Kubernetes Cluster Setup      → COMPLETED  → 3 часа назад
4. API Documentation             → COMPLETED  → 1 день назад
5. Real-time Chat Feature        → FAILED     → С ошибкой
6. Performance Analysis          → COMPLETED  → 28 часов назад
```

### Как работает?

```
HTTP Request
    ↓
Mock Interceptor (перехватчик)
    ↓
if (/api/agents)     → возвращает MOCK_AGENTS
if (/api/workflows)  → возвращает MOCK_WORKFLOWS
if (/api/workflows/id) → возвращает MOCK_WORKFLOW_STATES
    ↓
Response с задержкой 500ms
```

---

## 📚 Альтернативные команды

### NPM скрипты:
```bash
npm start              # Обычный режим (нужен backend)
npm run start:mock     # Mock режим (без backend)
npm run build          # Development build
npm run build:prod     # Production build
npm test               # Запуск тестов
```

### Angular CLI:
```bash
ng serve                              # Обычный режим
ng serve --configuration=mock --open  # Mock режим
ng build --configuration=production   # Production build
```

---

## 🛠️ Технологии

```
Angular 20.3          → Latest framework
TypeScript 5.9        → Type safety
Angular Material 20   → UI components
RxJS 7.8             → Reactive programming
SCSS                 → Advanced styling
Standalone           → Modern architecture
OnPush               → Performance
```

---

## 📁 Структура проекта

```
frontend-ui/
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   └── interfaces/      # TypeScript interfaces
│   │   ├── pages/
│   │   │   ├── dashboard/       # Главная
│   │   │   ├── workflows/       # Список workflows
│   │   │   ├── workflow-detail/ # Детали workflow
│   │   │   └── agents/          # Обзор агентов
│   │   ├── shared/
│   │   │   ├── components/      # Переиспользуемые компоненты
│   │   │   └── services/        # HTTP сервисы
│   │   ├── mocks/               # 🎭 Mock данные
│   │   │   ├── mock-data.ts
│   │   │   └── mock.interceptor.ts
│   │   └── style/               # Стили SPP
│   └── environments/            # Конфигурация
├── start-mock.sh                # 🚀 Скрипт запуска
├── QUICKSTART.md                # Быстрый старт
├── MOCK_MODE.md                 # Подробная документация
└── README.md                    # Основная документация
```

---

## 🔄 Режимы работы

### 1. Mock Mode (рекомендуется для начала)
```bash
./start-mock.sh
```
- Без backend
- Моковые данные
- Быстрый старт

### 2. Development Mode (с backend)
```bash
# Terminal 1: Backend
cd ..
python main.py

# Terminal 2: Frontend
npm start
```
- Реальный backend на localhost:8000
- Живые данные
- Полная функциональность

### 3. Production Mode
```bash
npm run build:prod
# Output: dist/llm-agent-ui/
```
- Оптимизированная сборка
- Готово для деплоя

---

## 🎨 Дизайн

### Цветовая палитра (из SPP)
```
Primary:   #3061D5  (Синий Santander)
Secondary: #F17B2C  (Оранжевый)
Tertiary:  #3b82f6  (Светло-синий)
Error:     #FB333D  (Красный)
Success:   #4caf50  (Зеленый)
```

### Material Design 3
- Современные компоненты
- Плавные анимации
- Responsive grid
- Dark mode ready

---

## 📱 Responsive Design

```
Mobile:  < 600px   → Single column
Tablet:  600-900px → 2 columns
Desktop: > 900px   → 3-4 columns
```

Все компоненты адаптивные!

---

## 🐛 Troubleshooting

### Проблема: Порт занят
```bash
ng serve --configuration=mock --port 4300
```

### Проблема: Модули не найдены
```bash
rm -rf node_modules package-lock.json
npm install
```

### Проблема: Mock не работает
1. Проверьте консоль на 🎭 логи
2. Убедитесь, что используете `start:mock`
3. Hard reload: Ctrl+Shift+R

### Проблема: Скрипт не запускается
```bash
chmod +x start-mock.sh
./start-mock.sh
```

---

## 📊 Производительность

```
Начальная загрузка:  2-3 секунды
API ответ (mock):    500ms
Навигация:           Мгновенно
Bundle size:         ~2MB
```

---

## 🎯 Что можно тестировать

### Функциональность
- [x] Dashboard со статистикой
- [x] Список workflows
- [x] Детали workflow
- [x] Список агентов
- [x] Навигация
- [x] Refresh кнопки
- [x] Responsive layout

### UI/UX
- [x] Material Design компоненты
- [x] Цветовая схема
- [x] Иконки
- [x] Анимации
- [x] Loading states
- [x] Error states
- [x] Empty states

---

## 💡 Советы

1. **Быстрое демо**: Используйте mock режим для презентаций
2. **Разработка UI**: Не ждите backend, работайте параллельно
3. **Тестирование**: Легко проверить edge cases
4. **Документация**: Делайте скриншоты/видео
5. **Прототипирование**: Быстрая итерация дизайна

---

## 📚 Документация

| Файл | Описание |
|------|----------|
| `QUICKSTART.md` | Самый быстрый старт |
| `MOCK_MODE.md` | Подробно о mock режиме |
| `SETUP.md` | Полная инструкция установки |
| `README.md` | Основная документация |

---

## 🚀 Начинаем!

```bash
cd frontend-ui
npm install
./start-mock.sh
```

Откроется: **http://localhost:4200**

**Приятной разработки! 🎉**

---

## 🤝 Нужна помощь?

- Проблемы с запуском: см. `TROUBLESHOOTING` секцию
- Вопросы по mock: см. `MOCK_MODE.md`
- Общие вопросы: см. `README.md`
- Issues: GitHub Issues

---

**Made with ❤️ using Angular 20 + Material Design**

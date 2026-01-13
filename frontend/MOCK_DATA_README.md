# Запуск фронтенда с моковыми данными

## Описание

Проект настроен для работы с моковыми данными через MSW (Mock Service Worker) в режиме разработки. Это позволяет разрабатывать и тестировать фронтенд без необходимости запуска бекенда.

## Настройка

### 1. Инициализация MSW Service Worker

Service Worker уже инициализирован в `public/mockServiceWorker.js`. Если нужно переинициализировать:

```bash
npx msw init public/ --save
```

### 2. Запуск в режиме разработки

Просто запустите dev сервер:

```bash
npm run dev
```

MSW автоматически активируется в режиме разработки и будет перехватывать все API запросы, используя моковые данные из `src/test/mocks/handlers.ts`.

## Моковые данные

### Расположение

- **Handlers**: `src/test/mocks/handlers.ts` - обработчики API запросов
- **Mock Data**: `src/test/utils/test-data.ts` - моковые данные и factory функции

### Доступные эндпоинты

Все эндпоинты используют базовый URL из переменной окружения `VITE_API_BASE_URL` (по умолчанию `http://localhost:8000`):

- `GET /health` - Health check
- `GET /api/workflows` - Получить список workflows
- `GET /api/workflows/:id` - Получить workflow по ID
- `POST /api/workflows` - Создать новый workflow
- `POST /api/workflows/:id/cancel` - Отменить workflow
- `GET /api/agents` - Получить список agents
- `GET /api/agents/:id` - Получить agent по ID

### Использование Factory функций

В тестах и при разработке можно использовать factory функции для создания тестовых данных:

```typescript
import { createMockWorkflow, createMockAgent } from '@/test/utils/test-data'

// Создать workflow с кастомными параметрами
const workflow = createMockWorkflow({
  status: 'running',
  message: 'Custom message',
})

// Создать agent с кастомными параметрами
const agent = createMockAgent({
  status: 'active',
  tools: [{ name: 'custom-tool' }],
})
```

## Отключение моковых данных

Чтобы использовать реальный бекенд:

1. Установите переменную окружения:
   ```bash
   VITE_USE_MOCK_DATA=false npm run dev
   ```

2. Или измените `src/main.tsx` - закомментируйте вызов `enableMocking()`

## Проверка работы

После запуска `npm run dev`:

1. Откройте консоль браузера (F12)
2. Вы должны увидеть сообщение от MSW: `[MSW] Mocking enabled.`
3. Все API запросы будут перехватываться и обрабатываться моковыми данными

## Добавление новых моковых данных

1. Добавьте новые данные в `src/test/utils/test-data.ts`
2. Обновите handlers в `src/test/mocks/handlers.ts`
3. Перезапустите dev сервер

## Troubleshooting

### MSW не работает

1. Проверьте, что файл `public/mockServiceWorker.js` существует
2. Проверьте консоль браузера на наличие ошибок
3. Убедитесь, что вы в режиме разработки (`npm run dev`)

### Service Worker не регистрируется

1. Очистите кэш браузера
2. Перезагрузите страницу с очисткой кэша (Ctrl+Shift+R / Cmd+Shift+R)
3. Проверьте, что браузер поддерживает Service Workers

# Dashboard Service - Информация о проекте

## 📦 Что создано

Полноценный web-сервис для персонализированных дашбордов с:
- ✅ Backend на FastAPI (Python)
- ✅ Frontend на React + Vite
- ✅ Интеграция с PostgreSQL
- ✅ Интеграция с Planfix REST API
- ✅ JWT аутентификация
- ✅ Красивый UI с таблицами
- ✅ Автоматическая фильтрация данных по пользователю

---

## 📁 Структура проекта

```
test-cursor/
│
├── backend/                          # Backend приложение (FastAPI)
│   ├── app/
│   │   ├── api/                     # API endpoints
│   │   │   ├── auth.py              # Аутентификация (логин, токены)
│   │   │   └── dashboard.py         # Дашборды (получение данных)
│   │   ├── core/                    # Ядро системы
│   │   │   ├── config.py            # Конфигурация из .env
│   │   │   ├── security.py          # JWT токены
│   │   │   └── database.py          # PostgreSQL подключение
│   │   ├── models/                  # Модели данных
│   │   │   └── schemas.py           # Pydantic схемы
│   │   ├── services/                # Бизнес-логика
│   │   │   ├── planfix_service.py   # Работа с Planfix API
│   │   │   └── dashboard_service.py # SQL-запросы для дашбордов
│   │   └── main.py                  # Главный файл FastAPI
│   ├── requirements.txt             # Python зависимости
│   ├── run.py                       # Скрипт запуска
│   ├── .env                         # Конфигурация (создан с вашими данными)
│   └── README.md                    # Документация backend
│
├── frontend/                         # Frontend приложение (React)
│   ├── src/
│   │   ├── components/              # React компоненты
│   │   │   ├── DataTable.jsx        # Компонент таблицы
│   │   │   └── DataTable.css
│   │   ├── pages/                   # Страницы
│   │   │   ├── LoginPage.jsx        # Страница входа
│   │   │   ├── LoginPage.css
│   │   │   ├── DashboardPage.jsx    # Главный дашборд
│   │   │   └── DashboardPage.css
│   │   ├── services/                # API клиенты
│   │   │   └── api.js               # Axios для backend API
│   │   ├── App.jsx                  # Главный компонент
│   │   ├── App.css
│   │   ├── main.jsx                 # Точка входа
│   │   └── index.css                # Глобальные стили
│   ├── index.html                   # HTML шаблон
│   ├── vite.config.js               # Конфигурация Vite
│   ├── package.json                 # Node зависимости
│   └── README.md                    # Документация frontend
│
├── .gitignore                        # Git ignore файл
├── README.md                         # Главная документация
├── START.md                          # 🚀 Быстрый старт
├── INSTRUCTIONS_RU.md                # 📋 Подробная инструкция
├── PROJECT_INFO.md                   # 📦 Этот файл
├── start_backend.bat                 # Скрипт запуска backend (Windows)
└── start_frontend.bat                # Скрипт запуска frontend (Windows)
```

---

## 🔧 Технологии

### Backend
- **FastAPI** 0.109.0 - современный web-фреймворк
- **SQLAlchemy** 2.0.25 - ORM для PostgreSQL
- **Pydantic** 2.5.3 - валидация данных
- **Python-Jose** 3.3.0 - JWT токены
- **Httpx** 0.26.0 - HTTP клиент для Planfix API
- **Psycopg2** 2.9.9 - PostgreSQL драйвер
- **Uvicorn** 0.27.0 - ASGI сервер

### Frontend
- **React** 18.2.0 - UI библиотека
- **Vite** 5.0.12 - сборщик (быстрее Webpack)
- **Axios** 1.6.5 - HTTP клиент
- **React Router** 6.21.3 - роутинг (подготовлено, если понадобится)

### Database
- **PostgreSQL** - ваша существующая база

### External APIs
- **Planfix REST API** - для получения данных пользователей

---

## 🔐 Безопасность

### Реализовано:
- ✅ JWT токены для аутентификации
- ✅ CORS настроен для безопасной работы
- ✅ Пароли и токены в переменных окружения (.env)
- ✅ HTTP Bearer authentication
- ✅ Автоматическая валидация токенов
- ✅ Защита от SQL-инъекций (параметризованные запросы)

### Для production дополнительно нужно:
- 🔒 HTTPS (SSL сертификат)
- 🔒 Сильный SECRET_KEY (сгенерировать случайный)
- 🔒 DEBUG=False
- 🔒 Rate limiting для API
- 🔒 Логирование запросов

---

## 🎯 Как это работает

### Флоу аутентификации:

```
1. Пользователь вводит EMAIL на LoginPage
         ↓
2. Frontend → POST /api/auth/login
         ↓
3. Backend запрашивает Planfix API по email
         ↓
4. Planfix возвращает данные пользователя (ФИО, ID)
         ↓
5. Backend создает JWT токен с ФИО внутри
         ↓
6. Frontend сохраняет токен в localStorage
         ↓
7. Редирект на DashboardPage
```

### Флоу получения данных:

```
1. DashboardPage загружается
         ↓
2. Frontend → GET /api/dashboard/ (с JWT токеном в header)
         ↓
3. Backend декодирует токен → получает ФИО пользователя
         ↓
4. Backend выполняет SQL-запросы с фильтром WHERE user = 'ФИО'
         ↓
5. Backend возвращает массив дашбордов с данными
         ↓
6. Frontend отображает таблицы через DataTable компонент
```

---

## 📊 Формат данных

### Запрос логина:
```json
POST /api/auth/login
{
  "email": "user@company.com"
}
```

### Ответ логина:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user_name": "Иванов Иван Иванович",
  "user_email": "user@company.com"
}
```

### Запрос дашборда:
```http
GET /api/dashboard/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Ответ дашборда:
```json
{
  "user_name": "Иванов Иван Иванович",
  "items": [
    {
      "id": "conversions",
      "title": "Конверсии КП",
      "description": "Показатели конверсии коммерческих предложений",
      "data": [
        {
          "Менеджер": "Иванов Иван",
          "Кол-во КП": 25,
          "Конверсия": "85.5%"
        }
      ],
      "columns": ["Менеджер", "Кол-во КП", "Конверсия"]
    }
  ]
}
```

---

## 🎨 UI/UX Особенности

### LoginPage:
- Красивый градиентный фон
- Валидация email
- Сообщения об ошибках
- Loading состояние при входе
- Анимация появления

### DashboardPage:
- Персонализированное приветствие с именем
- Header с кнопкой выхода
- Карточки для каждого дашборда
- Responsive дизайн

### DataTable:
- Автоматическое форматирование чисел
- Цветовая индикация процентов:
  - 🟢 ≥70% - зеленый
  - 🟡 40-69% - желтый
  - 🟠 <40% - оранжевый
- Zebra striping (чередующиеся строки)
- Sticky header при скролле
- Hover эффекты
- Адаптивный дизайн для мобильных

---

## 🚀 Быстрый старт

### Вариант 1: Используйте .bat скрипты (Windows)

**Терминал 1:**
```bash
start_backend.bat
```

**Терминал 2:**
```bash
start_frontend.bat
```

### Вариант 2: Ручной запуск

См. файл `START.md`

---

## 📝 Что нужно сделать дальше

### 1. ⚠️ ОБЯЗАТЕЛЬНО: Добавьте ваши SQL-запросы

Файл: `backend/app/services/dashboard_service.py`

Сейчас там примерные запросы. Замените их на реальные из вашей БД.

Подробная инструкция: `INSTRUCTIONS_RU.md`

### 2. Проверьте формат ФИО в базе

Убедитесь, что столбец "user" в ваших таблицах содержит ФИО в том же формате, что возвращает Planfix.

### 3. Протестируйте с реальными пользователями

Попросите коллег войти и проверить свои данные.

### 4. Добавьте больше дашбордов

По аналогии добавьте все нужные метрики и таблицы.

### 5. (Опционально) Добавьте графики

Установите библиотеку для графиков:
```bash
cd frontend
npm install recharts
```

И создайте компоненты для визуализации.

---

## 🐛 Отладка

### Backend логи:
Backend выводит все в консоль:
- SQL запросы (когда DEBUG=True)
- Ошибки подключения
- HTTP запросы

### Frontend логи:
Откройте DevTools (F12) → Console

### API документация:
http://localhost:8000/api/docs - интерактивная документация Swagger

### Health check:
http://localhost:8000/api/health - проверка работоспособности

---

## 📞 API Endpoints

### Authentication
- `POST /api/auth/login` - Вход по email
- `GET /api/auth/me` - Получить текущего пользователя

### Dashboard
- `GET /api/dashboard/` - Получить все дашборды
- `GET /api/dashboard/items` - Получить только элементы
- `POST /api/dashboard/query` - Выполнить кастомный запрос (dev)

### System
- `GET /` - Информация об API
- `GET /api/health` - Health check

---

## 🔮 Идеи для расширения

### В ближайшее время:
- [ ] Добавить все нужные SQL-запросы
- [ ] Настроить производственный деплой
- [ ] Добавить логирование действий пользователей

### В будущем:
- [ ] Графики и диаграммы (Chart.js, Recharts)
- [ ] Экспорт данных в Excel/CSV
- [ ] Фильтры и поиск по таблицам
- [ ] Кэширование данных (Redis)
- [ ] Email уведомления
- [ ] Мобильное приложение
- [ ] Админ-панель для управления дашбордами
- [ ] Темная тема

---

## 💾 База данных

### Подключение:
- Host: pg4.sweb.ru
- Port: 5433
- Database: headcorne_test
- User: headcorne_test

### Важно:
В ваших таблицах должен быть столбец с ФИО пользователя для фильтрации.

Примеры названий столбца:
- `user`
- `manager_name`
- `employee_name`
- `full_name`

---

## 🌐 Planfix API

### REST API:
- URL: https://megamindru.planfix.ru/rest/
- Token: 3325457cab2f1a9b69b3c9191eeadc82

### Используется для:
- Получения данных пользователя по email
- Получения ФИО пользователя
- Аутентификации

---

## 📚 Документация

- **START.md** - Быстрый старт для новичков
- **INSTRUCTIONS_RU.md** - Подробная инструкция по настройке
- **README.md** - Общее описание проекта
- **backend/README.md** - Backend документация
- **frontend/README.md** - Frontend документация
- **PROJECT_INFO.md** - Этот файл (техническая информация)

---

## 🤝 Поддержка

При возникновении проблем:

1. Проверьте логи backend и frontend
2. Откройте http://localhost:8000/api/health
3. Проверьте настройки в .env
4. Посмотрите документацию выше

---

Создано: 24 декабря 2025
Версия: 1.0.0





# Backend - Dashboard Service

FastAPI backend для персонализированного дашборда.

## Установка

### 1. Создайте виртуальное окружение

```bash
python -m venv venv
```

### 2. Активируйте виртуальное окружение

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Настройте переменные окружения

Создайте файл `.env` в папке `backend/`:

```env
# PostgreSQL Database
DB_HOST=pg4.sweb.ru
DB_PORT=5433
DB_USER=headcorne_test
DB_PASSWORD=Ss8SRGP5TH3W6J@L
DB_NAME=headcorne_test

# Planfix REST API
PLANFIX_API_URL=https://megamindru.planfix.ru/rest/
PLANFIX_API_TOKEN=3325457cab2f1a9b69b3c9191eeadc82

# Security (ВАЖНО: Измените SECRET_KEY в production!)
SECRET_KEY=your-super-secret-key-change-this-in-production-at-least-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Application
APP_NAME=Dashboard Service
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Запуск

### Вариант 1: Через run.py

```bash
python run.py
```

### Вариант 2: Через uvicorn

```bash
uvicorn app.main:app --reload --port 8000
```

Сервер запустится на `http://localhost:8000`

## API Документация

После запуска доступна по адресам:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Endpoints

### Аутентификация

**POST /api/auth/login**
- Вход по email
- Body: `{"email": "user@example.com"}`
- Response: JWT токен и информация о пользователе

**GET /api/auth/me**
- Получение информации о текущем пользователе
- Headers: `Authorization: Bearer <token>`

### Дашборд

**GET /api/dashboard/**
- Получение всех данных дашборда для текущего пользователя
- Headers: `Authorization: Bearer <token>`

**GET /api/dashboard/items**
- Получение списка элементов дашборда
- Headers: `Authorization: Bearer <token>`

### Служебные

**GET /**
- Информация об API

**GET /api/health**
- Проверка здоровья сервиса и подключения к БД

## Структура

```
backend/
├── app/
│   ├── api/              # API endpoints
│   │   ├── auth.py       # Аутентификация
│   │   └── dashboard.py  # Дашборды
│   ├── core/             # Конфигурация
│   │   ├── config.py     # Настройки
│   │   ├── security.py   # JWT токены
│   │   └── database.py   # Подключение к БД
│   ├── models/           # Модели данных
│   │   └── schemas.py    # Pydantic схемы
│   ├── services/         # Бизнес-логика
│   │   ├── planfix_service.py   # Работа с Planfix API
│   │   └── dashboard_service.py # Работа с дашбордами
│   └── main.py           # Главный файл приложения
├── requirements.txt      # Зависимости
├── run.py               # Скрипт запуска
└── .env                 # Переменные окружения (создать вручную)
```

## Добавление новых дашбордов

1. Откройте `app/services/dashboard_service.py`
2. Добавьте новый метод для вашего SQL-запроса (по аналогии с `_get_conversions_data`)
3. Добавьте вызов этого метода в `get_dashboard_data()`

Пример:

```python
def _get_my_custom_data(self, user_full_name: str) -> List[Dict]:
    query = """
    SELECT 
        column1,
        column2
    FROM your_table
    WHERE "user" = :user_name
    """
    return execute_query(query, {"user_name": user_full_name})
```

## Безопасность

⚠️ **ВАЖНО для production:**

1. Измените `SECRET_KEY` в `.env` на случайную строку минимум 32 символа
2. Установите `DEBUG=False`
3. Настройте правильные `CORS_ORIGINS`
4. Используйте HTTPS
5. Ограничьте доступ к endpoint `/api/dashboard/query` или удалите его

## Troubleshooting

### Ошибка подключения к базе данных

Проверьте:
- Правильность данных в `.env`
- Доступность хоста `pg4.sweb.ru:5433`
- Firewall и сетевые настройки

### Ошибка Planfix API

Проверьте:
- Правильность токена в `.env`
- Доступность `https://megamindru.planfix.ru/rest/`



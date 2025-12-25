# 📋 Инструкция по настройке Dashboard Service

## Обзор системы

Ваш дашборд состоит из:
- **Backend (FastAPI)** - получает данные из PostgreSQL и Planfix
- **Frontend (React)** - красивый интерфейс с таблицами
- **PostgreSQL** - ваша база данных с метриками
- **Planfix API** - для аутентификации пользователей

---

## Как это работает?

```
1. Пользователь вводит EMAIL
         ↓
2. Backend запрашивает Planfix API → получает ФИО пользователя
         ↓
3. Backend выполняет SQL-запросы с фильтром WHERE user = 'ФИО'
         ↓
4. Frontend отображает таблицы с данными этого пользователя
```

---

## Файлы, которые вам нужно настроить

### 1️⃣ SQL-запросы для дашбордов

**Файл:** `backend/app/services/dashboard_service.py`

**Что делать:**
1. Откройте файл
2. Найдите методы `_get_conversions_data` и `_get_preparation_time_data`
3. Замените примерные SQL-запросы на ваши реальные

**Пример реального запроса:**

```python
def _get_conversions_data(self, user_full_name: str) -> List[Dict]:
    """Конверсии КП по менеджерам"""
    query = """
    SELECT 
        manager_name as "Менеджер",
        kp_sent as "КП отправлено",
        deals_won as "Сделок выиграно",
        ROUND(deals_won::numeric / NULLIF(kp_sent, 0) * 100, 2) as "Конверсия %"
    FROM sales_statistics
    WHERE manager_name = :user_name
    ORDER BY kp_sent DESC
    LIMIT 50
    """
    
    try:
        result = execute_query(query, {"user_name": user_full_name})
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
```

**Важные моменты:**
- ✅ В запросе ОБЯЗАТЕЛЬНО должно быть `WHERE ... = :user_name`
- ✅ `:user_name` - это плейсхолдер, который заменится на ФИО пользователя
- ✅ Используйте алиасы для красивых названий столбцов: `column as "Красивое название"`
- ✅ Оберните запрос в try-except для обработки ошибок

---

### 2️⃣ Добавление новых дашбордов

**Шаги:**

1. **Создайте новый метод для запроса:**

```python
def _get_monthly_sales(self, user_full_name: str) -> List[Dict]:
    """Продажи по месяцам"""
    query = """
    SELECT 
        month_name as "Месяц",
        sales_amount as "Сумма продаж",
        deals_count as "Количество сделок"
    FROM monthly_sales
    WHERE manager_name = :user_name
    ORDER BY month_date DESC
    LIMIT 12
    """
    
    try:
        result = execute_query(query, {"user_name": user_full_name})
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
```

2. **Добавьте вызов в `get_dashboard_data`:**

```python
def get_dashboard_data(self, user_full_name: str) -> List[Dict[str, Any]]:
    dashboard_items = []
    
    # Конверсии
    conversions = self._get_conversions_data(user_full_name)
    if conversions:
        dashboard_items.append({
            "id": "conversions",
            "title": "Конверсии КП",
            "description": "Показатели конверсии коммерческих предложений",
            "data": conversions,
            "columns": list(conversions[0].keys()) if conversions else []
        })
    
    # ➕ НОВЫЙ ДАШБОРД
    monthly_sales = self._get_monthly_sales(user_full_name)
    if monthly_sales:
        dashboard_items.append({
            "id": "monthly_sales",
            "title": "Продажи по месяцам",
            "description": "Динамика продаж за последний год",
            "data": monthly_sales,
            "columns": list(monthly_sales[0].keys()) if monthly_sales else []
        })
    
    return dashboard_items
```

3. **Перезапустите backend** (Ctrl+C и снова `python run.py`)

4. **Обновите страницу в браузере** (F5)

---

## Структура базы данных

### Требования к столбцу "user"

В ваших таблицах PostgreSQL должен быть столбец с ФИО пользователя.

**Примеры:**

```sql
-- Вариант 1: столбец называется "user"
SELECT * FROM sales WHERE "user" = 'Иванов Иван Иванович';

-- Вариант 2: столбец называется "manager_name"
SELECT * FROM sales WHERE manager_name = 'Иванов Иван Иванович';

-- Вариант 3: столбец называется "employee_full_name"
SELECT * FROM sales WHERE employee_full_name = 'Иванов Иван Иванович';
```

**⚠️ ВАЖНО:**
- ФИО в базе должно совпадать с ФИО из Planfix!
- Формат: "Фамилия Имя Отчество"
- Регистр важен: "Иванов" ≠ "иванов"

---

## Проверка ФИО в Planfix

Чтобы узнать, какое ФИО возвращает Planfix:

1. Запустите backend
2. Откройте http://localhost:8000/api/docs
3. Найдите endpoint `POST /api/auth/login`
4. Нажмите "Try it out"
5. Введите email сотрудника
6. Нажмите "Execute"
7. Посмотрите в Response → `user_name` - это ФИО, которое будет использоваться для фильтрации

**Пример response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user_name": "Иванов Иван Иванович",  ← ВОТ ЭТО ФИО
  "user_email": "ivanov@company.ru"
}
```

---

## Примеры SQL-запросов из ваших скриншотов

Судя по скриншотам, у вас есть такие таблицы:

### 1. Конверсии КП

```python
def _get_conversions_data(self, user_full_name: str) -> List[Dict]:
    query = """
    SELECT 
        manager_name as "Менеджер",
        kp_count as "Кол-во КП",
        conversion_rate as "Конверсия %"
    FROM kp_conversions_table  -- замените на реальное название
    WHERE manager_name = :user_name
    ORDER BY kp_count DESC
    """
    return execute_query(query, {"user_name": user_full_name})
```

### 2. Средний срок подготовки КП

```python
def _get_preparation_time(self, user_full_name: str) -> List[Dict]:
    query = """
    SELECT 
        month_name as "Месяц",
        avg_preparation_days as "Среднее время (дней)"
    FROM kp_preparation_stats  -- замените на реальное название
    WHERE manager_name = :user_name
    ORDER BY month_date DESC
    LIMIT 12
    """
    return execute_query(query, {"user_name": user_full_name})
```

### 3. Заказы от клиентов

```python
def _get_client_orders(self, user_full_name: str) -> List[Dict]:
    query = """
    SELECT 
        client_name as "Клиент",
        orders_count as "Кол-во заказов",
        total_amount as "Сумма"
    FROM client_orders  -- замените на реальное название
    WHERE manager_name = :user_name
    ORDER BY total_amount DESC
    LIMIT 20
    """
    return execute_query(query, {"user_name": user_full_name})
```

---

## Настройка цветовой индикации в таблицах

Frontend автоматически подсвечивает процентные значения:

- 🟢 **Зеленый**: ≥ 70%
- 🟡 **Желтый**: 40-69%
- 🟠 **Оранжевый**: < 40%

Чтобы это работало, столбец должен содержать значение с символом `%`:
- ✅ `"85.5%"` - будет подсвечен
- ✅ `"45%"` - будет подсвечен
- ❌ `"85.5"` - НЕ будет подсвечен
- ❌ `85.5` (число) - НЕ будет подсвечен

**Как форматировать в SQL:**

```sql
-- Вариант 1: добавить % в запросе
SELECT 
    CONCAT(ROUND(conversion * 100, 2), '%') as "Конверсия"
FROM ...

-- Вариант 2: для PostgreSQL
SELECT 
    ROUND(conversion * 100, 2) || '%' as "Конверсия"
FROM ...
```

---

## Тестирование

### 1. Тест подключения к БД

```bash
cd backend
python
```

```python
from app.core.database import test_connection
test_connection()  # Должно вернуть True
```

### 2. Тест запроса

```python
from app.core.database import execute_query

# Проверьте, какие таблицы есть
tables = execute_query("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
""")
print(tables)

# Проверьте данные конкретного пользователя
data = execute_query("""
    SELECT * FROM your_table 
    WHERE "user" = :user_name 
    LIMIT 5
""", {"user_name": "Иванов Иван Иванович"})
print(data)
```

### 3. Тест Planfix API

```bash
cd backend
python
```

```python
import asyncio
from app.services.planfix_service import planfix_service

async def test():
    user = await planfix_service.get_user_by_email("test@example.com")
    print(user)

asyncio.run(test())
```

---

## Безопасность для Production

Когда будете разворачивать на production сервере:

### 1. Измените SECRET_KEY

`backend/.env`:
```env
SECRET_KEY=ваш-случайный-ключ-минимум-32-символа
```

Сгенерировать можно так:
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 2. Отключите DEBUG

`backend/.env`:
```env
DEBUG=False
```

### 3. Настройте CORS

`backend/.env`:
```env
CORS_ORIGINS=https://your-domain.com
```

### 4. Используйте HTTPS

Обязательно используйте SSL сертификат для production!

---

## Полезные команды

### Backend

```bash
# Запуск
cd backend
venv\Scripts\activate
python run.py

# Проверка здоровья
curl http://localhost:8000/api/health

# Просмотр API документации
# Откройте: http://localhost:8000/api/docs
```

### Frontend

```bash
# Запуск
cd frontend
npm run dev

# Сборка для production
npm run build

# Preview production сборки
npm run preview
```

---

## Частые вопросы

### ❓ Как добавить графики вместо таблиц?

Нужно установить библиотеку для графиков (например, Chart.js или Recharts) и создать новый компонент.

### ❓ Можно ли давать пользователям разные дашборды?

Да, можно добавить логику в `get_dashboard_data` для проверки роли пользователя.

### ❓ Как экспортировать данные в Excel?

Нужно добавить endpoint в backend для экспорта и кнопку в frontend.

### ❓ Можно ли кэшировать данные?

Да, можно использовать Redis или встроенный кэш Python.

---

## Что дальше?

1. ✅ Замените примерные SQL-запросы на реальные
2. ✅ Добавьте все нужные дашборды
3. ✅ Протестируйте с реальными пользователями
4. ✅ Соберите feedback
5. ✅ Добавьте новые фичи (графики, экспорт, фильтры и т.д.)

Успехов! 🚀



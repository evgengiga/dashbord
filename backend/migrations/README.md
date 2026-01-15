# Миграции базы данных

## Применение миграций

Для применения миграций выполните SQL скрипты в вашей PostgreSQL базе данных:

```bash
psql -h pg4.sweb.ru -p 5433 -U headcorne_test -d headcorne_test -f migrations/001_create_users_table.sql
```

Или через любой SQL клиент (pgAdmin, DBeaver, etc.) - просто выполните содержимое файла `001_create_users_table.sql`.

## Сброс паролей пользователей (для отладки)

### Вариант 1: Удаление пользователя (полный сброс)

```sql
-- Удалить пользователя из БД (при следующем входе потребуется регистрация)
DELETE FROM users WHERE email = 'user@example.com';
```

### Вариант 2: Изменение пароля напрямую (только для отладки!)

```sql
-- ВНИМАНИЕ: Это только для отладки! В production НЕ используйте!
-- Пароль будет: "test123"
UPDATE users 
SET password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJ5q5q5q5q'
WHERE email = 'user@example.com';
```

**Для генерации нового хеша пароля используйте Python:**

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd_context.hash("ваш_пароль"))
```

### Вариант 3: Просмотр всех пользователей

```sql
-- Посмотреть всех зарегистрированных пользователей
SELECT email, full_name, created_at FROM users;
```

## Структура таблицы users

- `id` - уникальный идентификатор
- `email` - email пользователя (уникальный)
- `password_hash` - хеш пароля (bcrypt)
- `full_name` - полное имя из Planfix
- `created_at` - дата создания
- `updated_at` - дата последнего обновления

## Безопасность

⚠️ **ВАЖНО:** 
- Пароли хранятся в виде bcrypt хешей (нельзя восстановить исходный пароль)
- Для сброса пароля нужно либо удалить пользователя, либо сгенерировать новый хеш
- В production рекомендуется добавить endpoint для сброса пароля через email








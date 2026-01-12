# 🚀 Быстрый деплой - 3 простых варианта

## ⚡ Вариант 1: Docker на вашем компьютере (5 минут)

**Что нужно:**
- Docker Desktop

**Шаги:**

1. Установите Docker Desktop: https://www.docker.com/products/docker-desktop/

2. Откройте PowerShell в папке проекта:

```bash
cd C:\Users\dante\OneDrive\Desktop\test-cursor
docker-compose up -d
```

3. **Готово!** Откройте: http://localhost

**Остановить:**
```bash
docker-compose down
```

---

## 🚂 Вариант 2: Railway (10 минут, БЕСПЛАТНО)

**Что нужно:**
- GitHub аккаунт
- Railway аккаунт

**Шаги:**

### 1. Загрузите проект на GitHub

```bash
cd C:\Users\dante\OneDrive\Desktop\test-cursor

# Инициализируйте git (если еще не сделали)
git init
git add .
git commit -m "Initial commit"

# Создайте репозиторий на GitHub.com и загрузите
git remote add origin https://github.com/ваш-username/dashboard.git
git push -u origin main
```

### 2. Зарегистрируйтесь на Railway

1. Откройте: https://railway.app
2. Sign up with GitHub
3. Авторизуйте Railway

### 3. Создайте проект

1. Dashboard → **New Project**
2. **Deploy from GitHub repo**
3. Выберите ваш репозиторий `dashboard`
4. Railway автоматически найдет `docker-compose.yml`

### 4. Настройте переменные окружения

В Railway Dashboard для **backend** сервиса:

```
DB_HOST=pg4.sweb.ru
DB_PORT=5433
DB_USER=headcorne_test
DB_PASSWORD=Ss8SRGP5TH3W6J@L
DB_NAME=headcorne_test
PLANFIX_API_URL=https://megamindru.planfix.ru/rest/
PLANFIX_API_TOKEN=3325457cab2f1a9b69b3c9191eeadc82
SECRET_KEY=generate-random-32-character-string-here
DEBUG=False
```

### 5. Получите URL

Railway выдаст вам URL типа:
- `https://dashboard-production-xxxx.up.railway.app`

**Готово!** Открывайте и пользуйтесь!

---

## 🎨 Вариант 3: Render (15 минут, БЕСПЛАТНО)

**Преимущество:** Совсем бесплатный тариф (но с ограничениями)

**Шаги:**

### 1. Backend на Render

1. Откройте: https://render.com
2. Sign up (можно через GitHub)
3. **New → Web Service**
4. Connect ваш GitHub репозиторий
5. Настройки:
   - **Name:** `dashboard-backend`
   - **Root Directory:** `backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

6. Environment Variables (добавьте все переменные из Railway выше)

7. **Create Web Service**

8. Дождитесь деплоя (5-10 минут)

9. Скопируйте URL (например: `https://dashboard-backend.onrender.com`)

### 2. Frontend на Render (или Vercel/Netlify)

#### Вариант 2A: Render

1. **New → Static Site**
2. Connect репозиторий
3. Настройки:
   - **Name:** `dashboard-frontend`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
4. Environment Variables:
   ```
   VITE_API_URL=https://dashboard-backend.onrender.com/api
   ```
5. **Create Static Site**

#### Вариант 2B: Vercel (быстрее и удобнее)

1. Откройте: https://vercel.com
2. Sign up через GitHub
3. **New Project**
4. Import ваш репозиторий
5. Настройки:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - Environment Variables:
     ```
     VITE_API_URL=https://dashboard-backend.onrender.com/api
     ```
6. **Deploy**

**Готово!** URL типа: `https://dashboard-username.vercel.app`

### 3. Обновите CORS в backend

В Render Dashboard → backend service → Environment:

Добавьте/обновите:
```
CORS_ORIGINS=https://dashboard-username.vercel.app,https://your-domain.com
```

Redeploy backend.

---

## 📊 Сравнение вариантов

| Вариант | Время | Стоимость | Сложность | Доступность |
|---------|-------|-----------|-----------|-------------|
| **Docker локально** | 5 мин | Бесплатно | ⭐ Очень легко | Только на вашем ПК |
| **Railway** | 10 мин | $5 free | ⭐⭐ Легко | Весь интернет |
| **Render** | 15 мин | Бесплатно* | ⭐⭐ Легко | Весь интернет |

*Render бесплатный, но засыпает после 15 мин неактивности и просыпается 30-60 сек

---

## 🎯 Моя рекомендация

### Для быстрого тестирования:
→ **Docker локально** (5 минут)

### Для production (~20 пользователей):
→ **Railway** (проще всего, $5 хватит надолго)

### Если нужен полностью бесплатный:
→ **Render** (но будет "засыпать")

---

## После деплоя

1. ✅ Откройте ваш URL
2. ✅ Войдите с email из Planfix
3. ✅ Добавьте свои SQL-запросы (см. INSTRUCTIONS_RU.md)
4. ✅ Поделитесь ссылкой с коллегами

---

## Проблемы?

### ❌ "Database connection failed"
- Проверьте, что PostgreSQL pg4.sweb.ru доступен из интернета
- Возможно, нужно добавить IP сервера в whitelist

### ❌ CORS ошибки
- Обновите `CORS_ORIGINS` в backend с URL вашего frontend

### ❌ Render сервис "засыпает"
- Это нормально для бесплатного тарифа
- Перейдите на платный ($7/мес) или используйте Railway

---

Нужна помощь с конкретным вариантом? Спрашивайте! 🚀





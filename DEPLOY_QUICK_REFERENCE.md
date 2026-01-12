# ⚡ Быстрая шпаргалка по деплою на Render

## 🎯 Минимальные шаги (5 минут)

### 1. Backend (Web Service)

**Настройки:**
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Environment Variables:**
```
DB_HOST=pg4.sweb.ru
DB_PORT=5433
DB_USER=headcorne_test
DB_PASSWORD=Ss8SRGP5TH3W6J@L
DB_NAME=headcorne_test
PLANFIX_API_URL=https://megamindru.planfix.ru/rest/
PLANFIX_API_TOKEN=3325457cab2f1a9b69b3c9191eeadc82
SECRET_KEY=ваш-случайный-ключ-32-символа-минимум
DEBUG=False
CORS_ORIGINS=*
```

### 2. Frontend (Static Site)

**Настройки:**
- Root Directory: `frontend`
- Build Command: `npm install && npm run build`
- Publish Directory: `dist`

**Environment Variable:**
```
VITE_API_URL=https://ваш-backend-url.onrender.com/api
```

### 3. Обновите CORS

В backend Environment Variables:
```
CORS_ORIGINS=https://ваш-frontend-url.onrender.com
```

Передеплойте backend.

### 4. Примените миграции

Выполните SQL из `backend/migrations/001_create_users_table.sql` в вашей БД.

---

## 🔗 Полезные ссылки

- **Render Dashboard:** https://dashboard.render.com
- **GitHub репозиторий:** https://github.com/evgengiga/dashbord
- **Полная инструкция:** см. `DEPLOY_FULL_GUIDE.md`

---

## ⚠️ Частые ошибки

1. **CORS ошибка** → Обновите `CORS_ORIGINS` в backend
2. **Backend не запускается** → Проверьте `Root Directory` = `backend`
3. **Frontend пустой** → Проверьте `VITE_API_URL`
4. **Database error** → Проверьте все DB переменные

---

**Полная инструкция:** `DEPLOY_FULL_GUIDE.md`


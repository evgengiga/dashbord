# 🚀 Backend на Render, Frontend на Beget

## ✅ Что это даст

- ✅ Backend работает на Render (бесплатно, автоматически)
- ✅ Frontend остается на Beget (твой домен)
- ✅ Не нужно возиться с Docker и Python на Beget
- ✅ Все работает автоматически

---

## 🎯 ШАГ 1: Задеплоить Backend на Render

### 1.1. Зарегистрируйся на Render

1. Открой: https://render.com
2. Sign up (можно через GitHub)
3. Подтверди email

### 1.2. Создай Web Service для Backend

1. В Dashboard нажми **New → Web Service**
2. **Connect GitHub** (или GitLab/Bitbucket) - подключи свой репозиторий
3. Если репозитория нет:
   - Создай на GitHub
   - Загрузи код туда

### 1.3. Настрой Backend Service

**Основные настройки:**
- **Name:** `dashboard-backend`
- **Root Directory:** `backend` (важно!)
- **Environment:** `Python 3`
- **Region:** `Frankfurt` (ближе к России)
- **Branch:** `main` (или `master`)
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Plan:** `Free` (бесплатный)

### 1.4. Добавь Environment Variables

В разделе **Environment Variables** добавь:

```
DB_HOST=pg4.sweb.ru
DB_PORT=5433
DB_USER=headcorne_test
DB_PASSWORD=Ss8SRGP5TH3W6J@L
DB_NAME=headcorne_test
PLANFIX_API_URL=https://megamindru.planfix.ru/rest/
PLANFIX_API_TOKEN=3325457cab2f1a9b69b3c9191eeadc82
SECRET_KEY=super-secret-key-change-in-production-min-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
APP_NAME=Dashboard Service
DEBUG=False
CORS_ORIGINS=https://dashboard.headcorn.pro
```

**⚠️ ВАЖНО:** 
- `SECRET_KEY` - замени на случайную строку минимум 32 символа
- `CORS_ORIGINS` - укажи свой домен на Beget (например: `https://dashboard.headcorn.pro`)

### 1.5. Создай Service

Нажми **Create Web Service**

### 1.6. Дождись деплоя

Render начнет деплой (5-10 минут). Следи за логами.

### 1.7. Скопируй URL Backend

После деплоя Render даст URL типа:
- `https://dashboard-backend.onrender.com`

**Скопируй этот URL!** Он понадобится для frontend.

---

## 🎯 ШАГ 2: Настроить Frontend на Beget

### 2.1. Обнови .env файл Frontend

**На своем компьютере:**

1. Открой `frontend/.env.production` (или создай, если нет)
2. Добавь:

```env
VITE_API_URL=https://dashboard-backend.onrender.com/api
```

**Замени `dashboard-backend.onrender.com` на свой URL из Render!**

### 2.2. Пересобери Frontend

**На своем компьютере:**

```bash
cd frontend
npm install
npm run build
```

### 2.3. Загрузи на Beget

**Через FileZilla или scp:**

1. Скопируй все файлы из `frontend/dist/` в `~/dashboard.headcorn.pro/public_html/`
2. Замени все старые файлы

---

## 🎯 ШАГ 3: Обновить CORS в Backend (если нужно)

**В Render Dashboard:**

1. Открой свой backend service
2. Перейди в **Environment**
3. Обнови `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://dashboard.headcorn.pro
   ```
4. Нажми **Save Changes**
5. Render автоматически перезапустит backend

---

## 🎯 ШАГ 4: Проверка

1. Открой свой сайт: `https://dashboard.headcorn.pro`
2. Попробуй войти
3. Если работает - готово!

---

## 🔧 Если что-то не работает

### Проблема 1: CORS ошибки

**Решение:** Проверь, что в Render `CORS_ORIGINS` содержит твой домен:
```
CORS_ORIGINS=https://dashboard.headcorn.pro
```

### Проблема 2: 404 на API запросы

**Решение:** Проверь, что в `frontend/.env.production` правильный URL:
```env
VITE_API_URL=https://dashboard-backend.onrender.com/api
```

**И пересобери frontend:**
```bash
cd frontend
npm run build
```

### Проблема 3: Backend не запускается на Render

**Проверь логи в Render Dashboard:**
1. Открой backend service
2. Перейди в **Logs**
3. Смотри на ошибки

**Частые ошибки:**
- Неправильный `Root Directory` (должно быть `backend`)
- Неправильный `Start Command` (должно быть `uvicorn app.main:app --host 0.0.0.0 --port $PORT`)
- Отсутствуют переменные окружения

---

## 📝 Важные замечания

1. **Render Free Plan:**
   - Backend "засыпает" после 15 минут неактивности
   - Первый запрос после "сна" занимает 30-60 секунд
   - Для production лучше использовать Paid Plan ($7/мес)

2. **Автоматический деплой:**
   - При каждом push в GitHub, Render автоматически передеплоит backend
   - Frontend нужно пересобирать и загружать вручную

3. **Обновление Frontend:**
   - Измени код
   - Выполни `npm run build` в `frontend/`
   - Загрузи файлы из `dist/` на Beget

---

## ✅ Готово!

Теперь:
- ✅ Backend работает на Render (автоматически)
- ✅ Frontend на Beget (твой домен)
- ✅ Все работает без Docker и Python на Beget

**Если нужна помощь с каким-то шагом - напиши!**





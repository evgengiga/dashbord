# 🐳 Инструкция: Запуск backend ВНУТРИ Docker окружения

## Как это работало вчера

Вчера вы заходили **ВНУТРЬ** Docker контейнера и запускали backend там. Это объясняет, почему Python 3.11 работал - он работал внутри Docker, где GLIBC правильная версия.

---

## 🎯 Способ 1: Зайти в существующий контейнер (если есть)

**Выполни в PuTTY:**

```bash
# Проверь, есть ли запущенные контейнеры
docker ps 2>&1

# Если есть контейнер с именем dashboard, зайди в него
docker exec -it dashboard-backend bash

# Или найди ID контейнера
docker ps
docker exec -it <CONTAINER_ID> bash
```

**Внутри контейнера выполни:**

```bash
cd /app
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 🎯 Способ 2: Запустить новый контейнер в интерактивном режиме

**Выполни в PuTTY:**

```bash
cd ~/dashboard.headcorn.pro/backend

# Запусти контейнер в интерактивном режиме
docker run -it --rm \
  -p 8001:8000 \
  -v $(pwd):/app \
  -w /app \
  -e DB_HOST=pg4.sweb.ru \
  -e DB_PORT=5433 \
  -e DB_USER=headcorne_test \
  -e DB_PASSWORD=Ss8SRGP5TH3W6J@L \
  -e DB_NAME=headcorne_test \
  -e PLANFIX_API_URL=https://megamindru.planfix.ru/rest/ \
  -e PLANFIX_API_TOKEN=3325457cab2f1a9b69b3c9191eeadc82 \
  -e SECRET_KEY=super-secret-key-change-in-production-min-32-characters-long \
  -e ALGORITHM=HS256 \
  -e ACCESS_TOKEN_EXPIRE_MINUTES=1440 \
  -e APP_NAME=Dashboard\ Service \
  -e DEBUG=False \
  -e CORS_ORIGINS=https://dashboard.headcorn.pro \
  python:3.11-slim \
  bash
```

**Если нет прав, попробуй с sudo:**

```bash
sudo docker run -it --rm \
  -p 8001:8000 \
  -v $(pwd):/app \
  -w /app \
  -e DB_HOST=pg4.sweb.ru \
  -e DB_PORT=5433 \
  -e DB_USER=headcorne_test \
  -e DB_PASSWORD=Ss8SRGP5TH3W6J@L \
  -e DB_NAME=headcorne_test \
  -e PLANFIX_API_URL=https://megamindru.planfix.ru/rest/ \
  -e PLANFIX_API_TOKEN=3325457cab2f1a9b69b3c9191eeadc82 \
  -e SECRET_KEY=super-secret-key-change-in-production-min-32-characters-long \
  -e ALGORITHM=HS256 \
  -e ACCESS_TOKEN_EXPIRE_MINUTES=1440 \
  -e APP_NAME=Dashboard\ Service \
  -e DEBUG=False \
  -e CORS_ORIGINS=https://dashboard.headcorn.pro \
  python:3.11-slim \
  bash
```

**После этого ты окажешься ВНУТРИ контейнера. Выполни:**

```bash
# 1. Установи зависимости
pip install -r requirements.txt

# 2. Запусти backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Или запусти в фоне (чтобы можно было выйти из контейнера):**

```bash
# Запусти в фоне
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > /app/backend.log 2>&1 &

# Проверь, что запустилось
ps aux | grep uvicorn

# Выйди из контейнера (контейнер продолжит работать)
exit
```

---

## 🎯 Способ 3: Использовать автоматический скрипт

**Скопируй скрипт `start_backend_inside_docker.sh` на сервер и выполни:**

```bash
cd ~/dashboard.headcorn.pro
chmod +x start_backend_inside_docker.sh
./start_backend_inside_docker.sh
```

---

## ⚠️ Важные замечания

1. **Порт 8001:** Backend будет доступен на порту 8001 снаружи (внутри контейнера на 8000)

2. **Монтирование папки:** Флаг `-v $(pwd):/app` монтирует папку `backend` в `/app` внутри контейнера, так что все изменения видны сразу

3. **Переменные окружения:** Все настройки передаются через `-e` флаги

4. **Интерактивный режим:** Флаг `-it` позволяет зайти внутрь контейнера

5. **Автоматическое удаление:** Флаг `--rm` удалит контейнер после выхода (если не запущен в фоне)

---

## 🔄 Если нужно перезапустить

1. **Выйди из контейнера:** `exit`
2. **Запусти заново:** Выполни команду из Способа 2 снова

---

## 📝 Для постоянной работы (автозапуск)

Если нужно, чтобы контейнер работал постоянно, используй фоновый режим:

```bash
docker run -d \
  --name dashboard-backend \
  -p 8001:8000 \
  --restart unless-stopped \
  -v $(pwd):/app \
  -w /app \
  -e DB_HOST=pg4.sweb.ru \
  -e DB_PORT=5433 \
  -e DB_USER=headcorne_test \
  -e DB_PASSWORD=Ss8SRGP5TH3W6J@L \
  -e DB_NAME=headcorne_test \
  -e PLANFIX_API_URL=https://megamindru.planfix.ru/rest/ \
  -e PLANFIX_API_TOKEN=3325457cab2f1a9b69b3c9191eeadc82 \
  -e SECRET_KEY=super-secret-key-change-in-production-min-32-characters-long \
  -e ALGORITHM=HS256 \
  -e ACCESS_TOKEN_EXPIRE_MINUTES=1440 \
  -e APP_NAME=Dashboard\ Service \
  -e DEBUG=False \
  -e CORS_ORIGINS=https://dashboard.headcorn.pro \
  python:3.11-slim \
  bash -c "pip install -r requirements.txt && uvicorn app.main:app --host 0.0.0.0 --port 8000"
```

Но для этого нужны права на Docker. Если нет прав, используй Способ 2 (интерактивный режим).






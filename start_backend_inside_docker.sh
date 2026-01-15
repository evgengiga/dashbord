#!/bin/bash
# Скрипт для запуска backend ВНУТРИ Docker окружения
# Как это работало вчера

set -e

echo "🐳 Запуск backend ВНУТРИ Docker окружения..."
echo ""

cd ~/dashboard.headcorn.pro/backend

# Цвета
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Способ 1: Попробовать зайти в существующий контейнер
echo -e "${YELLOW}🔍 Способ 1: Поиск существующего контейнера...${NC}"

# Проверяем через docker ps (может быть есть права на чтение)
if docker ps >/dev/null 2>&1; then
    CONTAINER_ID=$(docker ps --filter "name=dashboard" --format "{{.ID}}" 2>/dev/null | head -1)
    if [ ! -z "$CONTAINER_ID" ]; then
        echo -e "${GREEN}✅ Найден контейнер: $CONTAINER_ID${NC}"
        echo "Заходим в контейнер..."
        docker exec -it $CONTAINER_ID bash
        exit 0
    fi
fi

# Способ 2: Запустить новый контейнер в интерактивном режиме
echo -e "${YELLOW}🚀 Способ 2: Запуск нового контейнера в интерактивном режиме...${NC}"

# Пробуем с sudo (может быть есть)
if command -v sudo >/dev/null 2>&1; then
    echo -e "${YELLOW}Пробуем через sudo...${NC}"
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
else
    # Без sudo
    echo -e "${YELLOW}Пробуем без sudo...${NC}"
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
fi

# Если дошли сюда, значит контейнер запустился и мы внутри
# Теперь внутри контейнера выполни:
echo ""
echo -e "${GREEN}✅ Ты внутри Docker контейнера!${NC}"
echo ""
echo "Выполни следующие команды:"
echo "1. pip install -r requirements.txt"
echo "2. uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo ""
echo "Или запусти в фоне:"
echo "nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > /app/backend.log 2>&1 &"






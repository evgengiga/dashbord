#!/bin/bash
# Универсальный скрипт для запуска backend на Beget
# Пробует разные способы запуска

set -e

echo "🚀 Запуск Dashboard Backend..."

cd ~/dashboard.headcorn.pro/backend

# Цвета
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Проверка, что backend папка существует
if [ ! -d "." ]; then
    echo -e "${RED}❌ Папка backend не найдена!${NC}"
    exit 1
fi

# Способ 0: Проверить, может быть контейнер уже запущен
echo -e "${YELLOW}🔍 Проверка уже запущенных контейнеров...${NC}"
if docker ps >/dev/null 2>&1; then
    RUNNING_CONTAINER=$(docker ps --filter "name=dashboard-backend" --format "{{.Names}}" 2>/dev/null)
    if [ ! -z "$RUNNING_CONTAINER" ]; then
        echo -e "${GREEN}✅ Контейнер dashboard-backend уже запущен!${NC}"
        echo "Проверь: docker logs dashboard-backend"
        echo "Проверь порт: ss -tuln | grep 8001"
        exit 0
    fi
fi

# Способ 1: Попробовать через Docker (если есть права)
echo -e "${YELLOW}📦 Способ 1: Попытка запуска через Docker...${NC}"
if docker ps >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Docker доступен!${NC}"
    
    # Останови и удали старый контейнер
    docker stop dashboard-backend 2>/dev/null || true
    docker rm dashboard-backend 2>/dev/null || true
    
    # Запусти новый контейнер
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
      bash -c "pip install --no-cache-dir -r requirements.txt && uvicorn app.main:app --host 0.0.0.0 --port 8000" >/dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Backend запущен через Docker на порту 8001!${NC}"
        echo "Проверь: docker logs dashboard-backend"
        exit 0
    fi
else
    echo -e "${YELLOW}⚠️  Docker недоступен (нет прав или не установлен)${NC}"
    
    # Попробуем через docker-compose (может работать по-другому)
    echo -e "${YELLOW}🔍 Попытка через docker-compose...${NC}"
    if command -v docker-compose >/dev/null 2>&1; then
        cd ~/dashboard.headcorn.pro
        if [ -f "docker-compose.yml" ]; then
            docker-compose up -d backend 2>&1 | head -20
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✅ Backend запущен через docker-compose!${NC}"
                exit 0
            fi
        fi
    fi
fi

# Способ 2: Попробовать через системный Python 3
echo -e "${YELLOW}🐍 Способ 2: Поиск рабочего Python 3...${NC}"

# Ищем рабочий Python 3 - расширенный поиск
PYTHON_CMD=""

# Сначала проверяем через command -v (быстрее)
echo -e "${YELLOW}🔍 Поиск через PATH...${NC}"
for py in python3.10 python3.9 python3.8 python3.7 python3.6 python3.5 python3; do
    if command -v "$py" >/dev/null 2>&1; then
        # Проверяем, что Python работает (не выдает GLIBC ошибку)
        VERSION_OUTPUT=$("$py" --version 2>&1)
        EXIT_CODE=$?
        if [ $EXIT_CODE -eq 0 ] && ! echo "$VERSION_OUTPUT" | grep -qi "GLIBC"; then
            PYTHON_CMD=$py
            echo -e "${GREEN}✅ Найден рабочий Python: $PYTHON_CMD ($VERSION_OUTPUT)${NC}"
            break
        else
            echo -e "${YELLOW}⚠️  Python найден, но не работает: $py${NC}"
        fi
    fi
done

# Если не нашли, проверяем стандартные пути
if [ -z "$PYTHON_CMD" ]; then
    echo -e "${YELLOW}🔍 Поиск в стандартных путях...${NC}"
    PYTHON_PATHS=(
        "/usr/bin/python3.10" "/usr/bin/python3.9" "/usr/bin/python3.8" "/usr/bin/python3.7" "/usr/bin/python3.6" "/usr/bin/python3"
        "/usr/local/bin/python3.10" "/usr/local/bin/python3.9" "/usr/local/bin/python3.8" "/usr/local/bin/python3.7" "/usr/local/bin/python3.6" "/usr/local/bin/python3"
        "/opt/python3/bin/python3"
    )
    
    for py in "${PYTHON_PATHS[@]}"; do
        if [ -f "$py" ] && [ -x "$py" ]; then
            VERSION_OUTPUT=$("$py" --version 2>&1)
            EXIT_CODE=$?
            if [ $EXIT_CODE -eq 0 ] && ! echo "$VERSION_OUTPUT" | grep -qi "GLIBC"; then
                PYTHON_CMD=$py
                echo -e "${GREEN}✅ Найден рабочий Python: $PYTHON_CMD ($VERSION_OUTPUT)${NC}"
                break
            fi
        fi
    done
fi

# Если все еще не нашли, используем find (медленнее, но более тщательно)
if [ -z "$PYTHON_CMD" ]; then
    echo -e "${YELLOW}🔍 Расширенный поиск через find...${NC}"
    FOUND_PYTHON=$(find /usr/bin /usr/local/bin /opt -name "python3*" -type f 2>/dev/null | grep -v "python2" | head -10)
    
    for py in $FOUND_PYTHON; do
        if [ -x "$py" ]; then
            VERSION_OUTPUT=$("$py" --version 2>&1)
            EXIT_CODE=$?
            if [ $EXIT_CODE -eq 0 ] && ! echo "$VERSION_OUTPUT" | grep -qi "GLIBC"; then
                PYTHON_CMD=$py
                echo -e "${GREEN}✅ Найден рабочий Python: $PYTHON_CMD ($VERSION_OUTPUT)${NC}"
                break
            fi
        fi
    done
fi

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${RED}❌ Не найден рабочий Python 3${NC}"
    echo -e "${YELLOW}💡 Попробуй вручную найти Python:${NC}"
    echo "  find /usr -name 'python3*' -type f 2>/dev/null | head -10"
    echo "  which python3.8 python3.7 python3.6 python3"
    echo ""
    echo -e "${YELLOW}💡 Или попробуй запустить через Docker (если получишь права):${NC}"
    echo "  docker run -d --name dashboard-backend -p 8001:8000 ..."
    exit 1
fi

# Создаем или обновляем venv
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Создание виртуального окружения...${NC}"
    $PYTHON_CMD -m venv venv
else
    echo -e "${YELLOW}🔄 Обновление виртуального окружения...${NC}"
    rm -rf venv
    $PYTHON_CMD -m venv venv
fi

# Активируем venv
source venv/bin/activate

# Устанавливаем зависимости
echo -e "${YELLOW}📥 Установка зависимостей...${NC}"
pip install --upgrade pip >/dev/null 2>&1
pip install -r requirements.txt >/dev/null 2>&1

# Создаем .env файл (если нет)
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}📝 Создание .env файла...${NC}"
    cat > .env << EOF
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
EOF
fi

# Останавливаем старый процесс (если есть)
echo -e "${YELLOW}🛑 Остановка старого процесса...${NC}"
pkill -f "uvicorn app.main:app.*8001" 2>/dev/null || true
sleep 2

# Запускаем через nohup
echo -e "${YELLOW}🚀 Запуск backend на порту 8001...${NC}"
nohup uvicorn app.main:app --host 0.0.0.0 --port 8001 > backend.log 2>&1 &

# Ждем немного
sleep 3

# Проверяем, что запустилось
if ps aux | grep -v grep | grep "uvicorn app.main:app" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend запущен на порту 8001!${NC}"
    echo "Логи: tail -f backend.log"
    echo "Проверка: curl http://localhost:8001/api/health"
else
    echo -e "${RED}❌ Не удалось запустить backend${NC}"
    echo "Проверь логи: cat backend.log"
    exit 1
fi


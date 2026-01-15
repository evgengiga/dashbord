#!/bin/bash
# Скрипт для создания systemd сервиса для backend

set -e

echo "🔧 Создание systemd сервиса для Dashboard Backend..."

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Проверка прав root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Запустите скрипт с sudo${NC}"
    exit 1
fi

# Запрос пути к проекту
read -p "Введите полный путь к проекту (например: /home/dashboard/projects/dashbord): " PROJECT_PATH

if [ ! -d "$PROJECT_PATH" ]; then
    echo -e "${RED}❌ Директория не найдена: $PROJECT_PATH${NC}"
    exit 1
fi

if [ ! -d "$PROJECT_PATH/backend" ]; then
    echo -e "${RED}❌ Директория backend не найдена: $PROJECT_PATH/backend${NC}"
    exit 1
fi

# Запрос пользователя
read -p "Введите имя пользователя для запуска сервиса (например: dashboard): " SERVICE_USER

if ! id "$SERVICE_USER" &>/dev/null; then
    echo -e "${YELLOW}⚠️  Пользователь $SERVICE_USER не найден. Создать? (y/n)${NC}"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        adduser "$SERVICE_USER"
    else
        echo -e "${RED}❌ Пользователь должен существовать${NC}"
        exit 1
    fi
fi

# Создание файла сервиса
SERVICE_FILE="/etc/systemd/system/dashboard-backend.service"

cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Dashboard Backend Service
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$PROJECT_PATH/backend
Environment="PATH=$PROJECT_PATH/backend/venv/bin"
ExecStart=$PROJECT_PATH/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✅ Файл сервиса создан: $SERVICE_FILE${NC}"

# Перезагрузка systemd
systemctl daemon-reload

# Включение автозапуска
systemctl enable dashboard-backend

echo -e "${GREEN}✅ Сервис создан и включен!${NC}"
echo ""
echo "Управление сервисом:"
echo "  sudo systemctl start dashboard-backend    # Запустить"
echo "  sudo systemctl stop dashboard-backend     # Остановить"
echo "  sudo systemctl restart dashboard-backend  # Перезапустить"
echo "  sudo systemctl status dashboard-backend   # Статус"
echo "  sudo journalctl -u dashboard-backend -f   # Логи"








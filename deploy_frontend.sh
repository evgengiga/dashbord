#!/bin/bash
# Скрипт для автоматической сборки frontend

set -e

echo "🚀 Сборка Dashboard Frontend..."

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Проверка, что скрипт запущен из правильной директории
if [ ! -f "frontend/package.json" ]; then
    echo "❌ Ошибка: Запустите скрипт из корневой директории проекта"
    exit 1
fi

cd frontend

# Проверка наличия .env.production
if [ ! -f ".env.production" ]; then
    echo -e "${YELLOW}⚠️  Файл .env.production не найден.${NC}"
    read -p "Введите URL вашего backend API (например: https://dashboard.yourdomain.com/api): " API_URL
    
    if [ -z "$API_URL" ]; then
        echo "❌ URL не может быть пустым"
        exit 1
    fi
    
    echo "VITE_API_URL=$API_URL" > .env.production
    echo -e "${GREEN}✅ Создан файл .env.production${NC}"
else
    echo -e "${GREEN}✅ Файл .env.production найден${NC}"
fi

# Установка зависимостей
echo -e "${YELLOW}📥 Установка зависимостей...${NC}"
npm install

# Сборка проекта
echo -e "${YELLOW}🔨 Сборка проекта...${NC}"
npm run build

echo -e "${GREEN}✅ Frontend собран!${NC}"
echo ""
echo "Собранные файлы находятся в папке: frontend/dist/"
echo ""
echo "Следующие шаги:"
echo "1. Скопируйте файлы в /var/www/dashboard/:"
echo "   sudo cp -r dist/* /var/www/dashboard/"
echo "   sudo chown -R www-data:www-data /var/www/dashboard"
echo "2. Настройте Nginx (см. DEPLOY_OWN_SERVER.md)"


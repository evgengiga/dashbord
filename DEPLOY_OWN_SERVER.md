# 🖥️ Развертывание на собственном сервере (Beget/VPS)

## 📋 Что нужно перед началом

1. ✅ **VPS сервер** с доступом по SSH (Beget, Timeweb, или любой другой)
2. ✅ **Домен** (например: `dashboard.yourdomain.com`)
3. ✅ **Доступ по SSH** к серверу
4. ✅ **Root доступ** или sudo права

---

## 🎯 Шаг 1: Подготовка сервера

### 1.1. Подключитесь к серверу по SSH

```bash
ssh root@ваш-сервер-ip
# или
ssh ваш-пользователь@ваш-сервер-ip
```

### 1.2. Обновите систему (Ubuntu/Debian)

```bash
sudo apt update
sudo apt upgrade -y
```

### 1.3. Установите необходимые пакеты

```bash
# Python 3.11+ и pip
sudo apt install -y python3 python3-pip python3-venv

# Node.js 18+ и npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Nginx (веб-сервер)
sudo apt install -y nginx

# Git
sudo apt install -y git

# PostgreSQL клиент (для проверки подключения)
sudo apt install -y postgresql-client

# Дополнительные инструменты
sudo apt install -y build-essential
```

### 1.4. Проверьте установку

```bash
python3 --version  # Должно быть 3.11+
node --version      # Должно быть 18+
nginx -v            # Должна быть установлена
```

---

## 🎯 Шаг 2: Создание пользователя для приложения (опционально, но рекомендуется)

```bash
# Создайте пользователя
sudo adduser dashboard
sudo usermod -aG sudo dashboard

# Переключитесь на нового пользователя
su - dashboard
```

---

## 🎯 Шаг 3: Клонирование репозитория

### 3.1. Создайте директорию для проекта

```bash
mkdir -p ~/projects
cd ~/projects
```

### 3.2. Клонируйте репозиторий

```bash
git clone https://github.com/evgengiga/dashbord.git
cd dashbord
```

---

## 🎯 Шаг 4: Настройка Backend

### 4.1. Перейдите в директорию backend

```bash
cd ~/projects/dashbord/backend
```

### 4.2. Создайте виртуальное окружение Python

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4.3. Установите зависимости

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4.4. Создайте файл с переменными окружения

```bash
nano .env
```

Вставьте следующее содержимое (замените значения на свои):

```env
# PostgreSQL Database
DB_HOST=pg4.sweb.ru
DB_PORT=5433
DB_USER=headcorne_test
DB_PASSWORD=Ss8SRGP5TH3W6J@L
DB_NAME=headcorne_test

# Planfix REST API
PLANFIX_API_URL=https://megamindru.planfix.ru/rest/
PLANFIX_API_TOKEN=3325457cab2f1a9b69b3c9191eeadc82

# Security (ВАЖНО: Измените SECRET_KEY!)
SECRET_KEY=ваш-случайный-секретный-ключ-минимум-32-символа-измените-это
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Application
APP_NAME=Dashboard Service
DEBUG=False

# CORS (замените на ваш домен)
CORS_ORIGINS=https://dashboard.yourdomain.com,https://www.dashboard.yourdomain.com
```

**Сохраните:** `Ctrl+O`, `Enter`, `Ctrl+X`

**⚠️ ВАЖНО:** Замените `SECRET_KEY` на случайную строку (минимум 32 символа)!

### 4.5. Примените миграции базы данных

```bash
# Подключитесь к БД и выполните миграцию
psql -h pg4.sweb.ru -p 5433 -U headcorne_test -d headcorne_test -f migrations/001_create_users_table.sql
```

Или используйте Python скрипт:

```bash
python3 apply_migration.py
```

### 4.6. Протестируйте запуск backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Если все работает, остановите сервер: `Ctrl+C`

---

## 🎯 Шаг 5: Создание systemd сервиса для Backend

### 5.1. Создайте файл сервиса

```bash
sudo nano /etc/systemd/system/dashboard-backend.service
```

Вставьте следующее содержимое (замените пути на свои):

```ini
[Unit]
Description=Dashboard Backend Service
After=network.target

[Service]
Type=simple
User=dashboard
Group=dashboard
WorkingDirectory=/home/dashboard/projects/dashbord/backend
Environment="PATH=/home/dashboard/projects/dashbord/backend/venv/bin"
ExecStart=/home/dashboard/projects/dashbord/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**⚠️ ВАЖНО:** Замените `/home/dashboard` на путь к вашему пользователю!

**Сохраните:** `Ctrl+O`, `Enter`, `Ctrl+X`

### 5.2. Запустите сервис

```bash
sudo systemctl daemon-reload
sudo systemctl enable dashboard-backend
sudo systemctl start dashboard-backend
sudo systemctl status dashboard-backend
```

Проверьте, что сервис работает (должно быть `active (running)`).

### 5.3. Проверьте логи (если нужно)

```bash
sudo journalctl -u dashboard-backend -f
```

---

## 🎯 Шаг 6: Настройка Frontend

### 6.1. Перейдите в директорию frontend

```bash
cd ~/projects/dashbord/frontend
```

### 6.2. Создайте файл с переменными окружения

```bash
nano .env.production
```

Вставьте (замените на ваш домен):

```env
VITE_API_URL=https://dashboard.yourdomain.com/api
```

**Сохраните:** `Ctrl+O`, `Enter`, `Ctrl+X`

### 6.3. Установите зависимости и соберите проект

```bash
npm install
npm run build
```

После сборки файлы будут в папке `dist/`.

### 6.4. Скопируйте собранные файлы в директорию для nginx

```bash
sudo mkdir -p /var/www/dashboard
sudo cp -r dist/* /var/www/dashboard/
sudo chown -R www-data:www-data /var/www/dashboard
```

---

## 🎯 Шаг 7: Настройка Nginx

### 7.1. Создайте конфигурацию Nginx

```bash
sudo nano /etc/nginx/sites-available/dashboard
```

Вставьте следующее содержимое (замените `dashboard.yourdomain.com` на ваш домен):

```nginx
# Редирект с HTTP на HTTPS
server {
    listen 80;
    server_name dashboard.yourdomain.com www.dashboard.yourdomain.com;
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# Основной сервер (HTTPS)
server {
    listen 443 ssl http2;
    server_name dashboard.yourdomain.com www.dashboard.yourdomain.com;

    # SSL сертификаты (будем настраивать в следующем шаге)
    ssl_certificate /etc/letsencrypt/live/dashboard.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dashboard.yourdomain.com/privkey.pem;
    
    # SSL настройки
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Логи
    access_log /var/log/nginx/dashboard-access.log;
    error_log /var/log/nginx/dashboard-error.log;

    # Frontend (статичные файлы)
    root /var/www/dashboard;
    index index.html;

    # Проксирование API запросов на backend
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Статичные файлы frontend
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Кэширование статики
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**Сохраните:** `Ctrl+O`, `Enter`, `Ctrl+X`

### 7.2. Активируйте конфигурацию

```bash
sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/
sudo nginx -t  # Проверка конфигурации
```

Если проверка прошла успешно, перезапустите nginx:

```bash
sudo systemctl restart nginx
```

---

## 🎯 Шаг 8: Настройка SSL сертификата (Let's Encrypt)

### 8.1. Установите Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 8.2. Получите SSL сертификат

```bash
sudo certbot --nginx -d dashboard.yourdomain.com -d www.dashboard.yourdomain.com
```

Следуйте инструкциям:
- Введите email
- Согласитесь с условиями
- Выберите, перенаправлять ли HTTP на HTTPS (рекомендуется: 2)

### 8.3. Проверьте автообновление сертификата

```bash
sudo certbot renew --dry-run
```

Certbot автоматически обновит сертификаты перед истечением.

---

## 🎯 Шаг 9: Настройка DNS

### 9.1. Настройте A-запись в DNS вашего домена

В панели управления доменом (Beget или где вы покупали домен):

1. Найдите настройки DNS
2. Добавьте A-запись:
   - **Имя:** `dashboard` (или `@` для корневого домена)
   - **Тип:** `A`
   - **Значение:** IP адрес вашего сервера
   - **TTL:** `3600` (или по умолчанию)

3. Опционально, добавьте CNAME для www:
   - **Имя:** `www`
   - **Тип:** `CNAME`
   - **Значение:** `dashboard.yourdomain.com`

### 9.2. Дождитесь распространения DNS (5-60 минут)

Проверьте DNS:

```bash
nslookup dashboard.yourdomain.com
```

---

## 🎯 Шаг 10: Финальная проверка

### 10.1. Проверьте backend

```bash
curl http://127.0.0.1:8000/api/health
```

Должен вернуться JSON с `"status": "healthy"`.

### 10.2. Проверьте frontend

Откройте в браузере: `https://dashboard.yourdomain.com`

Должна открыться страница входа.

### 10.3. Проверьте API

Откройте: `https://dashboard.yourdomain.com/api/docs`

Должна открыться документация Swagger.

---

## 🔄 Обновление приложения

### Когда нужно обновить код:

```bash
cd ~/projects/dashbord
git pull origin main

# Обновить backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart dashboard-backend

# Обновить frontend
cd ../frontend
npm install
npm run build
sudo cp -r dist/* /var/www/dashboard/
sudo chown -R www-data:www-data /var/www/dashboard
```

---

## 🔧 Полезные команды

### Управление backend сервисом

```bash
# Статус
sudo systemctl status dashboard-backend

# Остановить
sudo systemctl stop dashboard-backend

# Запустить
sudo systemctl start dashboard-backend

# Перезапустить
sudo systemctl restart dashboard-backend

# Логи
sudo journalctl -u dashboard-backend -f
```

### Управление Nginx

```bash
# Перезапустить
sudo systemctl restart nginx

# Проверить конфигурацию
sudo nginx -t

# Логи
sudo tail -f /var/log/nginx/dashboard-error.log
```

---

## ⚠️ Безопасность

### 1. Настройте Firewall

```bash
# Установите UFW (если еще не установлен)
sudo apt install -y ufw

# Разрешите SSH
sudo ufw allow 22/tcp

# Разрешите HTTP и HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Включите firewall
sudo ufw enable
```

### 2. Регулярно обновляйте систему

```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Не храните секреты в Git

Убедитесь, что файл `.env` в `.gitignore`.

---

## 🆘 Решение проблем

### ❌ Backend не запускается

```bash
# Проверьте логи
sudo journalctl -u dashboard-backend -n 50

# Проверьте, что порт 8000 свободен
sudo netstat -tulpn | grep 8000

# Проверьте переменные окружения
cd ~/projects/dashbord/backend
source venv/bin/activate
python3 -c "from app.core.config import settings; print(settings.DB_HOST)"
```

### ❌ Nginx не работает

```bash
# Проверьте конфигурацию
sudo nginx -t

# Проверьте логи
sudo tail -f /var/log/nginx/error.log

# Проверьте, что nginx запущен
sudo systemctl status nginx
```

### ❌ SSL сертификат не работает

```bash
# Проверьте сертификат
sudo certbot certificates

# Обновите вручную
sudo certbot renew
```

### ❌ CORS ошибки

Убедитесь, что в `.env` backend указан правильный домен:

```env
CORS_ORIGINS=https://dashboard.yourdomain.com
```

И перезапустите backend:

```bash
sudo systemctl restart dashboard-backend
```

---

## 📝 Примечания для Beget

Если вы используете Beget:

1. **Панель управления:** Используйте панель Beget для управления доменами и DNS
2. **SSH доступ:** Обычно предоставляется по умолчанию
3. **Python/Node.js:** Могут быть уже установлены, проверьте версии
4. **Nginx:** Может быть уже установлен и настроен
5. **Порты:** Убедитесь, что порты 80 и 443 открыты

---

## 🎉 Готово!

Теперь ваш дашборд доступен по адресу: `https://dashboard.yourdomain.com`

---

**Последнее обновление:** 2025-01-XX


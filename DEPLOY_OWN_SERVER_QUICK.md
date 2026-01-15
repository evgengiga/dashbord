# ⚡ Быстрая шпаргалка: Деплой на свой сервер

## 🎯 Минимальные шаги

### 1. Подготовка сервера

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nodejs npm nginx git
```

### 2. Клонирование проекта

```bash
cd ~
git clone https://github.com/evgengiga/dashbord.git
cd dashbord
```

### 3. Настройка Backend

```bash
chmod +x deploy_backend.sh
./deploy_backend.sh
```

Создайте `.env` в `backend/`:
```env
DB_HOST=pg4.sweb.ru
DB_PORT=5433
DB_USER=headcorne_test
DB_PASSWORD=Ss8SRGP5TH3W6J@L
DB_NAME=headcorne_test
PLANFIX_API_URL=https://megamindru.planfix.ru/rest/
PLANFIX_API_TOKEN=3325457cab2f1a9b69b3c9191eeadc82
SECRET_KEY=ваш-случайный-ключ-32-символа
DEBUG=False
CORS_ORIGINS=https://ваш-домен.com
```

### 4. Создание systemd сервиса

```bash
chmod +x create_systemd_service.sh
sudo ./create_systemd_service.sh
sudo systemctl start dashboard-backend
```

### 5. Сборка Frontend

```bash
chmod +x deploy_frontend.sh
./deploy_frontend.sh
sudo cp -r frontend/dist/* /var/www/dashboard/
sudo chown -R www-data:www-data /var/www/dashboard
```

### 6. Настройка Nginx

Создайте `/etc/nginx/sites-available/dashboard` (см. `DEPLOY_OWN_SERVER.md`)

```bash
sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. SSL сертификат

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d ваш-домен.com
```

---

## 📝 Важные файлы

- **Полная инструкция:** `DEPLOY_OWN_SERVER.md`
- **Backend скрипт:** `deploy_backend.sh`
- **Frontend скрипт:** `deploy_frontend.sh`
- **Systemd скрипт:** `create_systemd_service.sh`

---

## 🔗 Полезные команды

```bash
# Backend
sudo systemctl status dashboard-backend
sudo journalctl -u dashboard-backend -f

# Nginx
sudo nginx -t
sudo systemctl restart nginx
sudo tail -f /var/log/nginx/dashboard-error.log
```

---

**Полная инструкция:** `DEPLOY_OWN_SERVER.md`








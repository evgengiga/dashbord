# 🚀 Запуск Backend на порту 8002 (как вчера)

## Быстрый запуск

**Внутри Docker окружения выполни:**

```bash
cd ~/dashboard.headcorn.pro/backend

# 1. Убей все процессы uvicorn (на всякий случай)
pkill -f uvicorn

# 2. Подожди немного
sleep 2

# 3. Активируй venv
source venv/bin/activate

# 4. Запусти на порту 8002
nohup uvicorn app.main:app --host 0.0.0.0 --port 8002 > backend.log 2>&1 &

# 5. Проверь
sleep 3
ps aux | grep uvicorn | grep -v grep
ss -tuln | grep 8002
curl http://127.0.0.1:8002/api/health
```

---

## Проверка работы

**Выполни:**

```bash
# Проверь процесс
ps aux | grep uvicorn | grep -v grep

# Проверь порт
ss -tuln | grep 8002

# Проверь health endpoint
curl http://127.0.0.1:8002/api/health

# Или через внешний адрес
curl http://dashboard.headcorn.pro/api/health
```

---

## Если нужно обновить .htaccess

**Если backend работает на 8002, но сайт не открывается, нужно обновить `.htaccess` на сервере.**

**Проверь файл `.htaccess` в `public_html`:**

```bash
# Выйди из Docker окружения
exit

# Проверь .htaccess
cat ~/dashboard.headcorn.pro/public_html/.htaccess | grep 800
```

**Если там указан порт 8001, нужно изменить на 8002.**

---

## Логи

**Просмотр логов:**

```bash
# Внутри Docker окружения
cd ~/dashboard.headcorn.pro/backend
tail -f backend.log
```





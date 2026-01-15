#!/bin/bash
# Диагностический скрипт для понимания состояния сервера

echo "🔍 ДИАГНОСТИКА СЕРВЕРА"
echo "===================="
echo ""

# 1. Проверка Docker
echo "1️⃣ ПРОВЕРКА DOCKER:"
echo "-------------------"
if command -v docker >/dev/null 2>&1; then
    echo "✅ Docker установлен: $(docker --version 2>&1)"
    echo ""
    echo "Проверка прав:"
    docker ps 2>&1 | head -3
    echo ""
    echo "Проверка контейнеров:"
    docker ps -a 2>&1 | grep -E "(dashboard|CONTAINER)" | head -5
else
    echo "❌ Docker не установлен"
fi
echo ""

# 2. Проверка Python
echo "2️⃣ ПРОВЕРКА PYTHON:"
echo "-------------------"
echo "Поиск Python в PATH:"
for py in python3.11 python3.10 python3.9 python3.8 python3.7 python3.6 python3 python; do
    if command -v $py >/dev/null 2>&1; then
        VERSION=$($py --version 2>&1)
        if echo "$VERSION" | grep -qi "GLIBC"; then
            echo "⚠️  $py: $VERSION (GLIBC ошибка)"
        else
            echo "✅ $py: $VERSION"
        fi
    fi
done
echo ""

echo "Поиск Python в стандартных путях:"
for path in /usr/bin/python3 /usr/local/bin/python3 /opt/python3/bin/python3; do
    if [ -f "$path" ]; then
        VERSION=$($path --version 2>&1)
        if echo "$VERSION" | grep -qi "GLIBC"; then
            echo "⚠️  $path: $VERSION (GLIBC ошибка)"
        else
            echo "✅ $path: $VERSION"
        fi
    fi
done
echo ""

# 3. Проверка портов
echo "3️⃣ ПРОВЕРКА ПОРТОВ:"
echo "-------------------"
echo "Порт 8000:"
ss -tuln | grep ":8000" || echo "  Свободен"
echo ""
echo "Порт 8001:"
ss -tuln | grep ":8001" || echo "  Свободен"
echo ""

# 4. Проверка процессов
echo "4️⃣ ПРОВЕРКА ПРОЦЕССОВ:"
echo "----------------------"
echo "Python процессы:"
ps aux | grep -E "python|uvicorn" | grep -v grep | head -5 || echo "  Нет запущенных процессов"
echo ""

# 5. Проверка venv
echo "5️⃣ ПРОВЕРКА VENV:"
echo "-----------------"
if [ -d "~/dashboard.headcorn.pro/backend/venv" ]; then
    echo "✅ venv существует"
    echo "Python в venv:"
    ~/dashboard.headcorn.pro/backend/venv/bin/python3 --version 2>&1 | head -1
else
    echo "❌ venv не найден"
fi
echo ""

# 6. История команд
echo "6️⃣ ПОСЛЕДНИЕ КОМАНДЫ С DOCKER/8001:"
echo "------------------------------------"
history | grep -E "(docker|8001|uvicorn)" | tail -5
echo ""

# 7. Рекомендации
echo "💡 РЕКОМЕНДАЦИИ:"
echo "----------------"
if ! docker ps >/dev/null 2>&1; then
    echo "❌ Docker недоступен - нужны права или другой способ запуска"
fi

PYTHON_FOUND=$(command -v python3.8 python3.7 python3.6 python3 2>/dev/null | head -1)
if [ -z "$PYTHON_FOUND" ]; then
    echo "❌ Python 3 не найден - нужно установить или использовать Docker"
else
    echo "✅ Найден Python: $PYTHON_FOUND"
fi

echo ""
echo "📋 СЛЕДУЮЩИЕ ШАГИ:"
echo "1. Если Docker недоступен - обратись в поддержку Beget или используй панель управления"
echo "2. Если Python не найден - используй Docker или установи Python 3"
echo "3. Если все есть, но не работает - проверь логи: docker logs dashboard-backend"






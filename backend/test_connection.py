"""
Скрипт для проверки подключений к PostgreSQL и Planfix API
"""
import sys
import asyncio

print("=" * 50)
print("Тест подключений")
print("=" * 50)

# Тест PostgreSQL
print("\n1. Проверка подключения к PostgreSQL...")
try:
    from app.core.database import test_connection
    if test_connection():
        print("✅ PostgreSQL: Подключение успешно!")
    else:
        print("❌ PostgreSQL: Ошибка подключения")
except Exception as e:
    print(f"❌ PostgreSQL: Ошибка - {e}")

# Тест Planfix API
print("\n2. Проверка Planfix API...")
try:
    from app.services.planfix_service import planfix_service
    
    async def test_planfix():
        # Пробуем получить пользователя
        user = await planfix_service.get_user_by_email("gurujo@megamindru.planfix.ru")
        if user:
            print(f"✅ Planfix API: Работает!")
            print(f"   Найден пользователь: {user.get('full_name', 'Неизвестно')}")
            return True
        else:
            print("⚠️ Planfix API: Работает, но пользователь не найден")
            print("   Попробуйте другой email")
            return False
    
    result = asyncio.run(test_planfix())
    
except Exception as e:
    print(f"❌ Planfix API: Ошибка - {e}")

print("\n" + "=" * 50)
print("Тест завершен")
print("=" * 50)




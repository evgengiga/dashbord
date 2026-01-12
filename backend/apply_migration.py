"""
Скрипт для применения миграции через Python
"""
import psycopg2
from pathlib import Path

# Параметры подключения
DB_CONFIG = {
    'host': 'pg4.sweb.ru',
    'port': 5433,
    'database': 'headcorne_test',
    'user': 'headcorne_test',
    'password': 'Ss8SRGP5TH3W6J@L'
}

def apply_migration():
    """Применяет миграцию из файла"""
    # Читаем SQL файл
    migration_file = Path(__file__).parent / 'migrations' / '001_create_users_table.sql'
    
    with open(migration_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # Подключаемся к БД
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("✅ Подключение к БД успешно!")
        
        # Выполняем SQL
        cursor.execute(sql_script)
        conn.commit()
        
        print("✅ Миграция применена успешно!")
        
        # Проверяем что таблица создана
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'users'
            );
        """)
        
        if cursor.fetchone()[0]:
            print("✅ Таблица 'users' создана!")
        else:
            print("❌ Таблица 'users' не найдена!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        if conn:
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    apply_migration()


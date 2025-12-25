"""
Подключение к базе данных
"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Создаем engine для подключения к PostgreSQL
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    echo=settings.DEBUG,  # Логирование SQL запросов в debug режиме
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


def get_db():
    """
    Dependency для получения сессии базы данных
    Использование: def endpoint(db: Session = Depends(get_db))
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def execute_query(query: str, params: dict = None):
    """
    Выполняет SQL запрос и возвращает результаты
    
    Args:
        query: SQL запрос
        params: Параметры для запроса (опционально)
        
    Returns:
        Список словарей с результатами
    """
    db = SessionLocal()
    try:
        result = db.execute(text(query), params or {})
        
        # Преобразуем результат в список словарей
        columns = result.keys()
        rows = result.fetchall()
        
        return [dict(zip(columns, row)) for row in rows]
    finally:
        db.close()


def test_connection() -> bool:
    """
    Проверяет подключение к базе данных
    
    Returns:
        True если подключение успешно, False иначе
    """
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False



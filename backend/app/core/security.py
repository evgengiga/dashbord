"""
Безопасность и аутентификация
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
import bcrypt
from .config import settings

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет пароль используя bcrypt напрямую
    
    Args:
        plain_password: Обычный пароль
        hashed_password: Хешированный пароль
        
    Returns:
        True если пароль верный, False иначе
    """
    # Обрезаем пароль до 72 байт перед проверкой
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Используем bcrypt напрямую
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def get_password_hash(password: str) -> str:
    """
    Хеширует пароль используя bcrypt напрямую (обход passlib для избежания проблем с длиной)
    
    Args:
        password: Обычный пароль (должен быть <= 72 байта)
        
    Returns:
        Хешированный пароль в формате bcrypt
    """
    # Bcrypt ограничение - 72 байта, обрезаем если нужно
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Обрезаем до 72 байт
        password_bytes = password_bytes[:72]
        print(f"⚠️ Password truncated to 72 bytes in get_password_hash")
    
    # Используем bcrypt напрямую, обходя passlib
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Возвращаем как строку (bcrypt возвращает bytes)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создает JWT токен
    
    Args:
        data: Данные для кодирования в токен
        expires_delta: Время жизни токена
        
    Returns:
        Закодированный JWT токен
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Декодирует JWT токен
    
    Args:
        token: JWT токен
        
    Returns:
        Декодированные данные из токена
        
    Raises:
        HTTPException: Если токен невалидный
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception





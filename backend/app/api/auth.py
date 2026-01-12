"""
API endpoints для аутентификации
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import timedelta
from sqlalchemy.orm import Session

from ..models.schemas import LoginRequest, LoginResponse, RegisterRequest, UserInfo
from ..models.user import User
from ..services.planfix_service import planfix_service
from ..core.security import create_access_token, decode_access_token, verify_password, get_password_hash
from ..core.database import get_db
from ..core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Вход по email и паролю
    
    1. Проверяет существует ли пользователь в БД
    2. Если нет - проверяет в Planfix и возвращает first_login=true
    3. Если есть - проверяет пароль и возвращает токен
    """
    # Проверяем существует ли пользователь в БД
    db_user = db.query(User).filter(User.email == request.email).first()
    
    if not db_user:
        # Пользователя нет в БД - проверяем в Planfix
        user_data = await planfix_service.get_user_by_email(request.email)
        
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с email {request.email} не найден в Planfix"
            )
        
        # Пользователь есть в Planfix, но нет в БД - это первый вход
        return LoginResponse(
            access_token="",  # Пустой токен, нужно зарегистрироваться
            token_type="bearer",
            user_name=planfix_service.get_user_full_name(user_data),
            user_email=request.email,
            first_login=True
        )
    
    # Пользователь есть в БД - проверяем пароль
    if not verify_password(request.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный пароль"
        )
    
    # Пароль верный - создаем токен
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": request.email,
            "full_name": db_user.full_name,
            "planfix_id": None  # Можно добавить если нужно
        },
        expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_name=db_user.full_name,
        user_email=request.email,
        first_login=False
    )


@router.post("/register", response_model=LoginResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Регистрация (первый вход) - установка пароля
    
    1. Проверяет что пользователь есть в Planfix
    2. Проверяет что пароли совпадают
    3. Создает запись в БД с хешем пароля
    4. Возвращает токен
    """
    # Проверяем совпадение паролей
    if request.password != request.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароли не совпадают"
        )
    
    # Проверяем минимальную длину пароля
    if len(request.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароль должен содержать минимум 6 символов"
        )
    
    # Проверяем максимальную длину пароля (bcrypt ограничение - 72 байта)
    # Для безопасности обрезаем до 72 символов (1 символ = 1 байт для ASCII)
    if len(request.password.encode('utf-8')) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароль не может быть длиннее 72 символов"
        )
    
    # Проверяем что пользователь есть в Planfix
    user_data = await planfix_service.get_user_by_email(request.email)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с email {request.email} не найден в Planfix"
        )
    
    # Проверяем что пользователь еще не зарегистрирован
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь уже зарегистрирован. Используйте вход."
        )
    
    # Получаем ФИО из Planfix
    full_name = planfix_service.get_user_full_name(user_data)
    
    # Обрезаем пароль до 72 байт (ограничение bcrypt)
    password_bytes = request.password.encode('utf-8')
    if len(password_bytes) > 72:
        password_to_hash = password_bytes[:72].decode('utf-8', errors='ignore')
    else:
        password_to_hash = request.password
    
    # Создаем пользователя в БД
    password_hash = get_password_hash(password_to_hash)
    db_user = User(
        email=request.email,
        password_hash=password_hash,
        full_name=full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Создаем токен
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": request.email,
            "full_name": full_name,
            "planfix_id": user_data.get("id")
        },
        expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_name=full_name,
        user_email=request.email,
        first_login=False
    )


@router.get("/me", response_model=UserInfo)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Получает информацию о текущем пользователе из токена
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    return UserInfo(
        email=payload.get("sub"),
        full_name=payload.get("full_name"),
        planfix_id=payload.get("planfix_id")
    )


def get_current_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Dependency для получения текущего пользователя из токена
    Используется в других endpoints
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    return payload



"""
API endpoints для аутентификации
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import timedelta

from ..models.schemas import LoginRequest, LoginResponse, UserInfo
from ..services.planfix_service import planfix_service
from ..core.security import create_access_token, decode_access_token
from ..core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Вход по email
    
    1. Получает email от пользователя
    2. Запрашивает данные из Planfix API
    3. Возвращает JWT токен и информацию о пользователе
    """
    # Получаем данные пользователя из Planfix
    user_data = await planfix_service.get_user_by_email(request.email)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с email {request.email} не найден в Planfix"
        )
    
    # Формируем полное ФИО
    full_name = planfix_service.get_user_full_name(user_data)
    
    # Создаем JWT токен
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
        user_email=request.email
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



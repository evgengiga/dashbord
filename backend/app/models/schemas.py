"""
Pydantic схемы для валидации данных
"""
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any, Optional


class LoginRequest(BaseModel):
    """Запрос на вход"""
    email: EmailStr


class LoginResponse(BaseModel):
    """Ответ после успешного входа"""
    access_token: str
    token_type: str = "bearer"
    user_name: str
    user_email: str


class UserInfo(BaseModel):
    """Информация о пользователе"""
    email: str
    full_name: str
    planfix_id: Optional[int] = None


class DashboardItem(BaseModel):
    """Элемент дашборда (таблица с данными)"""
    id: str
    title: str
    description: Optional[str] = None
    data: List[Dict[str, Any]]
    columns: List[str]
    details: Optional[List[Dict[str, Any]]] = None  # Для детализации (например, список задач)


class DashboardResponse(BaseModel):
    """Ответ с данными дашборда"""
    user_name: str
    items: List[DashboardItem]


class ErrorResponse(BaseModel):
    """Ответ с ошибкой"""
    detail: str



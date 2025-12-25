"""
API endpoints для дашбордов
"""
from fastapi import APIRouter, Depends
from typing import List

from ..models.schemas import DashboardResponse, DashboardItem
from ..services.dashboard_service import dashboard_service
from .auth import get_current_user_from_token

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", response_model=DashboardResponse)
async def get_dashboard(
    fiscal_year: str = "current",  # "current" или "previous"
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Получает данные дашборда для текущего пользователя
    
    Args:
        fiscal_year: "current" для текущего финансового года, "previous" для прошлого
        
    Все SQL-запросы автоматически фильтруются по ФИО пользователя
    """
    user_full_name = current_user.get("full_name")
    
    # Получаем данные дашборда
    dashboard_items = dashboard_service.get_dashboard_data(user_full_name, fiscal_year)
    
    return DashboardResponse(
        user_name=user_full_name,
        items=dashboard_items
    )


@router.get("/items", response_model=List[DashboardItem])
async def get_dashboard_items(
    fiscal_year: str = "current",
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Получает только элементы дашборда (без обертки)
    """
    user_full_name = current_user.get("full_name")
    dashboard_items = dashboard_service.get_dashboard_data(user_full_name, fiscal_year)
    return dashboard_items


@router.post("/query")
async def execute_custom_query(
    query: str,
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Выполняет пользовательский SQL-запрос с автоматической фильтрацией
    
    ВНИМАНИЕ: Этот endpoint предназначен для разработки.
    В production рекомендуется отключить или ограничить доступ.
    """
    user_full_name = current_user.get("full_name")
    result = dashboard_service.execute_custom_query(query, user_full_name)
    
    return {
        "user": user_full_name,
        "data": result,
        "columns": list(result[0].keys()) if result else []
    }



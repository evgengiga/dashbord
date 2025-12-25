"""
Сервис для работы с Planfix API
"""
import httpx
from typing import Optional, Dict
from ..core.config import settings


class PlanfixService:
    """Сервис для взаимодействия с Planfix REST API"""
    
    def __init__(self):
        self.base_url = settings.PLANFIX_API_URL
        self.token = settings.PLANFIX_API_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        """
        Получает информацию о пользователе из Planfix по email
        
        Args:
            email: Email пользователя
            
        Returns:
            Словарь с данными пользователя или None если не найден
        """
        try:
            async with httpx.AsyncClient() as client:
                # Запрос на получение пользователя по email
                response = await client.post(
                    f"{self.base_url}user/list",
                    headers=self.headers,
                    json={
                        "filters": [
                            {
                                "type": 1,  # email filter
                                "operator": "equal",
                                "value": email
                            }
                        ]
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Проверяем, что пользователь найден
                    if data.get("users") and len(data["users"]) > 0:
                        user = data["users"][0]
                        return {
                            "id": user.get("id"),
                            "email": user.get("email"),
                            "full_name": user.get("name"),
                            "last_name": user.get("lastName", ""),
                            "first_name": user.get("firstName", ""),
                            "middle_name": user.get("middleName", ""),
                        }
                
                return None
                
        except Exception as e:
            print(f"Planfix API error: {e}")
            return None
    
    def get_user_full_name(self, user_data: Dict) -> str:
        """
        Формирует полное ФИО пользователя из данных Planfix
        
        Args:
            user_data: Данные пользователя из Planfix
            
        Returns:
            Полное ФИО пользователя
        """
        # Пробуем сначала получить готовое полное имя
        if user_data.get("full_name"):
            return user_data["full_name"]
        
        # Или собираем из компонентов
        parts = []
        if user_data.get("last_name"):
            parts.append(user_data["last_name"])
        if user_data.get("first_name"):
            parts.append(user_data["first_name"])
        if user_data.get("middle_name"):
            parts.append(user_data["middle_name"])
        
        return " ".join(parts) if parts else "Unknown User"


# Создаем singleton экземпляр сервиса
planfix_service = PlanfixService()



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
            "Authorization": self.token,  # Planfix не использует Bearer
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
                # Согласно документации Planfix REST API
                response = await client.post(
                    f"{self.base_url}contact/list",
                    headers=self.headers,
                    json={
                        "email": email
                    },
                    timeout=10.0
                )
                
                print(f"Planfix API request to: {self.base_url}contact/list")
                print(f"Planfix API response status: {response.status_code}")
                print(f"Planfix API response: {response.text[:500]}")  # Первые 500 символов
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Проверяем разные варианты структуры ответа
                    contacts = data.get("contacts") or data.get("list") or []
                    
                    if contacts and len(contacts) > 0:
                        user = contacts[0]
                        full_name = (user.get("name") or 
                                   f"{user.get('lastName', '')} {user.get('firstName', '')} {user.get('middleName', '')}".strip())
                        
                        return {
                            "id": user.get("id"),
                            "email": user.get("email") or email,
                            "full_name": full_name,
                            "last_name": user.get("lastName", ""),
                            "first_name": user.get("firstName", ""),
                            "middle_name": user.get("middleName", ""),
                        }
                else:
                    print(f"Planfix API error response: {response.text}")
                
                return None
                
        except Exception as e:
            print(f"Planfix API exception: {e}")
            import traceback
            traceback.print_exc()
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



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
            "Content-Type": "application/json",
            "Accept": "application/json"
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
                # Используем user/list так как у токена есть user_readonly scope
                response = await client.post(
                    f"{self.base_url}user/list",
                    headers=self.headers,
                    json={
                        "filters": [
                            {
                                "type": 1,  # Email filter  
                                "operator": "equal",
                                "value": email
                            }
                        ],
                        "fields": "id,name,surname,patronymic,email"
                    },
                    timeout=10.0
                )
                
                print(f"Planfix API request to: {self.base_url}user/list")
                print(f"Planfix API response status: {response.status_code}")
                print(f"Planfix API response: {response.text[:500]}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    print(f"Planfix full response: {data}")  # Полный ответ для отладки
                    
                    # Проверяем разные варианты структуры ответа
                    users = data.get("users") or data.get("list") or []
                    
                    if users and len(users) > 0:
                        user = users[0]
                        
                        print(f"User data from Planfix: {user}")  # Данные пользователя
                        
                        # Собираем полное имя из компонентов
                        surname = user.get("surname") or user.get("lastName") or ""
                        name = user.get("name") or user.get("firstName") or ""
                        patronymic = user.get("patronymic") or user.get("middleName") or ""
                        
                        # Формируем ФИО как "Фамилия Имя Отчество"
                        full_name_parts = [surname, name, patronymic]
                        full_name = " ".join([p for p in full_name_parts if p])
                        
                        # Если ничего нет, пробуем извлечь имя из email
                        if not full_name:
                            full_name = user.get("name") or user.get("title")
                            
                            # Если все еще пусто - берем часть email до @
                            if not full_name:
                                email_name = email.split("@")[0]
                                # Пробуем распарсить типичные форматы: firstname.lastname или firstname_lastname
                                if "." in email_name:
                                    parts = email_name.split(".")
                                    full_name = " ".join([p.capitalize() for p in parts if p])
                                elif "_" in email_name:
                                    parts = email_name.split("_")
                                    full_name = " ".join([p.capitalize() for p in parts if p])
                                else:
                                    full_name = email_name.capitalize()
                        
                        print(f"Constructed full name: '{full_name}' (from surname='{surname}', name='{name}', patronymic='{patronymic}')")
                        
                        return {
                            "id": user.get("id"),
                            "email": user.get("email") or email,
                            "full_name": full_name,
                            "last_name": surname,
                            "first_name": name,
                            "middle_name": patronymic,
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
        if user_data.get("full_name") and user_data.get("full_name") != "":
            return user_data["full_name"]
        
        # Или собираем из компонентов (surname name patronymic)
        parts = []
        if user_data.get("last_name"):
            parts.append(user_data["last_name"])
        if user_data.get("first_name"):
            parts.append(user_data["first_name"])
        if user_data.get("middle_name"):
            parts.append(user_data["middle_name"])
        
        if parts:
            return " ".join(parts)
        
        # Если ничего нет, возвращаем email
        return user_data.get("email", "Unknown User")


# Создаем singleton экземпляр сервиса
planfix_service = PlanfixService()



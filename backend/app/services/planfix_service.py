"""
Сервис для работы с Planfix API
"""
import base64
import httpx
import xml.etree.ElementTree as ET
from typing import Optional, Dict
from ..core.config import settings


class PlanfixService:
    """Сервис для взаимодействия с Planfix REST и XML API"""
    
    def __init__(self):
        # REST API
        self.base_url = settings.PLANFIX_API_URL
        self.token = settings.PLANFIX_API_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # XML API (RU датацентр)
        self.xml_api_url = "https://apiru.planfix.ru/xml/"  # официальная точка входа XML API
        self.xml_api_key = "f6d50e651c89858b9bad67a482b3ad64"
        self.xml_token = "2f064a30c8530668cd4e01176be1fb9d"
        self.account = "megamindru"  # строго как в настройках XML API
    
    async def get_user_by_email_xml(self, email: str) -> Optional[Dict]:
        """
        Получает пользователя через XML API с базовой авторизацией (apiKey:token).
        Используем user.getList и ищем нужный email в выдаче.
        """
        print(f"🔷 Trying XML API (basic auth) for email: {email}")

        def local_part(addr: str) -> str:
            return addr.split("@")[0].lower() if addr else ""

        target_local = local_part(email)

        # XML запрос user.getList (Planfix ограничивает pageSize, ставим 100)
        xml_request = f"""<?xml version="1.0" encoding="UTF-8"?>
<request method="user.getList">
  <account>{self.account}</account>
  <pageCurrent>1</pageCurrent>
  <pageSize>100</pageSize>
</request>"""

        basic = base64.b64encode(f"{self.xml_api_key}:{self.xml_token}".encode("utf-8")).decode("utf-8")
        try:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(
                        self.xml_api_url,
                        content=xml_request,
                        headers={
                            "Content-Type": "application/xml; charset=utf-8",
                            "Accept": "application/xml",
                            "Authorization": f"Basic {basic}",
                        },
                        timeout=15.0
                    )
                except Exception as e:
                    print(f"❌ XML request exception: {e}")
                    return None

                print(f"🔷 XML API response status: {response.status_code}")
                print(f"🔷 XML API response (first 500 chars): {response.text[:500]}")

                if response.status_code != 200:
                    print(f"❌ XML API returned status {response.status_code}")
                    return None

                try:
                    root = ET.fromstring(response.text)
                except Exception as parse_err:
                    print(f"❌ XML parse error: {parse_err}")
                    return None

                if root.get('status') != 'ok':
                    err_code = root.find('.//code').text if root.find('.//code') is not None else "unknown"
                    err_msg = root.find('.//message').text if root.find('.//message') is not None else "Unknown error"
                    print(f"❌ XML API error: code={err_code}, msg={err_msg}")
                    return None

                users_node = root.find('.//users')
                if users_node is None:
                    print("⚠️ No users element in XML response")
                    return None

                def extract_user(user):
                    uid = user.find('id').text if user.find('id') is not None else None
                    surname = user.find('lastName').text if user.find('lastName') is not None else ""
                    name = user.find('name').text if user.find('name') is not None else ""
                    patronymic = user.find('midName').text if user.find('midName') is not None else ""
                    primary_email = user.find('email').text if user.find('email') is not None else ""
                    login = user.find('login').text if user.find('login') is not None else ""

                    # В БД нужен формат: Имя Фамилия (БЕЗ отчества!)
                    # Отчество игнорируется, так как в БД пользователи указаны только как Имя Фамилия
                    full_name_parts = [name, surname]  # Без patronymic!
                    full_name = " ".join([p for p in full_name_parts if p]) or login or primary_email or email

                    return uid, surname, name, patronymic, full_name, primary_email, login

                # Безопасный поиск пользователя
                all_users = users_node.findall('user')
                print(f"📋 Total users in XML response: {len(all_users)}")
                print(f"🔍 Searching for: email='{email}', local_part='{target_local}'")
                
                matched_user = None
                match_type = None
                
                # Проходим по всем пользователям
                for idx, user in enumerate(all_users):
                    # Безопасно извлекаем email и login
                    email_node = user.find('email')
                    login_node = user.find('login')
                    
                    user_email = email_node.text if (email_node is not None and email_node.text) else ""
                    user_login = login_node.text if (login_node is not None and login_node.text) else ""
                    
                    # Пропускаем пользователей без email и login
                    if not user_email and not user_login:
                        print(f"   [User #{idx+1}] Skipping: no email, no login")
                        continue
                    
                    # Приводим к нижнему регистру для сравнения
                    user_email_lower = user_email.lower() if user_email else ""
                    user_login_lower = user_login.lower() if user_login else ""
                    user_local = local_part(user_email)
                    
                    # Логируем каждого пользователя для отладки
                    print(f"   [User #{idx+1}] email='{user_email}', login='{user_login}', local='{user_local}'")
                    
                    # Проверяем совпадения (по приоритету)
                    if user_email_lower and user_email_lower == email.lower():
                        matched_user = user
                        match_type = "exact email"
                        print(f"      ✓ MATCH: exact email")
                        break
                    elif user_login_lower and user_login_lower == target_local:
                        matched_user = user
                        match_type = "login"
                        print(f"      ✓ MATCH: login")
                        break
                    elif user_local and user_local == target_local:
                        matched_user = user
                        match_type = "email local part"
                        print(f"      ✓ MATCH: email local part")
                        break
                
                if matched_user:
                    uid, surname, name, patronymic, full_name, primary_email, login = extract_user(matched_user)
                    print(f"\n✅ Found user via XML API user.getList!")
                    print(f"   Match type: {match_type}")
                    print(f"   ID: {uid}")
                    print(f"   Email: {primary_email}")
                    print(f"   Login: {login}")
                    print(f"   Full name: '{full_name}'")
                    print(f"   Parts: surname='{surname}', name='{name}', patronymic='{patronymic}'")

                    return {
                        "id": uid,
                        "email": primary_email or email,
                        "full_name": full_name,
                        "last_name": surname,
                        "first_name": name,
                        "middle_name": patronymic,
                    }
                
                print(f"\n⚠️ User with email '{email}' (local: '{target_local}') NOT FOUND in {len(all_users)} users")
                return None
        except Exception as e:
            print(f"❌ XML API exception: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        """
        Получает информацию о пользователе из Planfix по email
        
        Сначала пробует XML API, затем REST API как fallback
        
        Args:
            email: Email пользователя
            
        Returns:
            Словарь с данными пользователя или None если не найден
        """
        # 🔷 ПРИОРИТЕТ 1: Пробуем XML API
        xml_result = await self.get_user_by_email_xml(email)
        if xml_result:
            print(f"✅ Successfully got user via XML API")
            return xml_result
        
        print(f"⚠️ XML API failed, trying REST API as fallback...")
        
        # 🔄 FALLBACK: Пробуем REST API
        try:
            async with httpx.AsyncClient() as client:
                # Пробуем разные endpoints для получения ФИО
                endpoints_to_try = [
                    ("user/list", {"email": email}),
                    ("contact/list", {"email": email}),
                    ("employee/list", {"filters": [{"field": "email", "operator": "equals", "value": email}]})
                ]
                
                response = None
                for endpoint, payload in endpoints_to_try:
                    print(f"🔄 Trying endpoint: {endpoint} with payload: {payload}")
                    try:
                        response = await client.post(
                            f"{self.base_url}{endpoint}",
                            headers=self.headers,
                            json=payload,
                            timeout=10.0
                        )
                        print(f"   Response status: {response.status_code}")
                        
                        if response.status_code == 200:
                            print(f"   ✅ Success with endpoint: {endpoint}")
                            break
                        else:
                            print(f"   ❌ Failed: {response.text[:200]}")
                    except Exception as e:
                        print(f"   ❌ Exception: {e}")
                        continue
                
                if not response or response.status_code != 200:
                    print(f"❌ All endpoints failed!")
                    return None
                
                # Логи уже выведены выше в цикле
                if response and response.status_code == 200:
                    data = response.json()
                    
                    print(f"📋 Planfix full response: {data}")  # Полный ответ для отладки
                    
                    # Проверяем разные варианты структуры ответа (users, contacts, employees, list)
                    users = (data.get("users") or 
                            data.get("contacts") or 
                            data.get("employees") or 
                            data.get("list") or [])
                    
                    if users and len(users) > 0:
                        user = users[0]
                        
                        print(f"📋 User data from Planfix: {user}")  # Данные пользователя
                        print(f"🔑 Available keys in user object: {list(user.keys())}")
                        
                        # Проверяем, может быть fullName уже есть
                        full_name = (user.get("fullName") or 
                                   user.get("full_name") or 
                                   user.get("displayName") or
                                   user.get("title"))
                        
                        if full_name:
                            print(f"✅ Found fullName directly: '{full_name}'")
                        else:
                            # Собираем полное имя из компонентов
                            surname = user.get("surname") or user.get("lastName") or user.get("lastname") or ""
                            name = user.get("name") or user.get("firstName") or user.get("firstname") or ""
                            patronymic = user.get("patronymic") or user.get("middleName") or user.get("middlename") or ""
                            
                            print(f"🔍 Extracted: surname='{surname}', name='{name}', patronymic='{patronymic}'")
                        
                            # Формируем ФИО как "Имя Фамилия" (БЕЗ отчества!)
                            # Отчество игнорируется, так как в БД пользователи указаны только как Имя Фамилия
                            full_name_parts = [name, surname]  # Без patronymic!
                            full_name = " ".join([p for p in full_name_parts if p])
                            
                            print(f"🔧 Constructed from parts (without patronymic): '{full_name}'")
                        
                        # Если все еще пусто - берем часть email до @
                        if not full_name:
                            email_name = email.split("@")[0]
                            print(f"⚠️ No fullName from Planfix, using email part: '{email_name}'")
                            # Пробуем распарсить типичные форматы: firstname.lastname или firstname_lastname
                            if "." in email_name:
                                parts = email_name.split(".")
                                full_name = " ".join([p.capitalize() for p in parts if p])
                            elif "_" in email_name:
                                parts = email_name.split("_")
                                full_name = " ".join([p.capitalize() for p in parts if p])
                            else:
                                full_name = email_name.capitalize()
                        
                        print(f"🎯 Final full name: '{full_name}'")
                        
                        return {
                            "id": user.get("id"),
                            "email": user.get("email") or email,
                            "full_name": full_name,
                            "last_name": user.get("surname", ""),
                            "first_name": user.get("name", ""),
                            "middle_name": user.get("patronymic", ""),
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



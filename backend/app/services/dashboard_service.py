"""
Сервис для работы с дашбордами и SQL-запросами
"""
from typing import List, Dict, Any
from ..core.database import execute_query


class DashboardService:
    """Сервис для получения данных дашбордов"""
    
    def get_dashboard_data(self, user_full_name: str) -> List[Dict[str, Any]]:
        """
        Получает все данные дашборда для конкретного пользователя
        
        Args:
            user_full_name: Полное ФИО пользователя
            
        Returns:
            Список элементов дашборда с данными
        """
        dashboard_items = []
        
        # Здесь будут ваши SQL-запросы
        # Пример структуры:
        
        # 1. Пример таблицы с конверсиями
        conversions = self._get_conversions_data(user_full_name)
        if conversions:
            dashboard_items.append({
                "id": "conversions",
                "title": "Конверсии КП",
                "description": "Показатели конверсии коммерческих предложений",
                "data": conversions,
                "columns": list(conversions[0].keys()) if conversions else []
            })
        
        # 2. Пример таблицы со средним сроком подготовки
        preparation_time = self._get_preparation_time_data(user_full_name)
        if preparation_time:
            dashboard_items.append({
                "id": "preparation_time",
                "title": "Средний срок подготовки КП",
                "description": "Время подготовки коммерческих предложений по месяцам",
                "data": preparation_time,
                "columns": list(preparation_time[0].keys()) if preparation_time else []
            })
        
        # Добавьте здесь другие запросы по аналогии
        
        return dashboard_items
    
    def _get_conversions_data(self, user_full_name: str) -> List[Dict]:
        """
        Получает данные по конверсиям для пользователя
        
        ВАЖНО: Замените этот запрос на ваш реальный SQL-запрос
        """
        # Пример запроса - замените на свой
        query = """
        SELECT 
            date_column,
            metric1,
            metric2,
            percentage
        FROM your_table
        WHERE "user" = :user_name
        ORDER BY date_column DESC
        LIMIT 100
        """
        
        try:
            result = execute_query(query, {"user_name": user_full_name})
            return result
        except Exception as e:
            print(f"Error executing conversions query: {e}")
            return []
    
    def _get_preparation_time_data(self, user_full_name: str) -> List[Dict]:
        """
        Получает данные по срокам подготовки для пользователя
        
        ВАЖНО: Замените этот запрос на ваш реальный SQL-запрос
        """
        # Пример запроса - замените на свой
        query = """
        SELECT 
            month_column,
            avg_time,
            count
        FROM your_table
        WHERE "user" = :user_name
        ORDER BY month_column DESC
        LIMIT 100
        """
        
        try:
            result = execute_query(query, {"user_name": user_full_name})
            return result
        except Exception as e:
            print(f"Error executing preparation time query: {e}")
            return []
    
    def execute_custom_query(self, query: str, user_full_name: str) -> List[Dict]:
        """
        Выполняет пользовательский SQL-запрос с автоматической фильтрацией по пользователю
        
        Args:
            query: SQL-запрос (должен содержать плейсхолдер :user_name)
            user_full_name: ФИО пользователя для фильтрации
            
        Returns:
            Результаты запроса
        """
        try:
            # Проверяем, что запрос содержит фильтр по пользователю
            if ":user_name" not in query and "{user_name}" not in query:
                # Пробуем автоматически добавить фильтр
                if "WHERE" in query.upper():
                    query = query.replace("WHERE", 'WHERE "user" = :user_name AND', 1)
                else:
                    # Находим FROM и добавляем WHERE после него
                    query += ' WHERE "user" = :user_name'
            
            result = execute_query(query, {"user_name": user_full_name})
            return result
        except Exception as e:
            print(f"Error executing custom query: {e}")
            return []


# Создаем singleton экземпляр сервиса
dashboard_service = DashboardService()



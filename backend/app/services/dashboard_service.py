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
        
        # 1. Конверсии КП в образцы
        conversions = self._get_conversions_data(user_full_name)
        if conversions:
            dashboard_items.append({
                "id": "conversions",
                "title": "Конверсии КП в образцы",
                "description": "Показатели конверсии коммерческих предложений в образцы по периодам",
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
        Получает данные по конверсиям КП для пользователя за разные периоды
        """
        query = """
        WITH user_data AS (
            -- Объединяем данные из обеих таблиц
            SELECT 
                'Текущий квартал' as "Период",
                :user_name as "Менеджер",
                COUNT(DISTINCT proscheti.task_id) as "Кол-во КП",
                COUNT(DISTINCT obrazci.task_id) as "Кол-во образцов",
                CASE 
                    WHEN COUNT(DISTINCT proscheti.task_id) = 0 THEN 0
                    ELSE ROUND(
                        CAST(COUNT(DISTINCT obrazci.task_id) AS NUMERIC) * 100.0 / 
                        NULLIF(COUNT(DISTINCT proscheti.task_id), 0), 
                        2
                    )
                END as "Конверсия"
            FROM (
                SELECT task_id, "user", cp_finish FROM proscheti_gr_artema
                WHERE "user" = :user_name
                UNION ALL
                SELECT task_id, "user", cp_finish FROM proscheti_gr_zheni
                WHERE "user" = :user_name
            ) proscheti
            LEFT JOIN (
                SELECT task_id, "user", date_create FROM obrazci_gr_artema
                WHERE "user" = :user_name
                UNION ALL
                SELECT task_id, "user", date_create FROM obrazci_gr_zheni
                WHERE "user" = :user_name
            ) obrazci ON proscheti."user" = obrazci."user"
            WHERE 
                proscheti.cp_finish >= DATE_TRUNC('quarter', NOW())
                AND proscheti.cp_finish < DATE_TRUNC('quarter', NOW() + INTERVAL '3 month')
                AND (
                    obrazci.date_create IS NULL 
                    OR (
                        obrazci.date_create >= DATE_TRUNC('quarter', NOW())
                        AND obrazci.date_create < DATE_TRUNC('quarter', NOW() + INTERVAL '3 month')
                    )
                )
            
            UNION ALL
            
            -- Прошлый квартал
            SELECT 
                'Прошлый квартал' as "Период",
                :user_name as "Менеджер",
                COUNT(DISTINCT proscheti.task_id) as "Кол-во КП",
                COUNT(DISTINCT obrazci.task_id) as "Кол-во образцов",
                CASE 
                    WHEN COUNT(DISTINCT proscheti.task_id) = 0 THEN 0
                    ELSE ROUND(
                        CAST(COUNT(DISTINCT obrazci.task_id) AS NUMERIC) * 100.0 / 
                        NULLIF(COUNT(DISTINCT proscheti.task_id), 0), 
                        2
                    )
                END as "Конверсия"
            FROM (
                SELECT task_id, "user", cp_finish FROM proscheti_gr_artema
                WHERE "user" = :user_name
                UNION ALL
                SELECT task_id, "user", cp_finish FROM proscheti_gr_zheni
                WHERE "user" = :user_name
            ) proscheti
            LEFT JOIN (
                SELECT task_id, "user", date_create FROM obrazci_gr_artema
                WHERE "user" = :user_name
                UNION ALL
                SELECT task_id, "user", date_create FROM obrazci_gr_zheni
                WHERE "user" = :user_name
            ) obrazci ON proscheti."user" = obrazci."user"
            WHERE 
                proscheti.cp_finish >= DATE_TRUNC('quarter', NOW() - INTERVAL '3 month')
                AND proscheti.cp_finish < DATE_TRUNC('quarter', NOW())
                AND (
                    obrazci.date_create IS NULL 
                    OR (
                        obrazci.date_create >= DATE_TRUNC('quarter', NOW() - INTERVAL '3 month')
                        AND obrazci.date_create < DATE_TRUNC('quarter', NOW())
                    )
                )
            
            UNION ALL
            
            -- Финансовый год (1 марта текущего года - 28 февраля следующего)
            SELECT 
                'Финансовый год' as "Период",
                :user_name as "Менеджер",
                COUNT(DISTINCT proscheti.task_id) as "Кол-во КП",
                COUNT(DISTINCT obrazci.task_id) as "Кол-во образцов",
                CASE 
                    WHEN COUNT(DISTINCT proscheti.task_id) = 0 THEN 0
                    ELSE ROUND(
                        CAST(COUNT(DISTINCT obrazci.task_id) AS NUMERIC) * 100.0 / 
                        NULLIF(COUNT(DISTINCT proscheti.task_id), 0), 
                        2
                    )
                END as "Конверсия"
            FROM (
                SELECT task_id, "user", cp_finish FROM proscheti_gr_artema
                WHERE "user" = :user_name
                UNION ALL
                SELECT task_id, "user", cp_finish FROM proscheti_gr_zheni
                WHERE "user" = :user_name
            ) proscheti
            LEFT JOIN (
                SELECT task_id, "user", date_create FROM obrazci_gr_artema
                WHERE "user" = :user_name
                UNION ALL
                SELECT task_id, "user", date_create FROM obrazci_gr_zheni
                WHERE "user" = :user_name
            ) obrazci ON proscheti."user" = obrazci."user"
            WHERE 
                proscheti.cp_finish >= 
                    CASE 
                        WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                        THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int, 3, 1)
                        ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int - 1, 3, 1)
                    END
                AND proscheti.cp_finish < 
                    CASE 
                        WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                        THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + 1, 3, 1)
                        ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int, 3, 1)
                    END
                AND (
                    obrazci.date_create IS NULL 
                    OR (
                        obrazci.date_create >= 
                            CASE 
                                WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                                THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int, 3, 1)
                                ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int - 1, 3, 1)
                            END
                        AND obrazci.date_create < 
                            CASE 
                                WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                                THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + 1, 3, 1)
                                ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int, 3, 1)
                            END
                    )
                )
        )
        SELECT 
            "Период",
            "Кол-во КП",
            "Кол-во образцов",
            CONCAT("Конверсия", '%') as "Конверсия"
        FROM user_data
        ORDER BY 
            CASE "Период"
                WHEN 'Текущий квартал' THEN 1
                WHEN 'Прошлый квартал' THEN 2
                WHEN 'Финансовый год' THEN 3
            END
        """
        
        try:
            result = execute_query(query, {"user_name": user_full_name})
            return result
        except Exception as e:
            print(f"Error executing conversions query: {e}")
            import traceback
            traceback.print_exc()
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



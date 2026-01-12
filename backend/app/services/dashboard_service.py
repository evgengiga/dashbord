"""
Сервис для работы с дашбордами и SQL-запросами
"""
from typing import List, Dict, Any
from ..core.database import execute_query


class DashboardService:
    """Сервис для получения данных дашбордов"""
    
    def get_dashboard_data(self, user_full_name: str, fiscal_year: str = "current") -> List[Dict[str, Any]]:
        """
        Получает все данные дашборда для конкретного пользователя
        
        Args:
            user_full_name: Полное ФИО пользователя
            fiscal_year: "current" для текущего года, "previous" для прошлого
            
        Returns:
            Список элементов дашборда с данными
        """
        dashboard_items = []
        
        # 1. Просроченные задачи (самое важное - показываем первым!)
        overdue_tasks_data = self._get_overdue_tasks_data(user_full_name)
        if overdue_tasks_data and overdue_tasks_data.get("summary"):
            dashboard_items.append({
                "id": "overdue_tasks",
                "title": "⚠️ Просроченные задачи",
                "description": "Количество и среднее время просрочки по категориям",
                "data": overdue_tasks_data["summary"],
                "columns": list(overdue_tasks_data["summary"][0].keys()) if overdue_tasks_data["summary"] else [],
                "details": overdue_tasks_data.get("details", [])  # Добавляем детализацию
            })
        
        # 2. Конверсии КП в образцы
        conversions = self._get_conversions_data(user_full_name, fiscal_year)
        if conversions:
            dashboard_items.append({
                "id": "conversions",
                "title": "Конверсии КП в образцы",
                "description": "Показатели конверсии коммерческих предложений в образцы по периодам",
                "data": conversions,
                "columns": list(conversions[0].keys()) if conversions else []
            })
        
        # 3. Конверсии КП в производство
        production_conversions = self._get_production_conversions_data(user_full_name, fiscal_year)
        if production_conversions:
            dashboard_items.append({
                "id": "production_conversions",
                "title": "Конверсии КП в производство",
                "description": "Показатели конверсии коммерческих предложений в производство по периодам",
                "data": production_conversions,
                "columns": list(production_conversions[0].keys()) if production_conversions else []
            })
        
        # 4. Среднее время согласования КП по месяцам
        approval_time = self._get_approval_time_data(user_full_name)
        if approval_time:
            dashboard_items.append({
                "id": "approval_time",
                "title": "Среднее время согласования КП",
                "description": "Среднее количество дней на согласование КП по месяцам текущего года",
                "data": approval_time,
                "columns": list(approval_time[0].keys()) if approval_time else []
            })
        
        # 5. Среднее время принятия производства по месяцам
        production_acceptance_time = self._get_production_acceptance_time_data(user_full_name, fiscal_year)
        if production_acceptance_time:
            dashboard_items.append({
                "id": "production_acceptance_time",
                "title": "Среднее время принятия производства",
                "description": "Среднее количество дней на принятие производства по месяцам финансового года",
                "data": production_acceptance_time,
                "columns": list(production_acceptance_time[0].keys()) if production_acceptance_time else []
            })
        
        # 6. Заказы от клиентов по финансовому году
        client_orders = self._get_client_orders_data(user_full_name, fiscal_year)
        if client_orders:
            dashboard_items.append({
                "id": "client_orders",
                "title": "Заказы от клиентов",
                "description": "Количество заказов от клиентов за финансовый год",
                "data": client_orders,
                "columns": list(client_orders[0].keys()) if client_orders else []
            })
        
        return dashboard_items
    
    def _get_conversions_data(self, user_full_name: str, fiscal_year: str = "current") -> List[Dict]:
        """
        Получает данные по конверсиям КП для пользователя за разные периоды
        
        Args:
            user_full_name: ФИО пользователя
            fiscal_year: "current" или "previous"
        """
        print(f"🔍 Executing conversions query for user: '{user_full_name}', fiscal year: {fiscal_year}")
        
        # Сначала проверяем, какие пользователи есть в БД
        try:
            debug_query = """
            SELECT DISTINCT "user" 
            FROM (
                SELECT "user" FROM proscheti_gr_artema
                UNION
                SELECT "user" FROM proscheti_gr_zheni
            ) all_users
            WHERE "user" IS NOT NULL
            ORDER BY "user"
            LIMIT 50
            """
            all_users_in_db = execute_query(debug_query, {})
            print(f"👥 Users found in database tables: {[u['user'] for u in all_users_in_db]}")
        except Exception as e:
            print(f"⚠️ Could not fetch users list: {e}")
        
        # Определяем смещение для финансового года
        year_offset = 0 if fiscal_year == "current" else -1
        
        query = f"""
        WITH user_data AS (
            -- Объединяем данные из обеих таблиц
            SELECT 
                CONCAT(
                    'Текущий квартал (',
                    TO_CHAR(DATE_TRUNC('quarter', NOW()), 'DD.MM.YYYY'),
                    ' - ',
                    TO_CHAR(DATE_TRUNC('quarter', NOW() + INTERVAL '3 month') - INTERVAL '1 day', 'DD.MM.YYYY'),
                    ')'
                ) as "Период",
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
                CONCAT(
                    'Прошлый квартал (',
                    TO_CHAR(DATE_TRUNC('quarter', NOW() - INTERVAL '3 month'), 'DD.MM.YYYY'),
                    ' - ',
                    TO_CHAR(DATE_TRUNC('quarter', NOW()) - INTERVAL '1 day', 'DD.MM.YYYY'),
                    ')'
                ) as "Период",
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
            
            -- Финансовый год (1 марта - 28 февраля) с учетом выбранного года
            SELECT 
                CONCAT(
                    'Финансовый год (',
                    TO_CHAR(
                        CASE 
                            WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                            THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + {year_offset}, 3, 1)
                            ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int - 1 + {year_offset}, 3, 1)
                        END,
                        'DD.MM.YYYY'
                    ),
                    ' - ',
                    TO_CHAR(
                        CASE 
                            WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                            THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + 1 + {year_offset}, 3, 1) - INTERVAL '1 day'
                            ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + {year_offset}, 3, 1) - INTERVAL '1 day'
                        END,
                        'DD.MM.YYYY'
                    ),
                    ')'
                ) as "Период",
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
                        THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + {year_offset}, 3, 1)
                        ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int - 1 + {year_offset}, 3, 1)
                    END
                AND proscheti.cp_finish < 
                    CASE 
                        WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                        THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + 1 + {year_offset}, 3, 1)
                        ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + {year_offset}, 3, 1)
                    END
                AND (
                    obrazci.date_create IS NULL 
                    OR (
                        obrazci.date_create >= 
                            CASE 
                                WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                                THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + {year_offset}, 3, 1)
                                ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int - 1 + {year_offset}, 3, 1)
                            END
                        AND obrazci.date_create < 
                            CASE 
                                WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                                THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + 1 + {year_offset}, 3, 1)
                                ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + {year_offset}, 3, 1)
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
            CASE 
                WHEN "Период" LIKE 'Текущий квартал%' THEN 1
                WHEN "Период" LIKE 'Прошлый квартал%' THEN 2
                WHEN "Период" LIKE 'Финансовый год%' THEN 3
            END
        """
        
        try:
            result = execute_query(query, {"user_name": user_full_name})
            print(f"✅ Query executed, rows returned: {len(result)}")
            if result:
                print(f"📊 Sample row: {result[0]}")
            return result
        except Exception as e:
            print(f"Error executing conversions query: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _get_production_conversions_data(self, user_full_name: str, fiscal_year: str = "current") -> List[Dict]:
        """
        Получает данные по конверсиям КП в производство для пользователя за разные периоды
        
        Args:
            user_full_name: ФИО пользователя
            fiscal_year: "current" или "previous"
        """
        print(f"🔍 Executing production conversions query for user: '{user_full_name}', fiscal year: {fiscal_year}")
        
        # Определяем смещение для финансового года
        year_offset = 0 if fiscal_year == "current" else -1
        
        query = f"""
        WITH user_data AS (
            -- Текущий квартал
            SELECT 
                CONCAT(
                    'Текущий квартал (',
                    TO_CHAR(DATE_TRUNC('quarter', NOW()), 'DD.MM.YYYY'),
                    ' - ',
                    TO_CHAR(DATE_TRUNC('quarter', NOW() + INTERVAL '3 month') - INTERVAL '1 day', 'DD.MM.YYYY'),
                    ')'
                ) as "Период",
                COUNT(DISTINCT proscheti.task_id) as "Кол-во КП",
                COUNT(DISTINCT proizv.task_id) as "Кол-во в производстве",
                CASE 
                    WHEN COUNT(DISTINCT proscheti.task_id) = 0 THEN 0
                    ELSE ROUND(
                        CAST(COUNT(DISTINCT proizv.task_id) AS NUMERIC) * 100.0 / 
                        NULLIF(COUNT(DISTINCT proscheti.task_id), 0), 
                        2
                    )
                END as "Конверсия"
            FROM (
                SELECT task_id, "user", cp_finish, status FROM proscheti_gr_artema
                WHERE "user" = :user_name
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
                  AND (status = 'Завершенная' OR status = 'КП Согласовано')
                UNION ALL
                SELECT task_id, "user", cp_finish, status FROM proscheti_gr_zheni
                WHERE "user" = :user_name
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
                  AND (status = 'Завершенная' OR status = 'КП Согласовано')
            ) proscheti
            LEFT JOIN (
                SELECT task_id, "user", date_create FROM proizv_gr_artema
                WHERE "user" = :user_name
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
                UNION ALL
                SELECT task_id, "user", date_create FROM proizv_gr_zheni
                WHERE "user" = :user_name
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
            ) proizv ON proscheti."user" = proizv."user"
            WHERE 
                proscheti.cp_finish >= DATE_TRUNC('quarter', NOW())
                AND proscheti.cp_finish < DATE_TRUNC('quarter', NOW() + INTERVAL '3 month')
                AND (
                    proizv.date_create IS NULL 
                    OR (
                        proizv.date_create >= DATE_TRUNC('quarter', NOW())
                        AND proizv.date_create < DATE_TRUNC('quarter', NOW() + INTERVAL '3 month')
                    )
                )
            
            UNION ALL
            
            -- Прошлый квартал
            SELECT 
                CONCAT(
                    'Прошлый квартал (',
                    TO_CHAR(DATE_TRUNC('quarter', NOW() - INTERVAL '3 month'), 'DD.MM.YYYY'),
                    ' - ',
                    TO_CHAR(DATE_TRUNC('quarter', NOW()) - INTERVAL '1 day', 'DD.MM.YYYY'),
                    ')'
                ) as "Период",
                COUNT(DISTINCT proscheti.task_id) as "Кол-во КП",
                COUNT(DISTINCT proizv.task_id) as "Кол-во в производстве",
                CASE 
                    WHEN COUNT(DISTINCT proscheti.task_id) = 0 THEN 0
                    ELSE ROUND(
                        CAST(COUNT(DISTINCT proizv.task_id) AS NUMERIC) * 100.0 / 
                        NULLIF(COUNT(DISTINCT proscheti.task_id), 0), 
                        2
                    )
                END as "Конверсия"
            FROM (
                SELECT task_id, "user", cp_finish, status FROM proscheti_gr_artema
                WHERE "user" = :user_name
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
                  AND (status = 'Завершенная' OR status = 'КП Согласовано')
                UNION ALL
                SELECT task_id, "user", cp_finish, status FROM proscheti_gr_zheni
                WHERE "user" = :user_name
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
                  AND (status = 'Завершенная' OR status = 'КП Согласовано')
            ) proscheti
            LEFT JOIN (
                SELECT task_id, "user", date_create FROM proizv_gr_artema
                WHERE "user" = :user_name
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
                UNION ALL
                SELECT task_id, "user", date_create FROM proizv_gr_zheni
                WHERE "user" = :user_name
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
            ) proizv ON proscheti."user" = proizv."user"
            WHERE 
                proscheti.cp_finish >= DATE_TRUNC('quarter', NOW() - INTERVAL '3 month')
                AND proscheti.cp_finish < DATE_TRUNC('quarter', NOW())
                AND (
                    proizv.date_create IS NULL 
                    OR (
                        proizv.date_create >= DATE_TRUNC('quarter', NOW() - INTERVAL '3 month')
                        AND proizv.date_create < DATE_TRUNC('quarter', NOW())
                    )
                )
            
            UNION ALL
            
            -- Финансовый год (1 марта - 28 февраля) с учетом выбранного года
            SELECT 
                CONCAT(
                    'Финансовый год (',
                    TO_CHAR(
                        CASE 
                            WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                            THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + {year_offset}, 3, 1)
                            ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int - 1 + {year_offset}, 3, 1)
                        END,
                        'DD.MM.YYYY'
                    ),
                    ' - ',
                    TO_CHAR(
                        CASE 
                            WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                            THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + 1 + {year_offset}, 3, 1) - INTERVAL '1 day'
                            ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + {year_offset}, 3, 1) - INTERVAL '1 day'
                        END,
                        'DD.MM.YYYY'
                    ),
                    ')'
                ) as "Период",
                COUNT(DISTINCT proscheti.task_id) as "Кол-во КП",
                COUNT(DISTINCT proizv.task_id) as "Кол-во в производстве",
                CASE 
                    WHEN COUNT(DISTINCT proscheti.task_id) = 0 THEN 0
                    ELSE ROUND(
                        CAST(COUNT(DISTINCT proizv.task_id) AS NUMERIC) * 100.0 / 
                        NULLIF(COUNT(DISTINCT proscheti.task_id), 0), 
                        2
                    )
                END as "Конверсия"
            FROM (
                SELECT task_id, "user", cp_finish, status FROM proscheti_gr_artema
                WHERE "user" = :user_name
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
                  AND (status = 'Завершенная' OR status = 'КП Согласовано')
                UNION ALL
                SELECT task_id, "user", cp_finish, status FROM proscheti_gr_zheni
                WHERE "user" = :user_name
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
                  AND (status = 'Завершенная' OR status = 'КП Согласовано')
            ) proscheti
            LEFT JOIN (
                SELECT task_id, "user", date_create FROM proizv_gr_artema
                WHERE "user" = :user_name
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
                UNION ALL
                SELECT task_id, "user", date_create FROM proizv_gr_zheni
                WHERE "user" = :user_name
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
            ) proizv ON proscheti."user" = proizv."user"
            WHERE 
                proscheti.cp_finish >= 
                    CASE 
                        WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                        THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + {year_offset}, 3, 1)
                        ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int - 1 + {year_offset}, 3, 1)
                    END
                AND proscheti.cp_finish < 
                    CASE 
                        WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                        THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + 1 + {year_offset}, 3, 1)
                        ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + {year_offset}, 3, 1)
                    END
                AND (
                    proizv.date_create IS NULL 
                    OR (
                        proizv.date_create >= 
                            CASE 
                                WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                                THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + {year_offset}, 3, 1)
                                ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int - 1 + {year_offset}, 3, 1)
                            END
                        AND proizv.date_create < 
                            CASE 
                                WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                                THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + 1 + {year_offset}, 3, 1)
                                ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + {year_offset}, 3, 1)
                            END
                    )
                )
        )
        SELECT 
            "Период",
            "Кол-во КП",
            "Кол-во в производстве",
            CONCAT("Конверсия", '%') as "Конверсия"
        FROM user_data
        ORDER BY 
            CASE 
                WHEN "Период" LIKE 'Текущий квартал%' THEN 1
                WHEN "Период" LIKE 'Прошлый квартал%' THEN 2
                WHEN "Период" LIKE 'Финансовый год%' THEN 3
            END
        """
        
        try:
            result = execute_query(query, {"user_name": user_full_name})
            print(f"✅ Production query executed, rows returned: {len(result)}")
            if result:
                print(f"📊 Sample row: {result[0]}")
            return result
        except Exception as e:
            print(f"Error executing production conversions query: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _get_approval_time_data(self, user_full_name: str) -> List[Dict]:
        """
        Получает среднее время согласования КП по месяцам для пользователя
        
        Args:
            user_full_name: ФИО пользователя
        """
        print(f"🔍 Executing approval time query for user: '{user_full_name}'")
        
        query = """
        WITH monthly_data AS (
            SELECT
                DATE_TRUNC('month', cp_sogl)::date AS month_date,
                AVG(serch_sogl_day) AS avg_days
            FROM (
                SELECT cp_sogl, serch_sogl_day, "user" FROM proscheti_gr_artema
                WHERE "user" = :user_name
                  AND serch_date IS NOT NULL
                  AND cp_sogl IS NOT NULL
                  AND (serch_date <> '1970-01-01' OR serch_date IS NULL)
                  AND (cp_sogl <> '1970-01-01' OR cp_sogl IS NULL)
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
                UNION ALL
                SELECT cp_sogl, serch_sogl_day, "user" FROM proscheti_gr_zheni
                WHERE "user" = :user_name
                  AND serch_date IS NOT NULL
                  AND cp_sogl IS NOT NULL
                  AND (serch_date <> '1970-01-01' OR serch_date IS NULL)
                  AND (cp_sogl <> '1970-01-01' OR cp_sogl IS NULL)
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
            ) combined
            WHERE cp_sogl >= DATE_TRUNC('year', NOW())
              AND cp_sogl < DATE_TRUNC('year', NOW() + INTERVAL '1 year')
            GROUP BY DATE_TRUNC('month', cp_sogl)::date
            ORDER BY DATE_TRUNC('month', cp_sogl)::date
        ),
        with_changes AS (
            SELECT
                month_date,
                avg_days,
                LAG(avg_days) OVER (ORDER BY month_date) AS prev_month_avg
            FROM monthly_data
        )
        SELECT
            CASE EXTRACT(MONTH FROM month_date)
                WHEN 1 THEN 'Январь'
                WHEN 2 THEN 'Февраль'
                WHEN 3 THEN 'Март'
                WHEN 4 THEN 'Апрель'
                WHEN 5 THEN 'Май'
                WHEN 6 THEN 'Июнь'
                WHEN 7 THEN 'Июль'
                WHEN 8 THEN 'Август'
                WHEN 9 THEN 'Сентябрь'
                WHEN 10 THEN 'Октябрь'
                WHEN 11 THEN 'Ноябрь'
                WHEN 12 THEN 'Декабрь'
            END || ', ' || EXTRACT(YEAR FROM month_date)::text AS "Месяц",
            ROUND(avg_days::numeric, 1) AS "Среднее время (дней)",
            CASE
                WHEN prev_month_avg IS NULL THEN NULL
                ELSE ROUND((avg_days - prev_month_avg)::numeric, 1)
            END AS "Изменение"
        FROM with_changes
        ORDER BY month_date
        """
        
        try:
            result = execute_query(query, {"user_name": user_full_name})
            print(f"✅ Approval time query executed, rows returned: {len(result)}")
            if result:
                print(f"📊 Sample row: {result[0]}")
            return result
        except Exception as e:
            print(f"Error executing approval time query: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _get_overdue_tasks_data(self, user_full_name: str) -> List[Dict]:
        """
        Получает данные по просроченным задачам с группировкой и детализацией
        
        Args:
            user_full_name: ФИО пользователя
            
        Returns:
            Список словарей: summary (сводка) + details (детализация по типам)
        """
        print(f"🔍 Executing overdue tasks query for user: '{user_full_name}'")
        
        # Сводная таблица
        summary_query = """
        WITH proscheti_overdue AS (
            SELECT
                COUNT(*) AS count,
                AVG(prosr_day) AS avg_days
            FROM (
                SELECT prosr_day FROM proscheti_gr_artema
                WHERE "user" = :user_name
                  AND prosrok_now = 'Да'
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
                UNION ALL
                SELECT prosr_day FROM proscheti_gr_zheni
                WHERE "user" = :user_name
                  AND prosrok_now = 'Да'
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
            ) combined
        ),
        obrazci_overdue AS (
            SELECT
                COUNT(*) AS count,
                AVG(prosr_day) AS avg_days
            FROM (
                SELECT prosr_day FROM obrazci_gr_artema
                WHERE "user" = :user_name
                  AND prosrok_now = 'Да'
                  AND (status <> 'Завершенная' OR status IS NULL)
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
                UNION ALL
                SELECT prosr_day FROM obrazci_gr_zheni
                WHERE "user" = :user_name
                  AND prosrok_now = 'Да'
                  AND (status <> 'Завершенная' OR status IS NULL)
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
            ) combined
        ),
        proizv_overdue AS (
            SELECT
                COUNT(*) AS count,
                AVG(prosr_day) AS avg_days
            FROM (
                SELECT prosr_day FROM proizv_gr_artema
                WHERE "user" = :user_name
                  AND prosrok_now = 'Да'
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
                UNION ALL
                SELECT prosr_day FROM proizv_gr_zheni
                WHERE "user" = :user_name
                  AND prosrok_now = 'Да'
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
            ) combined
        )
        SELECT
            'Просчеты' AS "Категория",
            COALESCE(p.count, 0) AS "Кол-во",
            ROUND(COALESCE(p.avg_days, 0)::numeric, 1) AS "Ср. дней"
        FROM proscheti_overdue p
        UNION ALL
        SELECT
            'Образцы' AS "Категория",
            COALESCE(o.count, 0) AS "Кол-во",
            ROUND(COALESCE(o.avg_days, 0)::numeric, 1) AS "Ср. дней"
        FROM obrazci_overdue o
        UNION ALL
        SELECT
            'Производства' AS "Категория",
            COALESCE(pr.count, 0) AS "Кол-во",
            ROUND(COALESCE(pr.avg_days, 0)::numeric, 1) AS "Ср. дней"
        FROM proizv_overdue pr
        """
        
        # Детализация задач с task_id и task_name
        details_query = """
        SELECT
            'Просчеты' AS category,
            task_id,
            task_name,
            prosr_day
        FROM (
            SELECT task_id, task_name, prosr_day FROM proscheti_gr_artema
            WHERE "user" = :user_name
              AND prosrok_now = 'Да'
              AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
            UNION ALL
            SELECT task_id, task_name, prosr_day FROM proscheti_gr_zheni
            WHERE "user" = :user_name
              AND prosrok_now = 'Да'
              AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
        ) proscheti
        
        UNION ALL
        
        SELECT
            'Образцы' AS category,
            task_id,
            task_name,
            prosr_day
        FROM (
            SELECT task_id, task_name, prosr_day FROM obrazci_gr_artema
            WHERE "user" = :user_name
              AND prosrok_now = 'Да'
              AND (status <> 'Завершенная' OR status IS NULL)
              AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
            UNION ALL
            SELECT task_id, task_name, prosr_day FROM obrazci_gr_zheni
            WHERE "user" = :user_name
              AND prosrok_now = 'Да'
              AND (status <> 'Завершенная' OR status IS NULL)
              AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
        ) obrazci
        
        UNION ALL
        
        SELECT
            'Производства' AS category,
            task_id,
            task_name,
            prosr_day
        FROM (
            SELECT task_id, task_name, prosr_day FROM proizv_gr_artema
            WHERE "user" = :user_name
              AND prosrok_now = 'Да'
              AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
            UNION ALL
            SELECT task_id, task_name, prosr_day FROM proizv_gr_zheni
            WHERE "user" = :user_name
              AND prosrok_now = 'Да'
              AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
        ) proizv
        
        ORDER BY category, prosr_day DESC
        """
        
        try:
            summary = execute_query(summary_query, {"user_name": user_full_name})
            details = execute_query(details_query, {"user_name": user_full_name})
            
            print(f"✅ Overdue tasks summary: {len(summary)} categories")
            print(f"✅ Overdue tasks details: {len(details)} tasks")
            
            # Возвращаем и сводку, и детализацию
            return {
                "summary": summary,
                "details": details
            }
        except Exception as e:
            print(f"Error executing overdue tasks query: {e}")
            import traceback
            traceback.print_exc()
            return {"summary": [], "details": []}
    
    def _get_production_acceptance_time_data(self, user_full_name: str, fiscal_year: str = "current") -> List[Dict]:
        """
        Получает среднее время принятия производства по месяцам для пользователя
        
        Args:
            user_full_name: ФИО пользователя
            fiscal_year: "current" или "previous"
        """
        print(f"🔍 Executing production acceptance time query for user: '{user_full_name}', fiscal year: {fiscal_year}")
        
        # Определяем смещение для финансового года
        year_offset = 0 if fiscal_year == "current" else -1
        
        query = f"""
        WITH monthly_data AS (
            SELECT
                DATE_TRUNC('month', date_accept)::date AS month_date,
                AVG(colvo_days_accept) AS avg_days
            FROM (
                SELECT date_accept, colvo_days_accept FROM proizv_gr_artema
                WHERE "user" = :user_name
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
                  AND date_accept IS NOT NULL
                UNION ALL
                SELECT date_accept, colvo_days_accept FROM proizv_gr_zheni
                WHERE "user" = :user_name
                  AND ("user" <> 'Артем Василевский' OR "user" IS NULL)
                  AND date_accept IS NOT NULL
            ) combined
            WHERE date_accept >= 
                CASE 
                    WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                    THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + {year_offset}, 3, 1)
                    ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int - 1 + {year_offset}, 3, 1)
                END
            AND date_accept < 
                CASE 
                    WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                    THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + 1 + {year_offset}, 3, 1)
                    ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + {year_offset}, 3, 1)
                END
            GROUP BY DATE_TRUNC('month', date_accept)::date
            ORDER BY DATE_TRUNC('month', date_accept)::date
        ),
        with_changes AS (
            SELECT
                month_date,
                avg_days,
                LAG(avg_days) OVER (ORDER BY month_date) AS prev_month_avg
            FROM monthly_data
        )
        SELECT
            CASE EXTRACT(MONTH FROM month_date)
                WHEN 1 THEN 'Январь'
                WHEN 2 THEN 'Февраль'
                WHEN 3 THEN 'Март'
                WHEN 4 THEN 'Апрель'
                WHEN 5 THEN 'Май'
                WHEN 6 THEN 'Июнь'
                WHEN 7 THEN 'Июль'
                WHEN 8 THEN 'Август'
                WHEN 9 THEN 'Сентябрь'
                WHEN 10 THEN 'Октябрь'
                WHEN 11 THEN 'Ноябрь'
                WHEN 12 THEN 'Декабрь'
            END || ', ' || EXTRACT(YEAR FROM month_date)::text AS "Месяц",
            ROUND(avg_days::numeric, 1) AS "Среднее время (дней)",
            CASE
                WHEN prev_month_avg IS NULL THEN NULL
                ELSE ROUND((avg_days - prev_month_avg)::numeric, 1)
            END AS "Изменение"
        FROM with_changes
        ORDER BY month_date
        """
        
        try:
            result = execute_query(query, {"user_name": user_full_name})
            print(f"✅ Production acceptance time query executed, rows returned: {len(result)}")
            if result:
                print(f"📊 Sample row: {result[0]}")
            return result
        except Exception as e:
            print(f"Error executing production acceptance time query: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _get_client_orders_data(self, user_full_name: str, fiscal_year: str = "current") -> List[Dict]:
        """
        Получает данные по заказам от клиентов для пользователя за финансовый год
        
        Args:
            user_full_name: ФИО пользователя
            fiscal_year: "current" или "previous"
        """
        print(f"🔍 Executing client orders query for user: '{user_full_name}', fiscal year: {fiscal_year}")
        
        # Определяем смещение для финансового года
        year_offset = 0 if fiscal_year == "current" else -1
        
        query = f"""
        WITH client_data AS (
            SELECT
                kontr_name,
                COUNT(DISTINCT nad_zad_name) AS order_count
            FROM (
                SELECT kontr_name, nad_zad_name, "user", date_create FROM proizv_gr_artema
                WHERE "user" = :user_name
                  AND date_create IS NOT NULL
                UNION ALL
                SELECT kontr_name, nad_zad_name, "user", date_create FROM proizv_gr_zheni
                WHERE "user" = :user_name
                  AND date_create IS NOT NULL
            ) combined
            WHERE date_create >= 
                CASE 
                    WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                    THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + {year_offset}, 3, 1)
                    ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int - 1 + {year_offset}, 3, 1)
                END
            AND date_create < 
                CASE 
                    WHEN EXTRACT(MONTH FROM NOW()) >= 3 
                    THEN MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + 1 + {year_offset}, 3, 1)
                    ELSE MAKE_DATE(EXTRACT(YEAR FROM NOW())::int + {year_offset}, 3, 1)
                END
            GROUP BY kontr_name
        ),
        with_total AS (
            SELECT
                kontr_name AS "Клиент",
                order_count AS "Кол-во заказов",
                1 AS sort_order
            FROM client_data
            
            UNION ALL
            
            SELECT
                'ИТОГО' AS "Клиент",
                SUM(order_count) AS "Кол-во заказов",
                2 AS sort_order
            FROM client_data
        )
        SELECT
            "Клиент",
            "Кол-во заказов"
        FROM with_total
        ORDER BY
            sort_order,
            CASE WHEN sort_order = 1 THEN "Кол-во заказов" END DESC,
            CASE WHEN sort_order = 1 THEN "Клиент" END ASC
        """
        
        try:
            result = execute_query(query, {"user_name": user_full_name})
            print(f"✅ Client orders query executed, rows returned: {len(result)}")
            if result:
                print(f"📊 Sample row: {result[0]}")
                if len(result) > 1:
                    print(f"📊 Total row: {result[-1]}")
            return result
        except Exception as e:
            print(f"Error executing client orders query: {e}")
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



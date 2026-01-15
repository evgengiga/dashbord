-- Тестовый запрос для проверки структуры таблицы proizv_gr_artema
-- Выполните его в вашей БД чтобы проверить какие столбцы есть

SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'proizv_gr_artema';

-- Проверка наличия данных
SELECT 
    task_name,
    nad_zad_name,
    sum_project,
    kontr_name
FROM proizv_gr_artema 
LIMIT 5;








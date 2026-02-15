SELECT 
    id, 
    type_id,
    id || ' - ' || name_pl AS display_name,
    CASE WHEN type_id = 1 THEN 'Expense' ELSE 'Income' END AS type_name
FROM category
WHERE type_id IN (1, 2)
ORDER BY type_id, id;

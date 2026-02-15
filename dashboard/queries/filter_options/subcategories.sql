SELECT id, id || ' - ' || name_pl AS display_name
FROM subcategory
WHERE category_id = %(category_id)s
ORDER BY id;

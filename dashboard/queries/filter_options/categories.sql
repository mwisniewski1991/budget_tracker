SELECT id, id || ' - ' || name_pl AS display_name
FROM category
WHERE type_id = 1
ORDER BY id;

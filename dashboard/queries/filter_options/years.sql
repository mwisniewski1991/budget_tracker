SELECT DISTINCT DATE_PART('year', date)::integer as year
FROM incexp_header
ORDER BY year DESC;

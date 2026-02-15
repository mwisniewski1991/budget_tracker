with basic as(
	select
		to_char(incexp_header.date, 'YYYY.MM') as year_month,
		incexp_position.amount_absolute as amount

	from incexp_header

	left join incexp_position
		on incexp_header.id = incexp_position.header_id

	left join subcategory
		on incexp_position.subcategory_id = subcategory.id

	left join category
		on incexp_position.category_id = category.id

	where 1=1
	and (incexp_header.owner_id = %(owner)s  OR %(owner)s = -1)
	and incexp_header.type_id = 2
	and incexp_header.date >= %(date_from)s
	and incexp_header.date < %(date_to)s
	and (
		%(fixed_variable)s = 'All'
		OR (%(fixed_variable)s = 'Fixed only' AND subcategory.is_fixed_cost = 1)
		OR (%(fixed_variable)s = 'Variable only' AND subcategory.is_fixed_cost = 0)
	)
	and (
		%(income_categories)s IS NULL
		OR array_length(%(income_categories)s::text[], 1) IS NULL
		OR incexp_position.category_id = ANY(%(income_categories)s::text[])
	)
)
,basic_grouped as (
	select
		year_month,
		sum(amount) as amount
	from basic
	group by
		year_month
)
,year_months as (
select distinct to_char(incexp_header.date, 'YYYY.MM') as year_month
from incexp_header
where incexp_header.date >= %(date_from)s
  and incexp_header.date < %(date_to)s
)
select
	 year_months.year_month as "Rok miesiąc"
	,coalesce(basic_grouped.amount, 0) as "Przychody [PLN]"
from year_months
left join basic_grouped
	on year_months.year_month = basic_grouped.year_month
order by 1;

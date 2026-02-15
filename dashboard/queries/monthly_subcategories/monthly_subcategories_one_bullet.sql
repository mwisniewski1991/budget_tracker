with basic as(
	select
		to_char(incexp_header.date, 'YYYY.MM') as year_month,
		category.id as category_id,
		subcategory.id || ' - ' ||subcategory.name_pl as subcategory_name,
		incexp_position.amount_absolute as amount

	from incexp_header

	left join incexp_position
		on incexp_header.id = incexp_position.header_id

	left join type_dict
		on incexp_header.type_id = type_dict.id

	left join category
		on incexp_position.category_id = category.id

	left join subcategory
		on incexp_position.subcategory_id = subcategory.id

	left join owners
		on incexp_header.owner_id = owners.id

	left join accounts
		on incexp_header.account_id = accounts.id

	where 1=1
	and (incexp_header.owner_id = %(owner)s  OR %(owner)s = -1)
	and incexp_header.type_id = 1
	and incexp_position.category_id = %(category)s
	and incexp_header.date >= %(date_from)s
	and incexp_header.date < %(date_to)s
	and (
		%(fixed_variable)s = 'All'
		OR (%(fixed_variable)s = 'Fixed only' AND subcategory.is_fixed_cost = 1)
		OR (%(fixed_variable)s = 'Variable only' AND subcategory.is_fixed_cost = 0)
	)
)
,basic_grouped as (
	select
		year_month,
		subcategory_name,
		sum(amount) as amount
	from basic
	group by
		year_month,
		subcategory_name
)
,subcategories as (
	select subcategory.id || ' - ' ||subcategory.name_pl as subcategory_name
	from subcategory
	where exists (select 1 from category where category.id = subcategory.category_id and category.id = %(category)s )
	and subcategory.id = %(subcategory)s
)
,year_months as (
select distinct to_char(incexp_header.date, 'YYYY.MM') as year_month
from incexp_header
where incexp_header.date >= %(date_from)s
  and incexp_header.date < %(date_to)s
)
,yearmonths_subcategories as (
	select year_months.year_month, subcategories.subcategory_name
	from year_months
	cross join subcategories
)
select
	yearmonths_subcategories.subcategory_name as "Podkategoria"
	,avg(coalesce (basic_grouped.amount, 0)) as "Średnia wartość wydatków [PLN]"
from yearmonths_subcategories
left join basic_grouped
	on  yearmonths_subcategories.subcategory_name = basic_grouped.subcategory_name
	and yearmonths_subcategories.year_month         = basic_grouped.year_month
group by
	yearmonths_subcategories.subcategory_name
order by
	yearmonths_subcategories.subcategory_name;

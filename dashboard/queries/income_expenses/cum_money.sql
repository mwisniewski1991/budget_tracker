with basic as(
	select 
		to_char(incexp_header.date, 'YYYY.MM') as year_month,
		category.id as category_id,
		category.id || ' - ' ||category.name_pl as category_name,
		case when incexp_header.type_id = 1 then incexp_position.amount_absolute * -1
			 else incexp_position.amount_absolute end as amount
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
	and incexp_position.subcategory_id not in ('0010', '0011', '0013')
	and incexp_position.category_id != '20' 
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
	SELECT
    TO_CHAR(year_month, 'YYYY.MM') AS year_month
	FROM generate_series(
	    DATE '2024-01-01',
	    date_trunc('month', CURRENT_DATE),
	    INTERVAL '1 month'
	) AS year_month
)
select 
	 year_months.year_month as "Rok miesiąc"
	,sum(coalesce (basic_grouped.amount, 0)) over (order by year_months.year_month rows unbounded preceding)  as "Skumulowana gotówka [PLN]"
from year_months
left join basic_grouped
	on year_months.year_month    = basic_grouped.year_month
order by 1;
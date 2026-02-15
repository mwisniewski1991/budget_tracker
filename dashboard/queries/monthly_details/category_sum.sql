with basic as(
	select 
		extract(MONTH from incexp_header.date) as month,
		category.id as category_id,
		category.name_pl as category_name,
		case when incexp_header.type_id = 1 then incexp_position.amount_absolute * -1 else incexp_position.amount_absolute end as amount
		
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
	and (incexp_header.owner_id = %(owner)s  OR %(owner)s = '-1')
	and incexp_header.type_id = %(type_id)s
	and DATE_PART('year', incexp_header.date) = %(year)s::integer
	and (DATE_PART('month', incexp_header.date) = %(month)s OR %(month)s = -1) 
	and (incexp_position.category_id = %(category)s OR %(category)s = 'All') 
	and incexp_position.category_id  != '20'
)
select
	sum(amount) as amount
from basic;
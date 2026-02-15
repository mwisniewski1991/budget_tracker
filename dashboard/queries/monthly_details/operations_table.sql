with basic as(
	select
		incexp_header.id,
		incexp_header.date,
		owners.name_pl as owner_name,
		accounts.name_pl as account_name,
		category.id as category_id,
		subcategory.id as subcategory_id, 
		category.name_pl as category_name,
		subcategory.name_pl as subcategory_name,
		incexp_header.source,
		incexp_position.comment,
		incexp_position."connection",
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
	and (incexp_header.owner_id = %(owner)s  OR %(owner)s = '-1')
	and incexp_header.type_id = %(type_id)s
	and DATE_PART('year', incexp_header.date) = %(year)s::integer
	and (DATE_PART('month', incexp_header.date) = %(month)s OR %(month)s = -1) 
	and (incexp_position.category_id = %(category)s OR %(category)s = 'All') 
	and (incexp_position.subcategory_id = %(subcategory)s OR %(subcategory)s = 'All') 
	and incexp_position.category_id  != '20'
)
select 
	id,
	TO_CHAR(date, 'YYYY-MM-DD') as date,
	owner_name,
	account_name,
	subcategory_name,
	amount,
	source,
	comment,
	connection
from basic
order by date, id asc;


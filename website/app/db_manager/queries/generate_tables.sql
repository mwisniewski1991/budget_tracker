-- CREATE DATABASE budget_test
--     WITH
--     OWNER = mw
--     ENCODING = 'UTF8'
--     LC_COLLATE = 'pl_PL.UTF-8'
--     LC_CTYPE = 'pl_PL.UTF-8'
--     LOCALE_PROVIDER = 'libc'
--     TABLESPACE = pg_default
--     CONNECTION LIMIT = -1
--     IS_TEMPLATE = False;

-- OWNERS
DROP VIEW IF EXISTS public.owners_accounts;
DROP VIEW IF EXISTS public.type_category_subcategory;
DROP VIEW IF EXISTS public.incexp_view;
DROP TABLE IF EXISTS public.incexp_position;
DROP TABLE IF EXISTS public.incexp_header;
DROP TABLE IF EXISTS public.subcategory;
DROP TABLE IF EXISTS public.category;
DROP TABLE IF EXISTS public.type_dict;
DROP TABLE IF EXISTS public.accounts;
DROP TABLE IF EXISTS public.owners;


-- OWNERS
CREATE TABLE IF NOT EXISTS public.owners
(
    id character(2) not null primary key,
    name_pl character(50) COLLATE pg_catalog."default"
);


-- ACCOUNTS 
CREATE TABLE IF NOT EXISTS public.accounts
(
    id character(2) not null primary key,
    name_pl character(50) COLLATE pg_catalog."default",
    owner_id character(2)  references public.owners(id) not null
);


--  EVENT TYPE
CREATE TABLE IF NOT EXISTS public.type_dict
(
    id character(1) not null primary key,
    name_eng character(50) COLLATE pg_catalog."default",
    name_pl character(50) COLLATE pg_catalog."default"
);


-- CATEGORY 
CREATE TABLE IF NOT EXISTS public.category
(
    id char(2) NOT NULL PRIMARY KEY,
    name_pl character(100) COLLATE pg_catalog."default" not null,
    type_id character(1) references public.type_dict(id) not null

);


-- SUBCATEGORY 
CREATE TABLE IF NOT EXISTS public.subcategory
(
    id character(4) NOT NULL PRIMARY KEY,
    name_pl character(100) COLLATE pg_catalog."default" NOT NULL,
    category_id char(2) references public.category(id) NOT NULL,
    is_fixed_cost integer NOT NULL
);


-- INCOME EXPENSE
CREATE TABLE IF NOT EXISTS public.incexp_header
(
    id serial primary key,
    date date NOT NULL,
    source character(100) COLLATE pg_catalog."default",
    type_id character(1) references public.type_dict(id) NOT NULL,
    owner_id character(2) references public.owners(id) NOT NULL,
    account_id character(2) references public.accounts(id) NOT NULL,
    created_at timestamptz DEFAULT now(),
    created_at_utc timestamp DEFAULT (now() at time zone 'utc'),
    updated_at timestamptz DEFAULT now(),
    updated_at_utc timestamp DEFAULT (now() at time zone 'utc')

);

CREATE TABLE IF NOT EXISTS public.incexp_position
(
    header_id integer references public.incexp_header(id) not null,
    position_id integer not null,
    category_id character(2) references public.category(id) NOT NULL,
    subcategory_id character(4) references public.subcategory(id) NOT NULL,
    amount decimal NOT NULL,
    amount_absolute decimal GENERATED ALWAYS AS (abs(amount)) STORED,
    amount_full integer GENERATED ALWAYS AS (amount * 100) STORED,
    comment character(200) COLLATE pg_catalog."default",
    connection character(100) COLLATE pg_catalog."default",
    created_at timestamptz DEFAULT now(),
    created_at_utc timestamp DEFAULT (now() at time zone 'utc'),
    updated_at timestamptz DEFAULT now(),
    updated_at_utc timestamp DEFAULT (now() at time zone 'utc')

    constraint header_pos_id PRIMARY KEY  (header_id, position_id)
);



-- VIEWS
CREATE view owners_accounts as (
    SELECT 
	owners.id as owner_id,
	owners.name_pl as owner_name_pl,
	accounts.id as account_id,
	accounts.name_pl as account_name_pl 

    from public.owners as owners
    left join public.accounts as accounts
        on owners.id = accounts.owner_id	
);

CREATE VIEW type_category_subcategory as 
(
	SELECT
	type_dict.id as tpy_id,
	type_dict.name_pl as type_name_pl,
	category.id as category_id,
	category.name_pl as category_name_pl,
	subcategory.id as subcategory_id,
	subcategory.name_pl as subcategory_name_pl,
	subcategory.is_fixed_cost

	FROM public.subcategory AS subcategory
	INNER JOIN public.category AS category
		ON category.id = subcategory.category_id
	INNER JOIN public.type_dict as type_dict 
		on category.type_id = type_dict.id

	ORDER BY type_dict.id, category.id, subcategory.id
);



CREATE VIEW incexp_view AS 
(
    select

	incexp_position.header_id,
	incexp_position.position_id,

	owners.id as owner_id,
    owners.name_pl as owner, 
	
    accounts.id as account_id,
	accounts.name_pl as account,
	
	incexp_header.date,
    incexp_header.source,

	type_dict.name_pl as type,
	category.name_pl as category,
	subcategory.name_pl as subcategory,

    case 
        when incexp_header.type_id = '1' then incexp_position.amount_absolute * -1
        when incexp_header.type_id = '2' then incexp_position.amount_absolute
    end as amount_absolute,

	incexp_position.comment,
	incexp_position.connection
	
    from public.incexp_header as incexp_header

	inner join public.incexp_position as incexp_position
		on incexp_header.id = incexp_position.header_id

    left join public.owners as owners
        on incexp_header.owner_id = owners.id

    left join public.accounts as accounts  
        on incexp_header.account_id = accounts.id

    left join public.type_dict as type_dict
        on incexp_header.type_id = type_dict.id

    left join public.category as category
        on incexp_position.category_id = category.id

    left join public.subcategory as subcategory
        on incexp_position.subcategory_id = subcategory.id
);
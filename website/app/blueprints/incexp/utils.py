from ...models import INCEXP_header, INCEXP_position
from sqlalchemy import and_

def master_slave_decrypt(value: str) -> list:
    '''Function decrypt master value (e.g. '01') and slave value (e.g. '0001') from format '01_0001'. 
    Functions use for 
        - category and subcategory (e.g. '01_0001')
        - owners and accounts (e.g. '1_01')

    :param value: string for decrypting
    :returns: list[str, str]
    '''
    return value.split('_')

def master_slave_encrypt(master_value: str, slave_value:str) -> list:
    '''Function encrypt master value (e.g. '01') and slave value (e.g. '0001') into format '01_0001'. 
    Functions use for 
        - category and subcategory (e.g. '01_0001')
        - owners and accounts (e.g. '1_01')

    :param value_one: category_id from models
    :param value_second: subcategory_id from models
    :returns: str
    '''
    return f'{master_value}_{slave_value}'


def incexp_query_existings(
                    results_limit:int,
                    owner_id:int, 
                    account_id:str, 
                    type_id:int = None,
                    created_date_from:str = None,
                    created_date_to:str = None,
                    source:str = None,
                    comment:str = None,
                    connection:str = None,
                ) -> list:
                    
    incexp_list = (INCEXP_header
            .query
            .filter(and_(INCEXP_header.owner_id==owner_id, INCEXP_header.account_id==account_id))
            )

    if type_id:
        incexp_list = incexp_list.filter(INCEXP_header.type_id == type_id)

    if created_date_from:
        incexp_list = incexp_list.filter(INCEXP_header.date >= created_date_from)

    if created_date_to:
        incexp_list = incexp_list.filter(INCEXP_header.date <= created_date_to)
    
    if source:
        incexp_list = incexp_list.filter(INCEXP_header.source.ilike(f'%{source}%'))

    if created_date_from:
        incexp_list = incexp_list.filter(INCEXP_header.date >= created_date_from)

    if comment:
        incexp_list = incexp_list.filter(INCEXP_header.incexp_positions.any(INCEXP_position.comment.ilike(f"%{comment}%")))

    if connection:
        incexp_list = incexp_list.filter(INCEXP_header.incexp_positions.any(INCEXP_position.connection.ilike(f"%{connection}%")))

    return (incexp_list
                    .order_by(INCEXP_header.date.desc(), INCEXP_header.id)
                    .limit(results_limit)
                   ).all()


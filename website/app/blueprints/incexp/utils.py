from ... import db
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

def master_slave_encrypt(master_value: str, slave_value:str) -> str:
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
                    category_id:str = None,
                    subcategory_id:str = None,
                    created_date_from:str = None,
                    created_date_to:str = None,
                    source:str = None,
                    comment:str = None,
                    connection:str = None,
                ) -> list:
    '''
    Function for query Incomes and Expensed models in complex way.

    :param results_limit: how many records will be return
    :param owners_id: integer with id of one of owners
    :param account_id: string with account id from models (e.b '01')
    :param type_id: id for income (value: 1) or expenses (value 2)
    :param category_id: id for income or expense category (value example: '01')
    :param subcategory_id: id for income or expense subcategory (value example: '0001') 
    :param created_date_from: from which date results will be return
    :param created_date_to: to which date results will be return
    :param source: text with source information
    :param comment: text to filter comment column in model
    :param connection: text to filter connection column in model
    :return list: list if app.models class
    '''
                    
    incexp_list = (INCEXP_header
            .query
            .filter(and_(INCEXP_header.owner_id==owner_id, INCEXP_header.account_id==account_id))
            )

    if type_id:
        incexp_list = incexp_list.filter(INCEXP_header.type_id == type_id)

    if category_id:
        incexp_list = incexp_list.filter(INCEXP_header.incexp_positions.any(INCEXP_position.category_id == category_id))

    if subcategory_id:
        incexp_list = incexp_list.filter(INCEXP_header.incexp_positions.any(INCEXP_position.subcategory_id == subcategory_id))

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
                    .order_by(INCEXP_header.date.desc(), INCEXP_header.id.desc())
                    .limit(results_limit)
                   ).all()

def incexp_modify_new(
        incexp_header_id: int,
        incexp_forms: dict,
    ) -> None:

    incexp = (INCEXP_header
                .query
                .filter(INCEXP_header.id==incexp_header_id)
            ).first()

    incexp.date  = incexp_forms.date.data,
    incexp.source = incexp_forms.source.data,
    incexp.type_id = incexp_forms.type.data,

    for index, position in enumerate(incexp_forms.positions):
        if not position.category.data is None: 
            category_id, subcategory_id = master_slave_decrypt(position.category.data)    

            incexp.incexp_positions[index].category_id = category_id,
            incexp.incexp_positions[index].subcategory_id = subcategory_id,
            incexp.incexp_positions[index].amount = position.amount.data,
            incexp.incexp_positions[index].comment = position.comment.data,
            incexp.incexp_positions[index].connection = position.connection.data,

    db.session.commit()

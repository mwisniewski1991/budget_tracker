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
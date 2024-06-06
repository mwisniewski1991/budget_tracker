def category_subcategory_decrypt(value: str) -> list:
    '''Function decrypt category_id (e.g. '01') and subcategory_id (e.g. '0001') from format '01_0001'. 

    :param value: string for decrypting
    :returns: list[str, str]

    '''
    return value.split('_')

def category_subcategory_encrypt(value_one: str, value_second:str) -> list:
    '''Function encrypt category_id (e.g. '01') and subcategory_id (e.g. '0001') into format '01_0001'. 

    :param value_one: category_id from models
    :param value_second: subcategory_id from models
    :returns: str
    
    '''
    return f'{value_one}_{value_second}'
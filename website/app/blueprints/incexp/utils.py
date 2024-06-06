def category_subcategory_decrypt(value: str) -> list:
    return value.split('_')

def category_subcategory_encrypt(value_one: str, value_second:str) -> list:
    return f'{value_one}_{value_second}'
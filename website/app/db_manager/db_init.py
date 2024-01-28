from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from models.models import Owners, Accounts, Type, Category, Subategory 
import csv
from pathlib import Path

def get_database_uri() -> str:
    '''
        Return URI for database.
    '''
    if not Path('config/config.ini').exists():
        raise FileNotFoundError('File config/config.ini does not exists!')
    
    config = ConfigParser()
    config.read('config/config.ini')
    config_data = config['DATABASE']

    engine:str = config_data['engine']
    user:str = config_data['user']
    password:str = config_data['password']
    host:str = config_data['host']
    port:str = config_data['port']
    database_name:str = config_data['database_name']

    return f"{engine}://{user}:{password}@{host}:{port}/{database_name}"

def create_tables(engine) -> None:
    query:str = open('app/db_manager/queries/generate_tables.sql').read()
    with engine.connect() as conn:
        conn.execute(text(query))
        conn.commit()

def parse_csv(link:str) -> csv.reader:
    with open(link, 'r') as csv_file:
        data = csv.reader(csv_file, delimiter=',', )
        next(data) #skip header
        return [row for row in data]

def add_owners(session) -> None:
    data = parse_csv('app/db_manager/data/owners.csv')
    
    for row in data:
        name_pl, id = row
        new_owner = Owners(id=id, name_pl=name_pl)
        session.add(new_owner)  
    session.commit()

def add_accounts(session) -> None:
    data = parse_csv('app/db_manager/data/accounts.csv')
    for row in data:
        id, name_pl, owner_id = row
        new_account = Accounts(id=id, name_pl=name_pl, owner_id=owner_id)
        session.add(new_account)
    session.commit()

def add_types(session) -> None:
    data = parse_csv('app/db_manager/data/types.csv')
    for row in data:
        id, name_eng, name_pl = row
        new_type = Type(id=id, name_eng=name_eng, name_pl=name_pl)
        session.add(new_type)
    session.commit()
    
def add_categories(session) -> None:
    data = parse_csv('app/db_manager/data/categories.csv')
    for row in data:
        name_pl, id, type_id = row
        new_category = Category(id=id, name_pl=name_pl, type_id=type_id)
        session.add(new_category)
    session.commit()

def add_subcategorues(session) -> None:
    data = parse_csv('app/db_manager/data/subcategories.csv')
    for row in data:
        id, name_pl, category_id, is_fixed_cost = row
        new_subcategory = Subategory(id=id, name_pl=name_pl, category_id=category_id, is_fixed_cost=is_fixed_cost)
        session.add(new_subcategory)
    session.commit()


def main() -> None:
    database_uri = get_database_uri()
    engine = create_engine(database_uri)
    session = sessionmaker(bind=engine)
    s = session()

    create_tables(engine)

    add_owners(s)
    add_accounts(s)
    add_types(s)
    add_categories(s)
    add_subcategorues(s)
    
if __name__ == '__main__':
    main()
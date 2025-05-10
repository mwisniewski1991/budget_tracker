from flask import Blueprint, render_template, request, current_app
from ... import db
from ...models import Owners, Accounts, INCEXP_header, INCEXP_position, Category, Subategory
from ..incexp.forms import Incexp_header_form
import csv
from datetime import datetime
from ..incexp.utils import master_slave_encrypt, master_slave_decrypt, incexp_query_existings
from ..incexp.constants import DEFAULT_EMPTY_CHOICE
import logging

bulk_import = Blueprint(
    'bulk_import',
    __name__,
    template_folder='templates',
    static_folder="static"
)


@bulk_import.route('/', methods=['GET'])
def get_bulk_import():
    accounts = Accounts.query.filter(Accounts.is_active == 1).order_by(Accounts.owner_id, Accounts.id).all()
    choices_list = [f'{account.owner_id}_{account.id}' for account in accounts]
    incexp_header_form = Incexp_header_form()
    incexp_header_form.owner_accounts_ids.choices = choices_list

    owner_account_ids = current_app.config['DEFAULT_OWNER_ACCOUNT_IDS']

    return render_template("bulk_import/home.html.jinja", 
                            incexp_header_form=incexp_header_form, 
                            accounts=accounts,
                            owner_account_ids=owner_account_ids
                            )

@bulk_import.route('/preview', methods=['POST'])
def preview_bulk_import():

    if 'csv_file' not in request.files:
        return 'Nie przesłano pliku', 400
        
    file = request.files['csv_file']
    if file.filename == '':
        return 'Nie wybrano pliku', 400

    csv_file = file.stream.read().decode("UTF-8").splitlines()
    csv_reader = csv.DictReader(csv_file, delimiter=',')

    forms = []
    for row in csv_reader:
        incexp_header_form = Incexp_header_form()
        
        # Parsowanie daty
        date_str = row['Data transakcji']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Określenie typu i kwoty
        amount = 0
        if row['Obciążenia']:
            type_id = 1  # Wydatek
            amount = abs(float(row['Obciążenia'].replace(',', '.')))
        elif row['Uznania']:
            type_id = 2  # Przychód
            amount = abs(float(row['Uznania'].replace(',', '.')))


        categories_subcategories = (db.session
                                    .query(Category.id,
                                            Category.name_pl,
                                            Subategory.id,
                                            Subategory.name_pl,
                                            )
                                    .join(Subategory, Category.id == Subategory.category_id)
                                    .filter(Category.type_id == type_id)
                                    .order_by(Category.id, Subategory.id)
                                ).all()

        choices_list = [(master_slave_encrypt(cat_sub[0], cat_sub[2]),  f'{cat_sub[1].strip()} : {cat_sub[3].strip()}') for cat_sub in categories_subcategories]
        empty_choice = [(master_slave_encrypt('00','0000'), '')]
        choices_list = [*empty_choice, *choices_list, *empty_choice]
            
            
        # Ustawienie wartości formularza
        incexp_header_form.date.data = date
        incexp_header_form.type.data = str(type_id)
        incexp_header_form.source.data = row['Opis']
        incexp_header_form.positions[0].amount.data = amount
        incexp_header_form.positions[0].category.choices = choices_list


        for position in incexp_header_form.positions:
            position.category.choices = choices_list
        forms.append(incexp_header_form)
        
        logging.info(incexp_header_form)

    return render_template(
        "bulk_import/preview.html.jinja",
        forms=forms,
    )

@bulk_import.route('/incexp', methods=['POST'])
def add_incexp():
    incexp_header_form = Incexp_header_form()
    owner_id, account_id =  master_slave_decrypt(incexp_header_form.owner_accounts_ids.data)

    if any([position.amount.data for position in incexp_header_form.positions]):
        new_incexp_header = INCEXP_header(
            date  = incexp_header_form.date.data,
            source = incexp_header_form.source.data,
            owner_id = owner_id,
            account_id = account_id,
            type_id = incexp_header_form.type.data,
        )
        db.session.add(new_incexp_header)
        db.session.commit()

        for index, position in enumerate(incexp_header_form.positions):
            if position.category.data != DEFAULT_EMPTY_CHOICE: 
                category_id, subcategory_id = master_slave_decrypt(position.category.data)    

                new_incexp_position = INCEXP_position(
                    header_id = new_incexp_header.id,
                    position_id = index + 1,
                    category_id = category_id,
                    subcategory_id = subcategory_id,
                    amount = position.amount.data,
                    comment = position.comment.data,
                    connection = position.connection.data,
                )
                db.session.add(new_incexp_position)
        db.session.commit()

    return "DODANE"

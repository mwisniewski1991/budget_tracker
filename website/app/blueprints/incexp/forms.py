from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FormField, DateField, SelectField, FloatField, DecimalField
from datetime import datetime

class Incexp_position_form(FlaskForm):
    category = SelectField('Kategoria', choices=[])
    amount = DecimalField('amount', places=2,  render_kw={'step': '0.01', 'min': '0.00', })
    comment = StringField('comment', render_kw={"placeholder": "Komentarz"})
    connection = StringField('connection', render_kw={"placeholder": "Powiązanie",})


class Incexp_header_form(FlaskForm):
    owner_accounts_ids = SelectField('owner_accounts_ids', choices=[])
    type = SelectField('Typ', name='type-id', choices=[(1, 'Wydatek'), (2, 'Dochód')], render_kw={})
    date = DateField('Data', default=datetime.today)
    source = StringField('Source', render_kw={"placeholder": "Źródło"})
    positions = FieldList(FormField(Incexp_position_form), min_entries=6, max_entries=6)
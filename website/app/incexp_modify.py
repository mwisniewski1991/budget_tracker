def modify_header(header_model, new_model) -> None:
    new_date  = new_model.form['date']
    new_source = new_model.form['source']
    new_type_id = new_model.form['type_id']
    
    if new_date != header_model.date.strftime("%Y-%m-%d"):
        header_model.date = new_date
    if new_source != header_model.source.strip():
        header_model.source = new_source
    if new_type_id != header_model.type_id:
        header_model.type_id = new_type_id

def modify_position(position_model, new_model, i) -> None:

    new_category_id =  new_model.form[f'category_{i}']
    new_subcategory_id =  new_model.form[f'subcategory_{i}']
    new_amount =  float(new_model.form[f'amount_{i}'])
    new_comment = new_model.form[f'comment_{i}']
    new_connection = new_model.form[f'connection_{i}']

    if new_category_id !=  position_model.category_id:
        position_model.category_id = new_category_id

    if new_subcategory_id != position_model.subcategory_id:
        position_model.subcategory_id = new_subcategory_id
    
    if new_amount != position_model.amount:
        position_model.amount = new_amount

    if new_comment != position_model.comment.strip():
        position_model.comment = new_comment
    
    if new_connection != position_model.connection.strip():
        position_model.connection = new_connection
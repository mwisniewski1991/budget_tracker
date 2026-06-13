from app.models import Category, Subategory


def _create_subcategory(client, type_id, category_name, subcategory_name):
    client.post(f'/type/{type_id}/category', data={'category_name_pl': category_name})
    with client.application.app_context():
        category = Category.query.filter_by(name_pl=category_name, type_id=type_id).first()
        category_id = category.id

    client.post(
        f'/type/{type_id}/category/{category_id}/subcategory',
        data={'new_subcategory_name': subcategory_name},
    )
    with client.application.app_context():
        subcategory = Subategory.query.filter_by(
            name_pl=subcategory_name,
            category_id=category_id,
        ).first()
        return category_id, subcategory.id


def test_inactive_subcategory_hidden_in_cat_sub_options(client):
    _create_subcategory(client, 1, 'Expense Cat', 'Active Subcategory')
    _create_subcategory(client, 1, 'Expense Cat 2', 'Inactive Subcategory')

    with client.application.app_context():
        inactive = Subategory.query.filter_by(name_pl='Inactive Subcategory').first()
        inactive.is_active = 0
        from app import db
        db.session.commit()

    response = client.get('/incexp/cat-sub-options?type-id=1')
    assert response.status_code == 200
    assert b'Active Subcategory' in response.data
    assert b'Inactive Subcategory' not in response.data


def test_inactive_subcategory_hidden_in_subcategories_dropdown(client):
    category_id, _ = _create_subcategory(client, 1, 'Filter Cat', 'Visible Sub')
    with client.application.app_context():
        hidden = Subategory(
            category_id=category_id,
            name_pl='Hidden Sub',
            is_active=0,
        )
        from app import db
        db.session.add(hidden)
        db.session.commit()

    response = client.get(f'/incexp/subcategories?category-id={category_id}')
    assert response.status_code == 200
    assert b'Visible Sub' in response.data
    assert b'Hidden Sub' not in response.data

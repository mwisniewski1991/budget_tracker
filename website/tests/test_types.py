import pytest
from website.app import create_app, db
from website.app.models import Category, Subategory

def test_types_home(client):
    response = client.get('/type/2/category')
    assert response.status_code == 200
    assert b'Test Category' in response.data

def test_add_category(client):
    response = client.post('/type/2/category', data={
        'category_name_pl': 'New Test Category'
    })
    assert response.status_code == 302  # Redirect status code
    
    # Verify the category was added
    with client.application.app_context():
        category = Category.query.filter_by(name_pl='New Test Category').first()
        assert category is not None
        assert category.name_pl == 'New Test Category'
        assert category.type_id == '2'

def test_edit_category(client):
    # First get the test category
    with client.application.app_context():
        category = Category.query.filter_by(name_pl='Test Category').first()
        category_id = category.id

    response = client.put(f'/type/2/category/{category_id}', data={
        'category_name_pl': 'Updated Test Category'
    })
    assert response.status_code == 200
    
    # Verify the category was updated
    with client.application.app_context():
        updated_category = Category.query.get(category_id)
        assert updated_category.name_pl == 'Updated Test Category'

def test_add_subcategory(client):
    # Get the test category id
    with client.application.app_context():
        category = Category.query.filter_by(name_pl='Test Category').first()
        category_id = category.id

    response = client.post(f'/type/2/category/{category_id}/subcategory', data={
        'new_subcategory_name': 'New Test Subcategory'
    })
    assert response.status_code == 302  # Redirect status code
    
    # Verify the subcategory was added
    with client.application.app_context():
        subcategory = Subategory.query.filter_by(name_pl='New Test Subcategory').first()
        assert subcategory is not None
        assert subcategory.name_pl == 'New Test Subcategory'
        assert subcategory.category_id == category_id

def test_edit_subcategory(client):
    # Get the test subcategory
    with client.application.app_context():
        category = Category.query.filter_by(name_pl='Test Category').first()
        subcategory = Subategory.query.filter_by(name_pl='Test Subcategory').first()

    response = client.put(f'/type/2/category/{category.id}/subcategory/{subcategory.id}', data={
        'subcategory_name_pl': 'Updated Test Subcategory',
        'subcategory_fixed_cost': 'true'
    })
    assert response.status_code == 200
    
    # Verify the subcategory was updated
    with client.application.app_context():
        updated_subcategory = Subategory.query.get(subcategory.id)
        assert updated_subcategory.name_pl == 'Updated Test Subcategory'
        assert updated_subcategory.is_fixed_cost == 'true'

import pytest
from app.models import Category, Subategory

def test_types_home(client):
    """Test GET request to types home page"""
    response = client.get('/type/2/category')
    assert response.status_code == 200
    assert b'Kategorie i podkategorie' in response.data

def test_add_category(client):
    """Test POST request to create a new category"""
    response = client.post('/type/2/category', data={
        'category_name_pl': 'Test Category'
    })
    assert response.status_code == 302  # Redirect after successful creation
    assert response.headers['Location'] == '/type/2/category'
    
    # Verify the category was added
    with client.application.app_context():
        category = Category.query.filter_by(name_pl='Test Category').first()
        assert category is not None
        assert category.name_pl == 'Test Category'
        assert category.type_id == 2

def test_edit_category(client):
    """Test PUT request to edit a category"""
    # First get the test category
    with client.application.app_context():
        category = Category.query.filter_by(name_pl='Test Category').first()
        category_id = category.id

    response = client.put(f'/type/2/category/{category_id}', data={
        'category_name_pl': 'Updated Test Category'
    })
    assert response.status_code == 200
    with client.application.app_context():
        category = Category.query.filter_by(name_pl='Updated Test Category').first()
        assert category is not None
        assert category.name_pl == 'Updated Test Category'
        assert category.type_id == 2


def test_add_subcategory(client):
    """Test POST request to add subcategory to category"""
    with client.application.app_context():
        category = Category.query.filter_by(name_pl='Updated Test Category').first()
        category_id = category.id

    response = client.post(f'/type/2/category/{category_id}/subcategory', data={
        'new_subcategory_name': 'Test Subcategory'
    })
    assert response.status_code == 302  # Redirect after successful creation
    assert response.headers['Location'] == '/type/2/category'
    
    # Verify the subcategory was added
    with client.application.app_context():
        subcategory = Subategory.query.filter_by(name_pl='Test Subcategory').first()
        assert subcategory is not None
        assert subcategory.name_pl == 'Test Subcategory'
        assert subcategory.category_id == category_id

def test_edit_subcategory(client):
    """Test PUT request to edit a subcategory"""
    with client.application.app_context():
        category = Category.query.filter_by(name_pl='Updated Test Category').first()
        subcategory = Subategory.query.filter_by(name_pl='Test Subcategory').first()

    response = client.put(f'/type/2/category/{category.id}/subcategory/{subcategory.id}', data={
        'subcategory_name_pl': 'Updated Test Subcategory',
        'subcategory_fixed_cost': 1
    })
    assert response.status_code == 200
    with client.application.app_context():
        subcategory = Subategory.query.filter_by(name_pl='Updated Test Subcategory').first()
        assert subcategory is not None
        assert subcategory.name_pl == 'Updated Test Subcategory'
        assert subcategory.is_fixed_cost == 1

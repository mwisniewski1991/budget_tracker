def test_owners_home_get(client):
    """Test GET request to owners home page"""
    response = client.get("/owners/")
    assert response.status_code == 200
    assert b'owners' in response.data

def test_add_owner(client):
    """Test POST request to create a new owner"""
    response = client.post("/owners/", data={
        'owner_name_pl': 'Test Owner'
    })
    assert response.status_code == 302  # Redirect after successful creation
    assert response.headers['Location'] == '/owners'

def test_edit_owner(client):
    """Test PUT request to edit an owner"""
    # First create an owner
    client.post("/owners/", data={'owner_name_pl': 'Original Name'})
    
    # Then edit it
    response = client.put("/owners/1", data={
        'owner_name_pl': 'Updated Name'
    })
    assert response.status_code == 200
    assert b'Updated Name' in response.data

def test_add_account_to_owner(client):
    """Test POST request to add account to owner"""
    # First create an owner
    client.post("/owners/", data={'owner_name_pl': 'Test Owner'})
    
    # Then add an account
    response = client.post("/owners/1/accounts", data={
        'account_name_pl': 'Test Account'
    })
    assert response.status_code == 302  # Redirect after successful creation
    assert response.headers['Location'] == '/owners'


# def test_edit_account(client):
#     """Test PUT request to edit an account"""
#     # Create owner and account
#     client.post("/owners/", data={'owner_name_pl': 'Test Owner'})
#     client.post("/owners/1/accounts", data={'account_name_pl': 'Original Account'})
    
#     # Edit account
#     response = client.put("/owners/1/accounts/1", data={
#         'account_name_pl': 'Updated Account',
#         'account_is_active': 'true'
#     })
#     assert response.status_code == 200
#     assert b'Updated Account' in response.data

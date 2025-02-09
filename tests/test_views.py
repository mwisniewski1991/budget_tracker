def test_incexp(client):
    response = client.get("/incexp/")
    assert response.status_code == 200

def test_accounts_results(client):
    response = client.get("/accounts-results/")
    assert response.status_code == 200

def test_owners(client):
    response = client.get("/owners/")
    assert response.status_code == 200

def test_type_2_category(client):
    response = client.get("/type/2/category")
    assert response.status_code == 200

def test_type_1_category(client):
    response = client.get("/type/1/category")
    assert response.status_code == 200

def test_owner(client):
    response = client.get("/owner/")
    assert response.status_code == 404




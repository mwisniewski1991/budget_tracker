import pytest
import os 
from website.app import create_app, db
from dotenv import load_dotenv

@pytest.fixture
def app():
    # Load test environment variables
    load_dotenv('tests/.env.test')
    
    app = create_app()

    with app.app_context():
        db.create_all()
        yield app



@pytest.fixture
def client(app):
    return app.test_client()
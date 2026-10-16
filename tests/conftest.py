from fastapi.testclient import TestClient
from main import app
import pytest
from app.models.base import Base
from tests.database import test_db
from sqlalchemy import text

@pytest.fixture
def test_client():
    with TestClient(app=app) as client:
        yield client

@pytest.fixture(scope='session', autouse=True)
def create_tables():
    Base.metadata.create_all(bind=test_db)
    yield
    Base.metadata.drop_all(bind=test_db)

@pytest.fixture(autouse=True)
def clean_db():
    yield

    with test_db.begin() as conn:
        conn.execute(text("""TRUNCATE TABLE
        monitors,
        monitor_checks
        RESTART IDENTITY CASCADE"""
        ))

@pytest.fixture
def test_monitor(test_client: TestClient):
    response = test_client.post("/monitors",
                                json={
                                    'name': 'google',
                                    'url': 'https://www.google.com/'
                                }
                                )
    assert response.status_code == 201
    return response.json()

@pytest.fixture
def test_check_monitor(test_client: TestClient, test_monitor):
    response = test_client.post(f"/monitors/{test_monitor['id']}/checks")
    data = response.json()
    assert response.status_code == 200
    assert data['status_code'] == 200
    assert data['is_success'] == True
    assert data['error_message'] == None
    return data

@pytest.fixture
def test_check_monitor2(test_client: TestClient, test_monitor):
    response = test_client.post(f"/monitors/{test_monitor['id']}/checks")
    data = response.json()
    assert response.status_code == 200
    assert data['status_code'] == 200
    assert data['is_success'] == True
    assert data['error_message'] == None
    return data

@pytest.fixture
def test_check_monitor3(test_client: TestClient, test_monitor):
    response = test_client.post(f"/monitors/{test_monitor['id']}/checks")
    data = response.json()
    assert response.status_code == 200
    assert data['status_code'] == 200
    assert data['is_success'] == True
    assert data['error_message'] == None
    return data
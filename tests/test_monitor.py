from fastapi.testclient import TestClient
import pytest

def test_get_monitors(test_client: TestClient, test_monitor):
    response = test_client.get("/monitors")
    data = response.json()
    assert response.status_code == 200
    assert data[0]['name'] == 'google'
    assert data[0]['url'] == 'https://www.google.com/'

@pytest.mark.parametrize(
        argnames='payload, exp_status_code',
        argvalues=[
            [{'name': None, 'url': 'https://www.google.com/'}, 201],
            [{'name': 'string', 'url': 'https://www.google.com/'}, 201],
            [{'name': 'string', 'url': 'noturl'}, 422]
        ]
)
def test_add_monitor(test_client: TestClient,
                     payload, 
                     exp_status_code
                     ):
    response = test_client.post("/monitors", json=payload)
    assert response.status_code == exp_status_code

def test_get_existing_monitor(test_client: TestClient, test_monitor):
    response = test_client.get(f"/monitors/{test_monitor['id']}")
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == 'google'
    assert data['url'] == 'https://www.google.com/'

def test_get_unexisting_monitor(test_client: TestClient):
    response = test_client.get("/monitors/9999")
    assert response.status_code == 404

@pytest.mark.parametrize(
        argnames='payload, exp_status_code',
        argvalues=[
            [{'url': 'https://www.google.com/'}, 200],
            [{'name': 'new name', 'url': 'https://www.google.com/'}, 200],
            [{'name': 'new name'}, 200]
        ]
)
def test_change_monitor(
    test_client: TestClient, 
    test_monitor,
    payload, 
    exp_status_code
    ):
    response = test_client.patch(f"/monitors/{test_monitor['id']}",
                                 json=payload)
    assert response.status_code == exp_status_code

def test_delete_monitor(test_client: TestClient, test_monitor):
    response = test_client.get("/monitors")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1

    response = test_client.delete(f"/monitors/{test_monitor['id']}")
    assert response.status_code == 204

    response = test_client.get("/monitors")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 0

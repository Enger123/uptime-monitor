from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

def test_check_monitor(test_client: TestClient, test_monitor):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.is_success = True
    
    with patch('app.services.monitor_check.httpx.get',
               return_value=mock_response
               ):
        response = test_client.post(f"/monitors/{test_monitor['id']}/checks")
    data = response.json()
    assert response.status_code == 200
    assert data['status_code'] == 200
    assert data['is_success'] is True
    assert data['error_message'] is None

def test_list_checks_unexisting_monitor(test_client: TestClient):
    response = test_client.get("/monitors/9999/checks")
    assert response.status_code == 404

def test_list_checks_monitor(
        test_client: TestClient, 
        test_monitor, 
        test_check_monitor,
        test_check_monitor2,
        test_check_monitor3
        ):
    response = test_client.get(f"/monitors/{test_monitor['id']}/checks", 
                               params={'limit': 2}
                               )
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_list_checks_monitor_order(
    test_client: TestClient,
    test_monitor,
    test_check_monitor,
    test_check_monitor2,
    test_check_monitor3
):
    response = test_client.get(f"/monitors/{test_monitor['id']}/checks")
    data = response.json()
    assert response.status_code == 200
    assert data[0]['id'] == 3
    assert data[1]['id'] == 2
    assert data[2]['id'] == 1
    
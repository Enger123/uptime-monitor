from fastapi.testclient import TestClient

def test_check_monitor(test_client: TestClient, test_monitor):
    response = test_client.post(f"/monitors/{test_monitor['id']}/checks")
    data = response.json()
    assert response.status_code == 200
    assert data['status_code'] == 200
    assert data['is_success'] == True
    assert data['error_message'] == None

def test_check_unexisting_monitor(test_client: TestClient):
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
    
import requests

api_url = 'http://localhost:8001'

def test_healthcheck():
    response = requests.get(f'{api_url}/__health')
    assert response.status_code == 200

class TestLoyalty():
    def test_get_empty_loyalty(self):
        response = requests.get(f'{api_url}/v1/loyalties')
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_create_loyalty(self):
        body = {"status": "New status", "nameLoyalty": "Text"}
        response = requests.post(f'{api_url}/v1/loyalties', json=body)
        assert response.status_code == 200
        assert response.json().get('status') == 'New status'
        assert response.json().get('nameLoyalty') == 'Text'
        assert response.json().get('id') == 0

    def test_get_loyalty_by_id(self):
        response = requests.get(f'{api_url}/v1/loyalties/0')
        assert response.status_code == 200
        assert response.json().get('status') == 'New status'
        assert response.json().get('nameLoyalty') == 'Text'
        assert response.json().get('id') == 0

    def test_get_loyalty(self):
        response = requests.get(f'{api_url}/v1/loyalties')
        assert response.status_code == 200
        assert len(response.json()) == 1
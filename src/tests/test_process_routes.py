import pytest
from API.routes.process_routes import scraper_bp
from flask import Flask

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(scraper_bp)
    with app.test_client() as client:
        yield client

def test_get_processo_tjal(client):
    response = client.get('/api/processo', json={
        'process_number': '0710802-55.2018.8.02.0001',
        'tribunal_name': 'TJAL'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "grau_1" in data
    assert "grau_2" in data

def test_get_processo_tjce(client):
    response = client.get('/api/processo', json={
        'process_number': '0070337-91.2008.8.06.0001',
        'tribunal_name': 'TJCE'
    })
    assert response.status_code == 200
    data = response.get_json()

    assert "grau_1" in data
    assert "grau_2" in data

def test_get_processo_unsupported_tribunal(client):
    response = client.get('/api/processo', json={
        'process_number': '0710802-55.2018.8.02.0001',
        'tribunal_name': 'TJSP'  
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Nome do Tribunal não foi encontrado ou não existe!"


    
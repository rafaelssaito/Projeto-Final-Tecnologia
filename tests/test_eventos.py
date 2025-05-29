import json
import pytest
import firebase_admin
from firebase_admin import credentials, auth
from main import app, db
from models import Evento

# 🔥 Substitua pelo caminho da sua chave do Firebase
cred = credentials.Certificate("C:/Users/Rafael Saito/Desktop/P2 Tecnologia/serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# 🔥 Gere um token JWT válido antes dos testes
TEST_USER_EMAIL = "rafaelssaito@gmail.com"
TEST_USER_PASSWORD = "Saito2005#"

# Obtém um usuário do Firebase
user = auth.get_user_by_email(TEST_USER_EMAIL)
TEST_FIREBASE_TOKEN = x0a;98501adc-441c-405 {auth.create_custom_token(user.uid).decode()}"

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
    client = app.test_client()
    yield client
    with app.app_context():
        db.drop_all()

def test_post_evento(client):
    payload = {
        "titulo": "Evento de Teste",
        "data": "2025-05-28 20:30:00"
    }
    response = client.post("/eventos", json=payload, headers={"Authorization": TEST_FIREBASE_TOKEN})
    assert response.status_code == 201

def test_put_evento(client):
    payload = {
        "titulo": "Evento Para Atualizar",
        "data": "2025-05-28 20:30:00"
    }
    post_response = client.post("/eventos", json=payload, headers={"Authorization": TEST_FIREBASE_TOKEN})
    assert post_response.status_code == 201

    payload_update = {
        "titulo": "Evento Atualizado",
        "data": "2025-06-30 19:00:00"
    }
    put_response = client.put("/eventos/1", json=payload_update, headers={"Authorization": TEST_FIREBASE_TOKEN})
    assert put_response.status_code == 200

def test_delete_evento(client):
    payload = {
        "titulo": "Evento Para Deletar",
        "data": "2025-05-28 20:30:00"
    }
    client.post("/eventos", json=payload, headers={"Authorization": TEST_FIREBASE_TOKEN})

    delete_response = client.delete("/eventos/1", headers={"Authorization": TEST_FIREBASE_TOKEN})
    assert delete_response.status_code == 200

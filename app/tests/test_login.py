from main import app
from starlette.testclient import TestClient

client = TestClient(app)

def test_get_token():
    """
    Tokenを取得 成功パターン
    """
    response = client.post(
        "/api/token", 
        json={
              "email": "test@example.com",
              "password" : "testpass",
        }
    )
    assert response.status_code == 200 

def test_get_token_failed():
    """
    Tokenを取得 失敗
    """
    response = client.post(
        "/api/token", 
        json={
              "email": "testdwdwdwdwdw@example.com",
              "password" : "testpass",
        }
    )
    assert response.status_code == 401 

def test_get_token_failed_wrong_password():
    """
    Tokenを取得 失敗
    """
    response = client.post(
        "/api/token", 
        json={
              "email": "test@example.com",
              "password" : "testpass123",
        }
    )
    assert response.status_code == 401 
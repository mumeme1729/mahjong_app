import json
import pytest
from main import app
from starlette.testclient import TestClient

client = TestClient(app)


# @temp_db
def test_create_user_success():
    """
    Userを追加 成功パターン
    """
    response = client.post(
        "/api/register", 
        json={
              "email": "test@example.com",
              "is_active": True,
              "password" : "testpass",
        }
    )
    assert response.status_code == 200 or response.status_code == 400

def test_create_user_without_password():
    """
    Userを追加 成功パターン
    """
    response = client.post(
        "/api/register", 
        json={
              "email": "test2@example.com",
              "is_active": True,
        }
    )
    assert response.status_code == 422


 
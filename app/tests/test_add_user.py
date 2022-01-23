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
              "email": "testuser@example.com",
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


############### テスト用ユーザーを追加 ######################
def test_create_user2():
    """
    Userを追加 成功パターン
    """
    response = client.post(
        "/api/register", 
        json={
              "email": "testuser2@example.com",
              "is_active": True,
              "password" : "testpass",
        }
    )
    assert response.status_code == 200 or response.status_code == 400

def test_create_user3():
    """
    Userを追加 成功パターン
    """
    response = client.post(
        "/api/register", 
        json={
              "email": "testuser3@example.com",
              "is_active": True,
              "password" : "testpass",
        }
    )
    assert response.status_code == 200 or response.status_code == 400

def test_create_user4():
    """
    Userを追加 成功パターン
    """
    response = client.post(
        "/api/register", 
        json={
              "email": "testuser4@example.com",
              "is_active": True,
              "password" : "testpass",
        }
    )
    assert response.status_code == 200 or response.status_code == 400


def test_create_user5():
    """
    Userを追加 成功パターン
    """
    response = client.post(
        "/api/register", 
        json={
              "email": "testuser5@example.com",
              "is_active": True,
              "password" : "testpass",
        }
    )
    assert response.status_code == 200 or response.status_code == 400

def test_create_user6():
    """
    Userを追加 成功パターン
    """
    response = client.post(
        "/api/register", 
        json={
              "email": "testuser6@example.com",
              "is_active": True,
              "password" : "testpass",
        }
    )
    assert response.status_code == 200 or response.status_code == 400
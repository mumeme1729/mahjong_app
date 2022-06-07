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
              "firebase_uid": "cC6ZHDOvkYVZQcE1RMNVlTQV73X2",
              "is_active": True,
        }
    )
    assert response.status_code == 200 or response.status_code == 400


############### テスト用ユーザーを追加 ######################
def test_create_user2():
    """
    Userを追加 成功パターン
    """
    response = client.post(
        "/api/register", 
        json={
              "firebase_uid": "a16p2KHhEtZpyl97lby47SV6vCJ3",
              "is_active": True,
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
              "firebase_uid": "sxTyPwmzutQU8BZl5kWwAvvUxMf2",
              "is_active": True,
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
              "firebase_uid": "RCCgsrBowWSP2Kn1ukAKLcQPtPx2",
              "is_active": True,
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
              "firebase_uid": "qB9j8qN3VvQ0E1QgjMyIg7Y8ARw2",
              "is_active": True,
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
              "firebase_uid": "sKKq16dhYKNA14ns03oCYQnR7mP2",
              "is_active": True,
        }
    )
    assert response.status_code == 200 or response.status_code == 400

def test_create_user7():
    """
    Userを追加 成功パターン
    """
    response = client.post(
        "/api/register", 
        json={
              "firebase_uid": "5JklJinhpYbNVhJR2mFqnKoWDtg1",
              "is_active": True,
        }
    )
    assert response.status_code == 200 or response.status_code == 400

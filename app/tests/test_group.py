from ast import Param
from datetime import timedelta
import uuid
from services.authenticates.create_access_token import create_access_token
from main import app
from starlette.testclient import TestClient

client = TestClient(app)


def test_create_group_without_token():
    """
    グループ作成(認証無し)
    """

    response = client.post(
        "/api/groups/create_groups", 
        #headers={"Authentication": "coneofsilence"},
        json={
            "title": "string",
            "password": "string",
            "text": "string",
            "image": "string"
        }
    )
    assert response.status_code == 401

def test_create_group_wrong_token():
    """
    グループ作成(認証無し)
    """

    response = client.post(
        "/api/groups/create_groups", 
        #headers={"Authentication": "coneofsilence"},
        json={
            "title": "string",
            "password": "string",
            "text": "string",
            "image": "string"
        }
    )
    assert response.status_code == 401

def test_create_group_with_correct_token():
    """
    グループ作成 成功
    """
    access_token_expires = timedelta(minutes = 1800)
    token = create_access_token(
        token_payload={"sub": "testuser@example.com"},expires_delta=access_token_expires
    )
    auth = f"Bearer {token}"
    response = client.post(
        "/api/groups/create_groups", 
        headers={"Authorization": auth},
        json={
            "title": "string",
            "password": "string",
            "text": "string",
            "image": "string"
        }
    )
    assert response.status_code == 200 or response.status_code == 400

# def test_join_group():
#     """
#     グループ参加 成功 or 既に参加している
#     """
#     #トークン取得
#     access_token_expires = timedelta(minutes = 1800)
#     token = create_access_token(
#         token_payload={"sub": "testuser6@example.com"},expires_delta=access_token_expires
#     )
#     auth = f"Bearer {token}"
#     response = client.put(
#         "/api/groups/join_group", 
#         headers={"Authorization": auth},
#         json={
#             "title": "string",
#             "password": "string",
#             "text": "string",
#             "image": "string"
#         }
#     )
#     assert response.status_code == 200 or (response.status_code == 400 and response.detail == "already joined this group")

def test_leave_group_success():
    """
    グループ脱退成功パターン
    """
    access_token_expires = timedelta(minutes = 1800)
    token = create_access_token(
        token_payload={"sub": "testuser@example.com"},expires_delta=access_token_expires
    )
    auth = f"Bearer {token}"
    #グループを作成する
    res = client.post(
        "/api/groups/create_groups", 
        headers={"Authorization": auth},
        json={
            "title": "string",
            "password": "string",
            "text": "string",
            "image": "string"
        }
    )
    assert res.status_code == 200
    
    response = client.put(
        "/api/groups/leave_group", 
        headers={"Authorization": auth},
        params={
            "group_id": uuid.UUID(res.text[1:37]),
        }
    )

    assert response.status_code == 200

def test_leave_group_dont_belong_group():
    """
    グループ脱退失敗パターン(グループに属していない)
    """
    access_token_expires = timedelta(minutes = 1800)
    token = create_access_token(
        token_payload={"sub": "testuser@example.com"},expires_delta=access_token_expires
    )
    auth = f"Bearer {token}"
   
    response = client.put(
        "/api/groups/leave_group", 
        headers={"Authorization": auth},
        params={
            "group_id": uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        }
    )

    assert response.status_code == 400


def test_leave_group_dont_belong_group():
    """
    グループ脱退失敗パターン(既に非アクティブ)
    """
    access_token_expires = timedelta(minutes = 1800)
    token = create_access_token(
        token_payload={"sub": "testuser@example.com"},expires_delta=access_token_expires
    )
    auth = f"Bearer {token}"
    #グループを作成する
    res = client.post(
        "/api/groups/create_groups", 
        headers={"Authorization": auth},
        json={
            "title": "string",
            "password": "string",
            "text": "string",
            "image": "string"
        }
    )
    assert res.status_code == 200
    
    res1 = client.put(
        "/api/groups/leave_group", 
        headers={"Authorization": auth},
        params={
            "group_id": uuid.UUID(res.text[1:37]),
        }
    )

    assert res1.status_code == 200


    response = client.put(
        "/api/groups/leave_group", 
        headers={"Authorization": auth},
        params={
            "group_id": uuid.UUID(res.text[1:37]),
        }
    )


    assert response.status_code == 400

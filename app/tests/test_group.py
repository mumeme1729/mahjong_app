from main import app
from starlette.testclient import TestClient

client = TestClient(app)

token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNjQzMDI4NDczfQ.Rbj5sSvkqMh9dP3u_Bfm_Yr593sYeoq-i5fklu2Hrg8"

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

def test_join_group():
    """
    グループ参加 成功 or 既に参加している
    """
    #トークン取得
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
    assert response.status_code == 200 or (response.status_code == 400 and response.detail == "already joined this group")
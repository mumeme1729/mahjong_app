from main import app
from starlette.testclient import TestClient

client = TestClient(app)

token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNjQzMDI4NDczfQ.Rbj5sSvkqMh9dP3u_Bfm_Yr593sYeoq-i5fklu2Hrg8"

def test_create_game_without_token():
    """
    Game作成(認証無し)
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

def test_create_game_success():
    """
    Game作成 成功
    """
    auth = f"Bearer {token}"
    response = client.post(
        "/api/games/create_game/", 
        headers={"Authorization": auth},
        json={
            "is_sanma": False,
            "group_id": "bbd7768a-eb32-4195-b625-a12bea1d613e",
        }
    )
    assert response.status_code == 200

def test_create_game_does_not_group():
    """
    グループが存在しない
    """
    auth = f"Bearer {token}"
    response = client.post(
        "/api/games/create_game/", 
        headers={"Authorization": auth},
        json={
            "is_sanma": False,
            "group_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        }
    )
    assert response.status_code == 400



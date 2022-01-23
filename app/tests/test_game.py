from datetime import timedelta
import uuid
from services.authenticates.create_access_token import create_access_token
from main import app
from starlette.testclient import TestClient

client = TestClient(app)

###### gameテスト用にテストグループにテストユーザーを参加させる ######

group_id = ""
user2 = ""
user3 = ""
user4 = ""
user5 = ""

def test_create_group():
    """
    テスト用のグループ作成 
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
            "title": "テストグループ",
            "password": "string",
            "text": "string",
            "image": "string"
        }
    )
    global group_id
    group_id = response.text[1:37]
    assert response.status_code == 200 or response.status_code == 400

def test_join_group2():
    """
    グループ参加 成功 or 既に参加している
    """
    #トークン取得
    access_token_expires = timedelta(minutes = 1800)
    token = create_access_token(
        token_payload={"sub": "testuser2@example.com"},expires_delta=access_token_expires
    )
    auth = f"Bearer {token}"
    
    response = client.put(
        "/api/groups/join_group", 
        headers={"Authorization": auth},
        params={
            "group_id": uuid.UUID(group_id),
            "password": "string"
        }
    )
    global user2
    user2 = response.text[1:37]
    assert response.status_code == 200 or response.status_code == 400

def test_join_group3():
    """
    グループ参加 成功 or 既に参加している
    """
    #トークン取得
    access_token_expires = timedelta(minutes = 1800)
    token = create_access_token(
        token_payload={"sub": "testuser3@example.com"},expires_delta=access_token_expires
    )
    auth = f"Bearer {token}"
    response = client.put(
        "/api/groups/join_group", 
        headers={"Authorization": auth},
        params={
            "group_id": uuid.UUID(group_id),
            "password": "string"
        }
    )
    global user3
    user3 = response.text[1:37]
    assert response.status_code == 200 or response.status_code == 400

def test_join_group4():
    """
    グループ参加 成功 or 既に参加している
    """
    #トークン取得
    access_token_expires = timedelta(minutes = 1800)
    token = create_access_token(
        token_payload={"sub": "testuser4@example.com"},expires_delta=access_token_expires
    )
    auth = f"Bearer {token}"
    response = client.put(
        "/api/groups/join_group", 
        headers={"Authorization": auth},
        params={
            "group_id": uuid.UUID(group_id),
            "password": "string"
        }
    )
    global user4
    user4 = response.text[1:37]
    assert response.status_code == 200 or response.status_code == 400

def test_join_group5():
    """
    グループ参加 成功 or 既に参加している
    """
    #トークン取得
    access_token_expires = timedelta(minutes = 1800)
    token = create_access_token(
        token_payload={"sub": "testuser5@example.com"},expires_delta=access_token_expires
    )
    auth = f"Bearer {token}"
    response = client.put(
        "/api/groups/join_group", 
        headers={"Authorization": auth},
        params={
            "group_id": uuid.UUID(group_id),
            "password": "string"
        }
    )
    global user5
    user5 = response.text[1:37]
    assert response.status_code == 200 or response.status_code == 400

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
    Game作成 成功 4麻
    """
    access_token_expires = timedelta(minutes = 1800)
    token = create_access_token(
        token_payload={"sub": "testuser@example.com"},expires_delta=access_token_expires
    )

    auth = f"Bearer {token}"
    response = client.post(
        "/api/games/create_game/", 
        headers={"Authorization": auth},
        json={
            "is_sanma": False,
            "group_id": group_id,
            "game_results": [
                {
                    "rank": 1,
                    "score": 25000,
                    "game": None,
                    "profile": user2
                },
                {
                    "rank": 2,
                    "score": 30000,
                    "game": None,
                    "profile": user3
                },
                {
                    "rank": 3,
                    "score": 25000,
                    "game": None,
                    "profile": user4
                },
                {
                    "rank": 4,
                    "score": 20000,
                    "game": None,
                    "profile": user5
                }
            ]
        }
    )
    assert response.status_code == 200

def test_create_game_success_3():
    """
    Game作成 成功 3麻
    """
    access_token_expires = timedelta(minutes = 1800)
    token = create_access_token(
        token_payload={"sub": "testuser@example.com"},expires_delta=access_token_expires
    )

    auth = f"Bearer {token}"
    response = client.post(
        "/api/games/create_game/", 
        headers={"Authorization": auth},
        json={
            "is_sanma": True,
            "group_id": group_id,
            "game_results": [
                {
                    "rank": 1,
                    "score": 25000,
                    "game": None,
                    "profile": user2
                },
                {
                    "rank": 2,
                    "score": 30000,
                    "game": None,
                    "profile": user3
                },
                {
                    "rank": 3,
                    "score": 25000,
                    "game": None,
                    "profile": user4
                },
            ]
        }
    )
    assert response.status_code == 200

def test_create_game_false_4_but_3():
    """
    Game作成 失敗 4麻なのに結果3つ
    """
    access_token_expires = timedelta(minutes = 1800)
    token = create_access_token(
        token_payload={"sub": "testuser@example.com"},expires_delta=access_token_expires
    )

    auth = f"Bearer {token}"
    response = client.post(
        "/api/games/create_game/", 
        headers={"Authorization": auth},
        json={
            "is_sanma": False,
            "group_id": group_id,
            "game_results": [
                {
                    "rank": 1,
                    "score": 25000,
                    "game": None,
                    "profile": user2
                },
                {
                    "rank": 2,
                    "score": 30000,
                    "game": None,
                    "profile": user3
                },
                {
                    "rank": 3,
                    "score": 25000,
                    "game": None,
                    "profile": user4
                },
            ]
        }
    )
    assert response.status_code == 400

def test_create_game_flase_3_but_4():
    """
    Game作成 失敗 3麻なのに結果4つ
    """
    access_token_expires = timedelta(minutes = 1800)
    token = create_access_token(
        token_payload={"sub": "testuser@example.com"},expires_delta=access_token_expires
    )

    auth = f"Bearer {token}"
    response = client.post(
        "/api/games/create_game/", 
        headers={"Authorization": auth},
        json={
            "is_sanma": True,
            "group_id": group_id,
            "game_results": [
                {
                    "rank": 1,
                    "score": 25000,
                    "game": None,
                    "profile": user2
                },
                {
                    "rank": 2,
                    "score": 30000,
                    "game": None,
                    "profile": user3
                },
                {
                    "rank": 3,
                    "score": 25000,
                    "game": None,
                    "profile": user4
                },
                {
                    "rank": 4,
                    "score": 25000,
                    "game": None,
                    "profile": user5
                },
            ]
        }
    )
    assert response.status_code == 400

def test_create_game_flase_nod_belong_this_group():
    """
    Game作成 失敗 参加していないグループに作成
    """
    access_token_expires = timedelta(minutes = 1800)
    token = create_access_token(
        token_payload={"sub": "testuser6@example.com"},expires_delta=access_token_expires
    )

    auth = f"Bearer {token}"
    response = client.post(
        "/api/games/create_game/", 
        headers={"Authorization": auth},
        json={
            "is_sanma": True,
            "group_id": group_id,
            "game_results": [
                {
                    "rank": 1,
                    "score": 25000,
                    "game": None,
                    "profile": user2
                },
                {
                    "rank": 2,
                    "score": 30000,
                    "game": None,
                    "profile": user3
                },
                {
                    "rank": 3,
                    "score": 25000,
                    "game": None,
                    "profile": user4
                },
                {
                    "rank": 4,
                    "score": 25000,
                    "game": None,
                    "profile": user5
                },
            ]
        }
    )
    assert response.status_code == 400

def test_create_game_flase_doesnot_exist_group():
    """
    Game作成 失敗 参加していないグループに作成
    """
    access_token_expires = timedelta(minutes = 1800)
    token = create_access_token(
        token_payload={"sub": "testuser@example.com"},expires_delta=access_token_expires
    )

    auth = f"Bearer {token}"
    response = client.post(
        "/api/games/create_game/", 
        headers={"Authorization": auth},
        json={
            "is_sanma": False,
            "group_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "game_results": [
                {
                    "rank": 1,
                    "score": 25000,
                    "game": None,
                    "profile": user2
                },
                {
                    "rank": 2,
                    "score": 30000,
                    "game": None,
                    "profile": user3
                },
                {
                    "rank": 3,
                    "score": 25000,
                    "game": None,
                    "profile": user4
                },
                {
                    "rank": 4,
                    "score": 25000,
                    "game": None,
                    "profile": user5
                },
            ]
        }
    )
    assert response.status_code == 400

def test_delete_game_success():
    """
    Game削除 成功
    """
    access_token_expires = timedelta(minutes = 1800)
    token = create_access_token(
        token_payload={"sub": "testuser@example.com"},expires_delta=access_token_expires
    )

    auth = f"Bearer {token}"
    response = client.post(
        "/api/games/create_game/", 
        headers={"Authorization": auth},
        json={
            "is_sanma": False,
            "group_id": group_id,
            "game_results": [
                {
                    "rank": 1,
                    "score": 25000,
                    "game": None,
                    "profile": user2
                },
                {
                    "rank": 2,
                    "score": 30000,
                    "game": None,
                    "profile": user3
                },
                {
                    "rank": 3,
                    "score": 25000,
                    "game": None,
                    "profile": user4
                },
                {
                    "rank": 4,
                    "score": 25000,
                    "game": None,
                    "profile": user5
                },
            ]
        }
    )
    game_id = response.text[1:37]
    
    res = client.delete(
        "/api/games/delete_game/", 
        headers={"Authorization": auth},
         params={
            "game_id": uuid.UUID(game_id),
        }
    )

    assert response.status_code == 200


def test_delete_game_false_does_not_exit_game():
    """
    ゲーム削除失敗 対象のゲームが存在しない
    """
    access_token_expires = timedelta(minutes = 1800)
    token = create_access_token(
        token_payload={"sub": "testuser@example.com"},expires_delta=access_token_expires
    )
    auth = f"Bearer {token}"
    res = client.delete(
        "/api/games/delete_game/", 
        headers={"Authorization": auth},
         params={
            "game_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        }
    )

    assert res.status_code == 400
from datetime import timedelta
import uuid
from services.authenticates.get_current_user import create_token
from main import app
from starlette.testclient import TestClient
from firebase_admin import auth, credentials
import firebase_admin

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
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNmNWQ4ZTc0ZjNjNDg2ZWU1MDNkNWVlYzkzYTEwMWM2NGJhY2Y3ZGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ3JvdXAtbWFoam9uZyIsImF1ZCI6Imdyb3VwLW1haGpvbmciLCJhdXRoX3RpbWUiOjE2NDU4Mzg4MzUsInVzZXJfaWQiOiJjQzZaSERPdmtZVlpRY0UxUk1OVmxUUVY3M1gyIiwic3ViIjoiY0M2WkhET3ZrWVZaUWNFMVJNTlZsVFFWNzNYMiIsImlhdCI6MTY0NTgzODgzNSwiZXhwIjoxNjQ1ODQyNDM1LCJlbWFpbCI6Im11bWVtZS5leGVAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm11bWVtZS5leGVAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.sz-kPOsGk3UG_1RJPnyfF_wgbFxQhbu8gmN9bGa2XOisVasLL1dd2oGDxVeew3djhWU-jyS33x5YsQ9gUZmBGdsPk-mUN7iE2JTwQhQIOZ-3COE91smPmGoqrgYrstfHLvu1v_buwuRZhFSYd2mNxevUw0BQnRHpFqvNaLrAk0NuhIXWC4TDtl_rewIFdtkhO3vpsQdD4OCpxZI-_PZX-9XnuetyZiu47yymzVodfqQoAuxQ3s59Wq_XMQYiYa3oK5z_G2BxmDn5v9TDrYUb11dt8_Nnuo9hzZ1SLms_YuW3-CME-TaxxCREBcF8dvXjIuIhTMzTgCIWBMw-syPZOA" 
    t = f"Bearer {token}"
    response = client.post(
        "/api/groups/create_groups", 
        headers={"Authorization": t},
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
    token =  "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNmNWQ4ZTc0ZjNjNDg2ZWU1MDNkNWVlYzkzYTEwMWM2NGJhY2Y3ZGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ3JvdXAtbWFoam9uZyIsImF1ZCI6Imdyb3VwLW1haGpvbmciLCJhdXRoX3RpbWUiOjE2NDU4Mzg2NjgsInVzZXJfaWQiOiI1SmtsSmluaHBZYk5WaEpSMm1GcW5Lb1dEdGcxIiwic3ViIjoiNUprbEppbmhwWWJOVmhKUjJtRnFuS29XRHRnMSIsImlhdCI6MTY0NTgzODY2OCwiZXhwIjoxNjQ1ODQyMjY4LCJlbWFpbCI6InRlc3R1c2VyMUBleGFtcGxlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJ0ZXN0dXNlcjFAZXhhbXBsZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.jPXefgZKJu5H1XgL2JMpJ-RO5fVQU06bHphY2nFeWrPN_tvSkRXFKx3CitmsX83oTfChHIhZCW7G1AKjuyN9pSVHkrDoC4xMVsfUoTN39k5ufCyOnvfx0B9h0LUSCO6fcY8VOiEvQ1nnj1WPsWYL_7DePHaUTI-Y0yv0EQPgqk5wjMJ6o4_Zf-TjTFyvL3UcvG15d4y2ZAVv4rYNbSkgg_Ume9SCktw6aqrsFBrfCpZ1_i-1vKhF7PXbpwqQqL-chd9qvs3LOI9W7xyXOo3Ngy2rLf2UyFOVdXUI1TBAVirACFhfg47gNAVXY8SxvG-0cbr1Zh5s5TLU3hE-8gE9bg"
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
    token =  "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNmNWQ4ZTc0ZjNjNDg2ZWU1MDNkNWVlYzkzYTEwMWM2NGJhY2Y3ZGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ3JvdXAtbWFoam9uZyIsImF1ZCI6Imdyb3VwLW1haGpvbmciLCJhdXRoX3RpbWUiOjE2NDU4Mzg3MzMsInVzZXJfaWQiOiJhMTZwMktIaEV0WnB5bDk3bGJ5NDdTVjZ2Q0ozIiwic3ViIjoiYTE2cDJLSGhFdFpweWw5N2xieTQ3U1Y2dkNKMyIsImlhdCI6MTY0NTgzODczMywiZXhwIjoxNjQ1ODQyMzMzLCJlbWFpbCI6InRlc3R1c2VyMkBleGFtcGxlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJ0ZXN0dXNlcjJAZXhhbXBsZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.DGaIWmcS1eMAF7YnoJjh5-2ykogou8uQBK5lFDSBkd9sWv7kd_dIQaUPOVUvspQc_Ggaxp_G0WzYlgqQAjf9d7X-HnGhZ132iE9OWn3qOZGWCMTG6WyPKo1Iy8WNo2C14pute-ze_7gas3RPmC6V2Ok_HB9FJmgJucJizOjtAASu8G1mxsh2Oix2jJjz4oN0uWhDI8bnKTbkIqtw3MQS3N3OkqpqmjUbWDWOxY5d_oNF55NJZjy95Uz220smaRyFa3cXGfIqkQAPbbqhwKL_PtP8BTBA98_l1N2cdJ9sF5Tqzo2VMU43HLkgiBxxo_85aWxLQ3KrR5PeP8KCCSYvEA"
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
    token =  "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNmNWQ4ZTc0ZjNjNDg2ZWU1MDNkNWVlYzkzYTEwMWM2NGJhY2Y3ZGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ3JvdXAtbWFoam9uZyIsImF1ZCI6Imdyb3VwLW1haGpvbmciLCJhdXRoX3RpbWUiOjE2NDU4Mzg3NjcsInVzZXJfaWQiOiJzeFR5UHdtenV0UVU4QlpsNWtXd0F2dlV4TWYyIiwic3ViIjoic3hUeVB3bXp1dFFVOEJabDVrV3dBdnZVeE1mMiIsImlhdCI6MTY0NTgzODc2NywiZXhwIjoxNjQ1ODQyMzY3LCJlbWFpbCI6InRlc3R1c2VyM0BleGFtcGxlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJ0ZXN0dXNlcjNAZXhhbXBsZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.YwVqseDrxlFdrzR0Iy7YhzXxJweo-K9CIaDyi63XVlRTACMUbvj5eQ_cqwYNO_gRT52Gwndhe9OerpRz6B1UE5BiBL8lYdjRp7jHhX50sKw1gY-1EgJxtW83GmLsCn-POfhkPOyLgBWMte9S8ktQcxNCZUvkGTAMNpg7aiDLvBtWKnbf4JvhOmCCiVZq6pWqLj4MxXwNm6w1y3hHcpOaEQhWjdZRmzuXCF55R-gxnt9LZLtlR8RHmAJgdSZwrxaJuiQA5Uh0hd4rX1JI1HTmXVHnsvtNQDFRkDTnXbkxks4wTztb74Z5U0TVzT-2bodIv1FG7Fjh2uC1Q3AKhS97bQ"
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
    token =  "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNmNWQ4ZTc0ZjNjNDg2ZWU1MDNkNWVlYzkzYTEwMWM2NGJhY2Y3ZGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ3JvdXAtbWFoam9uZyIsImF1ZCI6Imdyb3VwLW1haGpvbmciLCJhdXRoX3RpbWUiOjE2NDU4Mzg3OTQsInVzZXJfaWQiOiJSQ0Nnc3JCb3dXU1AyS24xdWtBS0xjUVB0UHgyIiwic3ViIjoiUkNDZ3NyQm93V1NQMktuMXVrQUtMY1FQdFB4MiIsImlhdCI6MTY0NTgzODc5NCwiZXhwIjoxNjQ1ODQyMzk0LCJlbWFpbCI6InRlc3R1c2VyNEBleGFtcGxlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJ0ZXN0dXNlcjRAZXhhbXBsZS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.Kw9Klb_K5_qfy5yyESaJoUe3Ib1bXZxUZInHmcuzBNBwuyN4LzpvjP5SK6_IALOTY5WjzrarhcyM9CKDkoig8u1VybldaYVpYuzUJCzJvslARCFAD7OdAUC-_E3_86FLN-JMyt_OcBcLSPVz6q_7F3SAcDP06vwXm7z4jKncX35t0QoJq4ylG8iw8fE0CUSRXeW-bjXteHx_HmUBha11V0leVYSnYyuX_YC6IKby3L16-GM-Fi-pbhwrntjGCDqXkDzPfbSB_gIz17HpxgZgc9FfWZz54pqYFX5YgzhNbk0v84uK-OUdd6YdteOw0nZN8u267VajVZBV8d27MFkK1Q"
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
    token =  "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNmNWQ4ZTc0ZjNjNDg2ZWU1MDNkNWVlYzkzYTEwMWM2NGJhY2Y3ZGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ3JvdXAtbWFoam9uZyIsImF1ZCI6Imdyb3VwLW1haGpvbmciLCJhdXRoX3RpbWUiOjE2NDU4Mzg4MzUsInVzZXJfaWQiOiJjQzZaSERPdmtZVlpRY0UxUk1OVmxUUVY3M1gyIiwic3ViIjoiY0M2WkhET3ZrWVZaUWNFMVJNTlZsVFFWNzNYMiIsImlhdCI6MTY0NTgzODgzNSwiZXhwIjoxNjQ1ODQyNDM1LCJlbWFpbCI6Im11bWVtZS5leGVAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm11bWVtZS5leGVAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.sz-kPOsGk3UG_1RJPnyfF_wgbFxQhbu8gmN9bGa2XOisVasLL1dd2oGDxVeew3djhWU-jyS33x5YsQ9gUZmBGdsPk-mUN7iE2JTwQhQIOZ-3COE91smPmGoqrgYrstfHLvu1v_buwuRZhFSYd2mNxevUw0BQnRHpFqvNaLrAk0NuhIXWC4TDtl_rewIFdtkhO3vpsQdD4OCpxZI-_PZX-9XnuetyZiu47yymzVodfqQoAuxQ3s59Wq_XMQYiYa3oK5z_G2BxmDn5v9TDrYUb11dt8_Nnuo9hzZ1SLms_YuW3-CME-TaxxCREBcF8dvXjIuIhTMzTgCIWBMw-syPZOA"
    
    auth = f"Bearer {token}"
    response = client.post(
        "/api/games/create_game/", 
        headers={"Authorization": auth},
        json={
            "is_sanma": False,
            "group_id": group_id,
            "game_results": [
                {
                    "rank": 4,
                    "score": 20000,
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
                    "rank": 1,
                    "score": 40000,
                    "game": None,
                    "profile": user4
                },
                {
                    "rank": 3,
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
    token =  "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNmNWQ4ZTc0ZjNjNDg2ZWU1MDNkNWVlYzkzYTEwMWM2NGJhY2Y3ZGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ3JvdXAtbWFoam9uZyIsImF1ZCI6Imdyb3VwLW1haGpvbmciLCJhdXRoX3RpbWUiOjE2NDU4Mzg4MzUsInVzZXJfaWQiOiJjQzZaSERPdmtZVlpRY0UxUk1OVmxUUVY3M1gyIiwic3ViIjoiY0M2WkhET3ZrWVZaUWNFMVJNTlZsVFFWNzNYMiIsImlhdCI6MTY0NTgzODgzNSwiZXhwIjoxNjQ1ODQyNDM1LCJlbWFpbCI6Im11bWVtZS5leGVAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm11bWVtZS5leGVAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.sz-kPOsGk3UG_1RJPnyfF_wgbFxQhbu8gmN9bGa2XOisVasLL1dd2oGDxVeew3djhWU-jyS33x5YsQ9gUZmBGdsPk-mUN7iE2JTwQhQIOZ-3COE91smPmGoqrgYrstfHLvu1v_buwuRZhFSYd2mNxevUw0BQnRHpFqvNaLrAk0NuhIXWC4TDtl_rewIFdtkhO3vpsQdD4OCpxZI-_PZX-9XnuetyZiu47yymzVodfqQoAuxQ3s59Wq_XMQYiYa3oK5z_G2BxmDn5v9TDrYUb11dt8_Nnuo9hzZ1SLms_YuW3-CME-TaxxCREBcF8dvXjIuIhTMzTgCIWBMw-syPZOA"
    
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
    token =  "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNmNWQ4ZTc0ZjNjNDg2ZWU1MDNkNWVlYzkzYTEwMWM2NGJhY2Y3ZGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ3JvdXAtbWFoam9uZyIsImF1ZCI6Imdyb3VwLW1haGpvbmciLCJhdXRoX3RpbWUiOjE2NDU4Mzg4MzUsInVzZXJfaWQiOiJjQzZaSERPdmtZVlpRY0UxUk1OVmxUUVY3M1gyIiwic3ViIjoiY0M2WkhET3ZrWVZaUWNFMVJNTlZsVFFWNzNYMiIsImlhdCI6MTY0NTgzODgzNSwiZXhwIjoxNjQ1ODQyNDM1LCJlbWFpbCI6Im11bWVtZS5leGVAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm11bWVtZS5leGVAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.sz-kPOsGk3UG_1RJPnyfF_wgbFxQhbu8gmN9bGa2XOisVasLL1dd2oGDxVeew3djhWU-jyS33x5YsQ9gUZmBGdsPk-mUN7iE2JTwQhQIOZ-3COE91smPmGoqrgYrstfHLvu1v_buwuRZhFSYd2mNxevUw0BQnRHpFqvNaLrAk0NuhIXWC4TDtl_rewIFdtkhO3vpsQdD4OCpxZI-_PZX-9XnuetyZiu47yymzVodfqQoAuxQ3s59Wq_XMQYiYa3oK5z_G2BxmDn5v9TDrYUb11dt8_Nnuo9hzZ1SLms_YuW3-CME-TaxxCREBcF8dvXjIuIhTMzTgCIWBMw-syPZOA"
    
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
    token =  "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNmNWQ4ZTc0ZjNjNDg2ZWU1MDNkNWVlYzkzYTEwMWM2NGJhY2Y3ZGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ3JvdXAtbWFoam9uZyIsImF1ZCI6Imdyb3VwLW1haGpvbmciLCJhdXRoX3RpbWUiOjE2NDU4Mzg4MzUsInVzZXJfaWQiOiJjQzZaSERPdmtZVlpRY0UxUk1OVmxUUVY3M1gyIiwic3ViIjoiY0M2WkhET3ZrWVZaUWNFMVJNTlZsVFFWNzNYMiIsImlhdCI6MTY0NTgzODgzNSwiZXhwIjoxNjQ1ODQyNDM1LCJlbWFpbCI6Im11bWVtZS5leGVAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm11bWVtZS5leGVAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.sz-kPOsGk3UG_1RJPnyfF_wgbFxQhbu8gmN9bGa2XOisVasLL1dd2oGDxVeew3djhWU-jyS33x5YsQ9gUZmBGdsPk-mUN7iE2JTwQhQIOZ-3COE91smPmGoqrgYrstfHLvu1v_buwuRZhFSYd2mNxevUw0BQnRHpFqvNaLrAk0NuhIXWC4TDtl_rewIFdtkhO3vpsQdD4OCpxZI-_PZX-9XnuetyZiu47yymzVodfqQoAuxQ3s59Wq_XMQYiYa3oK5z_G2BxmDn5v9TDrYUb11dt8_Nnuo9hzZ1SLms_YuW3-CME-TaxxCREBcF8dvXjIuIhTMzTgCIWBMw-syPZOA"
    
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
    token =  "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNmNWQ4ZTc0ZjNjNDg2ZWU1MDNkNWVlYzkzYTEwMWM2NGJhY2Y3ZGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ3JvdXAtbWFoam9uZyIsImF1ZCI6Imdyb3VwLW1haGpvbmciLCJhdXRoX3RpbWUiOjE2NDU4Mzg4MzUsInVzZXJfaWQiOiJjQzZaSERPdmtZVlpRY0UxUk1OVmxUUVY3M1gyIiwic3ViIjoiY0M2WkhET3ZrWVZaUWNFMVJNTlZsVFFWNzNYMiIsImlhdCI6MTY0NTgzODgzNSwiZXhwIjoxNjQ1ODQyNDM1LCJlbWFpbCI6Im11bWVtZS5leGVAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm11bWVtZS5leGVAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.sz-kPOsGk3UG_1RJPnyfF_wgbFxQhbu8gmN9bGa2XOisVasLL1dd2oGDxVeew3djhWU-jyS33x5YsQ9gUZmBGdsPk-mUN7iE2JTwQhQIOZ-3COE91smPmGoqrgYrstfHLvu1v_buwuRZhFSYd2mNxevUw0BQnRHpFqvNaLrAk0NuhIXWC4TDtl_rewIFdtkhO3vpsQdD4OCpxZI-_PZX-9XnuetyZiu47yymzVodfqQoAuxQ3s59Wq_XMQYiYa3oK5z_G2BxmDn5v9TDrYUb11dt8_Nnuo9hzZ1SLms_YuW3-CME-TaxxCREBcF8dvXjIuIhTMzTgCIWBMw-syPZOA"
    
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
    token =  "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNmNWQ4ZTc0ZjNjNDg2ZWU1MDNkNWVlYzkzYTEwMWM2NGJhY2Y3ZGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ3JvdXAtbWFoam9uZyIsImF1ZCI6Imdyb3VwLW1haGpvbmciLCJhdXRoX3RpbWUiOjE2NDU4Mzg4MzUsInVzZXJfaWQiOiJjQzZaSERPdmtZVlpRY0UxUk1OVmxUUVY3M1gyIiwic3ViIjoiY0M2WkhET3ZrWVZaUWNFMVJNTlZsVFFWNzNYMiIsImlhdCI6MTY0NTgzODgzNSwiZXhwIjoxNjQ1ODQyNDM1LCJlbWFpbCI6Im11bWVtZS5leGVAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm11bWVtZS5leGVAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.sz-kPOsGk3UG_1RJPnyfF_wgbFxQhbu8gmN9bGa2XOisVasLL1dd2oGDxVeew3djhWU-jyS33x5YsQ9gUZmBGdsPk-mUN7iE2JTwQhQIOZ-3COE91smPmGoqrgYrstfHLvu1v_buwuRZhFSYd2mNxevUw0BQnRHpFqvNaLrAk0NuhIXWC4TDtl_rewIFdtkhO3vpsQdD4OCpxZI-_PZX-9XnuetyZiu47yymzVodfqQoAuxQ3s59Wq_XMQYiYa3oK5z_G2BxmDn5v9TDrYUb11dt8_Nnuo9hzZ1SLms_YuW3-CME-TaxxCREBcF8dvXjIuIhTMzTgCIWBMw-syPZOA"
    
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
    token =  "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNmNWQ4ZTc0ZjNjNDg2ZWU1MDNkNWVlYzkzYTEwMWM2NGJhY2Y3ZGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ3JvdXAtbWFoam9uZyIsImF1ZCI6Imdyb3VwLW1haGpvbmciLCJhdXRoX3RpbWUiOjE2NDU4Mzg4MzUsInVzZXJfaWQiOiJjQzZaSERPdmtZVlpRY0UxUk1OVmxUUVY3M1gyIiwic3ViIjoiY0M2WkhET3ZrWVZaUWNFMVJNTlZsVFFWNzNYMiIsImlhdCI6MTY0NTgzODgzNSwiZXhwIjoxNjQ1ODQyNDM1LCJlbWFpbCI6Im11bWVtZS5leGVAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm11bWVtZS5leGVAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.sz-kPOsGk3UG_1RJPnyfF_wgbFxQhbu8gmN9bGa2XOisVasLL1dd2oGDxVeew3djhWU-jyS33x5YsQ9gUZmBGdsPk-mUN7iE2JTwQhQIOZ-3COE91smPmGoqrgYrstfHLvu1v_buwuRZhFSYd2mNxevUw0BQnRHpFqvNaLrAk0NuhIXWC4TDtl_rewIFdtkhO3vpsQdD4OCpxZI-_PZX-9XnuetyZiu47yymzVodfqQoAuxQ3s59Wq_XMQYiYa3oK5z_G2BxmDn5v9TDrYUb11dt8_Nnuo9hzZ1SLms_YuW3-CME-TaxxCREBcF8dvXjIuIhTMzTgCIWBMw-syPZOA"
    
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
    token =  "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNmNWQ4ZTc0ZjNjNDg2ZWU1MDNkNWVlYzkzYTEwMWM2NGJhY2Y3ZGEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ3JvdXAtbWFoam9uZyIsImF1ZCI6Imdyb3VwLW1haGpvbmciLCJhdXRoX3RpbWUiOjE2NDU4Mzg4MzUsInVzZXJfaWQiOiJjQzZaSERPdmtZVlpRY0UxUk1OVmxUUVY3M1gyIiwic3ViIjoiY0M2WkhET3ZrWVZaUWNFMVJNTlZsVFFWNzNYMiIsImlhdCI6MTY0NTgzODgzNSwiZXhwIjoxNjQ1ODQyNDM1LCJlbWFpbCI6Im11bWVtZS5leGVAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm11bWVtZS5leGVAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.sz-kPOsGk3UG_1RJPnyfF_wgbFxQhbu8gmN9bGa2XOisVasLL1dd2oGDxVeew3djhWU-jyS33x5YsQ9gUZmBGdsPk-mUN7iE2JTwQhQIOZ-3COE91smPmGoqrgYrstfHLvu1v_buwuRZhFSYd2mNxevUw0BQnRHpFqvNaLrAk0NuhIXWC4TDtl_rewIFdtkhO3vpsQdD4OCpxZI-_PZX-9XnuetyZiu47yymzVodfqQoAuxQ3s59Wq_XMQYiYa3oK5z_G2BxmDn5v9TDrYUb11dt8_Nnuo9hzZ1SLms_YuW3-CME-TaxxCREBcF8dvXjIuIhTMzTgCIWBMw-syPZOA"
    
    auth = f"Bearer {token}"
    res = client.delete(
        "/api/games/delete_game/", 
        headers={"Authorization": auth},
         params={
            "game_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        }
    )

    assert res.status_code == 400
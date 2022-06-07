import yaml
from models import profiles
from services.cruds.user_crud import get_user_by_firebase_uid
from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional #指定の型 or None を許容する場合に使用
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from firebase_admin import auth, credentials
import firebase_admin

from schemas.user import User
from db import get_db
from services.logs.set_logs import set_logger


# 設定ファイルを読み込む
with open('settings.yaml', 'r') as yml:
    settings = yaml.safe_load(yml)

_secret_key = settings['fastapi']['password']['SECRET_KEY']
_algorithm = settings['fastapi']['password']['ALGORITHM']

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

cred = credentials.Certificate('secret_key.json')
firebase_admin.initialize_app(cred)

# ロガーの設定
_logger = set_logger(__name__)
async def get_current_user(cred: HTTPAuthorizationCredentials=Depends(HTTPBearer(auto_error=False)),db:Session = Depends(get_db)) -> User:
    """
    JWTを解析し、現在ログインしているユーザーを返す。
    
    Parameters

    ----------
    token : str
        jwtのトークンデータ
    """
    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
        )
    try:
        decoded_token = auth.verify_id_token(cred.credentials)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    uid = decoded_token['uid']
    # ユーザーテーブルからトークンデータのユーザー名と等しいユーザーを取得
    user_data = get_user_by_firebase_uid(uid,db)
    user = User(
            id = user_data.id,
            firebase_uid = user_data.firebase_uid,
            is_active = user_data.is_active,
            profiles = user_data.profiles,
            nick_name = user_data.nick_name,
            image = user_data.image
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    ユーザーがアクティブかどうかを検証する。
    
    Parameters
    
    ----------
    current_data : User
        現在ログインしているユーザー情報
    """
    if not current_user.is_active:
        _logger.warning(HTTPException(status_code=400, detail="Inactive user"))
        raise HTTPException(status_code=400, detail="Inactive user")
        
    return current_user


# カスタムトークンの作成
def create_token(uid: str):
    """
    テスト用のトークン取得
    """
    
    token = auth.create_custom_token(uid)
        
    return token.decode()
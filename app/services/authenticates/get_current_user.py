import os
import yaml
from services.cruds.user_crud import get_user_by_email
from fastapi import Depends,HTTPException,status
from jose import JWTError, jwt
from typing import Optional #指定の型 or None を許容する場合に使用
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from models.users import UserTable
from schemas.user import User
from db import get_db
from services.logs.set_logs import set_logger


# 設定ファイルを読み込む
with open('settings.yaml', 'r') as yml:
    settings = yaml.safe_load(yml)

_secret_key = settings['fastapi']['password']['SECRET_KEY']
_algorithm = settings['fastapi']['password']['ALGORITHM']
_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ロガーの設定
_logger = set_logger(__name__)
async def get_current_user(token: str = Depends(_oauth2_scheme),db:Session = Depends(get_db)) -> User:
    """
    JWTを解析し、現在ログインしているユーザーを返す。
    
    Parameters

    ----------
    token : str
        jwtのトークンデータ
    """
    #memo 認証キーがない場合は処理に入る前に弾かれる。
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # jwtをデコードする。
        payload = jwt.decode(token, _secret_key, algorithms=[_algorithm])
        #デコードしたjwtからsub(ユーザー名)を取り出す。
        user_email: str = payload.get("sub")
        if user_email is None:
            _logger.warning(credentials_exception)
            raise credentials_exception
        
    except JWTError:
        _logger.warning(credentials_exception)
        raise credentials_exception
        
    # ユーザーテーブルからトークンデータのユーザー名と等しいユーザーを取得
    user_data = get_user_by_email(user_email,db)
    user = User(
            id = user_data.id,
            email = user_data.email,
            is_active = user_data.is_active,
            groups = user_data.groups
    )
    if user is None:
        _logger.warning(credentials_exception)
        raise credentials_exception
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
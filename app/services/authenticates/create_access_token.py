import os
import yaml
from datetime import datetime, timedelta
from typing import Optional
from utils.errors import ApiException
from fastapi import HTTPException,status
from jose import JWTError, jwt

# 設定ファイルを読み込む
with open('settings.yaml', 'r') as yml:
    settings = yaml.safe_load(yml)

_secret_key = settings['fastapi']['password']['SECRET_KEY']
_algorithm = settings['fastapi']['password']['ALGORITHM']


def create_access_token(uid: str, expires_delta: Optional[timedelta] = None,):
    """
    アクセストークンを作成する
    
    Parameters
    
    ----------
    token_payload : dict
        jwtのペイロードに設定する辞書型の情報
    expires_delta : Optional[timedelta]
        jwtの有効期限
    """
    create_jwt_exception = ApiException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        status="fail",
        detail="Could not create jwt",
    )
    try:
        to_encode =token_payload.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=10080)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, _secret_key, algorithm=_algorithm)
        return encoded_jwt
    except: 
        raise create_jwt_exception
    # token = auth.create_custom_token(uid)
    # return token
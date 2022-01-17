from typing import Any
import yaml
import logging
import requests

from datetime import timedelta
from fastapi import APIRouter, Body, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.token import Token,LoginInfo
from schemas.user import UserCreate

from services.cruds.user_crud import get_all_users,get_user_by_email, set_user
from services.logs.set_logs import set_logger
from services.authenticates.authenticate_user import authenticate_user
from services.authenticates.create_access_token import create_access_token
from db import get_db

router = APIRouter()

with open('settings.yaml', 'r') as yml:
    settings = yaml.safe_load(yml)

#ログファイルを作成
_uvicorn_accsess_logger = set_logger("uvicorn.access",file_name = 'access')
_ormapper_logger = set_logger("sqlalchemy.engine",file_name='ormapper')
_logger = set_logger(__name__)

@router.post("/register")
async def create_character(user_data:UserCreate,db:Session = Depends(get_db)):
    """
    ユーザー登録を行う。
    """
    #既に登録されているか確認を行う
    user = get_user_by_email(user_data.email,db)
    if not user:
        #データベースにユーザーを登録する
        user = set_user(user_data,db)
        return user
    else:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: LoginInfo,db:Session = Depends(get_db)) -> dict:
    """
    ログイン認証が完了したらJWTを返す。
    """
    try:
        #DBからフォームに入力されたユーザー名のユーザーを取り出す。
        user_data = get_user_by_email(form_data.email,db)
        user = authenticate_user(user_data,form_data.password)
        if not user:
            _logger.warning(f"login: {form_data.email}[ Failure ]")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        #パスワードの検証が完了したらトークンを生成
        access_token_expires = timedelta(minutes = settings['fastapi']['token']['ACCESS_TOKEN_EXPIRE_MINUTES'])
        access_token = create_access_token(
            token_payload={"sub": user.email},expires_delta=access_token_expires
        )
        _logger.info(f"login: {form_data.email} [ Success ]")
        return {"access_token": access_token, "token_type": "bearer"}


    except requests.exceptions.RequestException as e:
        _logger.exception(e)
        raise {"exception": f"{e}"}
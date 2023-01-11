from typing import Any
import yaml
import logging
import requests

from datetime import timedelta
from schemas.response import CommonResponseSuccess
from utils.errors import ApiException
from fastapi import APIRouter, Body, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.token import Token,LoginInfo
from schemas.user import UserCreate

from services.cruds.user_crud import get_all_users,get_user_by_firebase_uid, set_user
from services.logs.set_logs import set_logger
from services.authenticates.authenticate_user import authenticate_user
from services.authenticates.create_access_token import create_access_token
from db import get_db

router = APIRouter()

with open('settings.yaml', 'r') as yml:
    settings = yaml.safe_load(yml)

#ログファイルを作成
_logger = logging.getLogger(__name__)
set_logger(_logger)

@router.post("/register", response_model = CommonResponseSuccess)
async def create_character(user_data:UserCreate,db:Session = Depends(get_db)):
    """
    ユーザー登録を行う。
    """
    try:
        #既に登録されているか確認を行う
        user = get_user_by_firebase_uid(user_data.firebase_uid,db)
        if not user:
            #データベースにユーザーを登録する
            user = set_user(user_data,db)
            return {"status":"ok"}
        else:
            raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="User is already registered.",
            )
        
    except ApiException as e:
        db.rollback()
        _logger.warning(f"request failed. status_code = {e.status_code} detail = {e.detail}")
        raise e

    except Exception as e:
        _logger.error(f"request failed. Error = {e}")
        db.rollback()
        raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="BadRequest",
            )
    

# @router.post("/token", response_model=Token)
# async def login_for_access_token(form_data: LoginInfo,db:Session = Depends(get_db)) -> dict:
#     """
#     ログイン認証が完了したらJWTを返す。
#     """
#     try:
#         #DBからフォームに入力されたユーザー名のユーザーを取り出す。
#         user_data = get_user_by_firebase_uid(form_data.email,db)
#         user = authenticate_user(user_data,form_data.password)
#         if not user:
#             _logger.warning(f"login: {form_data.email}[ Failure ]")
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Incorrect email or password",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
            
#         #パスワードの検証が完了したらトークンを生成
#         access_token_expires = timedelta(minutes = settings['fastapi']['token']['ACCESS_TOKEN_EXPIRE_MINUTES'])
#         access_token = create_access_token(
#             token_payload={"sub": user.email},expires_delta=access_token_expires
#         )
#         _logger.info(f"login: {form_data.email} [ Success ]")
#         return {"access_token": access_token, "token_type": "bearer"}


#     except requests.exceptions.RequestException as e:
#         _logger.exception(e)
#         raise {"exception": f"{e}"}
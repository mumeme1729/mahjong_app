"""
userのCRUD処理を実装

"""

from typing import List,Any,Dict,Optional,Union
from sqlalchemy.orm import joinedload,contains_eager
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import and_
from models.games_results import GameResultTable
from models.groups import GroupsTable
from models.profiles import ProfileTable
from schemas.group import Group
from schemas.user import UserCreate, UserUpdate
from services.authenticates.hash_and_verify_the_password import get_password_hash
from models.users import UserTable
from fastapi import HTTPException
from utils import errors
from schemas.user import User
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder

#create
def set_user(obj_in:UserCreate,db:Session)->dict:
    """
    postされたユーザー情報をDBに格納する
    """
    try:
        dt = datetime.now()
        dt.strftime("%Y/%m/%d %H:%M:%S")
    
        user = UserTable(
                # email = obj_in.email,
                # hashed_password = get_password_hash(obj_in.password),
                firebase_uid = obj_in.firebase_uid,
                is_active = obj_in.is_active,
                created_at = dt,
                nick_name = None,
                image = None
        )
        
        db.add(user)
        db.commit()
        return user
    except Exception as e:
            raise e
    

#update
def update_user_crud(user: User, update_info:UserUpdate, path:str, db: Session) -> User:
    """
    ユーザーのデータを更新する
    """
    try:
        user_table = get_user_by_id(user.id, db)
        if update_info.nick_name is not None:
            user_table.nick_name = update_info.nick_name
        if update_info.introduction is not None:
            user_table.introduction = update_info.introduction
        if path is not None:
            user_table.image = path
        db.commit()
        return user_table
    except Exception as e:
            raise e

#GET 
def get_user_by_firebase_uid(uid: str,db: Session) -> Optional[UserTable]:
        """
        指定したemailを持つユーザーを取得
        """
        try:
            return db.query(UserTable).filter(UserTable.firebase_uid == uid).options(joinedload(UserTable.profiles)).first()
        except Exception as e:
            raise e

def get_all_users(db:Session) ->List[UserTable]:
        """
        登録されている全てのユーザーを取得
        """
        try:
            users = db.query(UserTable).options(joinedload(UserTable.profiles)).all()
            return users
        except Exception as e:
            raise e

def get_user_by_id(id: str,db: Session) -> Optional[UserTable]:
        """
        指定したidを持つユーザーを取得
        """
        try:
            return db.query(UserTable).filter(UserTable.id == id).options(joinedload(UserTable.profiles)).first()
        except Exception as e:
            raise e
        
# ユーザーに関連するデータをすべて取得
def get_total_join_group_per_user(user_id: str,db: Session)->List[dict]:
    """
    指定されたユーザーの全グループを返す
    """
    try:
        get_group_query = f"""
            SELECT groups.* FROM users
            JOIN profiles ON users.id = profiles.user
            JOIN groups ON groups.id = profiles.group
            WHERE users.id::text = '{user_id}' AND profiles.is_active = true;
        """
        group_info = db.execute(get_group_query)
        group_info_list = []
        for res in group_info:
            result_dict = dict(res)
            group_info_list.append(result_dict)
        return group_info_list
    
    except Exception as e:
            raise e




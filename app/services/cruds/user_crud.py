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
from services.logs.set_logs import set_logger
from fastapi import HTTPException
from utils import errors
from schemas.user import User
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder

 #ロガーの作成
_logger = set_logger(__name__)

#create
def set_user(obj_in:UserCreate,db:Session)->dict:
    """
    postされたユーザー情報をDBに格納する
    """
    dt = datetime.now()
    dt.strftime("%Y/%m/%d %H:%M:%S")
    _logger.info(f" user_data: {obj_in}")
 
    user = UserTable(
            email = obj_in.email,
            hashed_password = get_password_hash(obj_in.password),
            is_active = obj_in.is_active,
            created_at = dt,
            nick_name = obj_in.email,
            image = None
    )
    
    db.add(user)
    db.commit()
    return user
    

#update
def update_user(db_obj: User,obj_in: Union[UserUpdate, Dict[str, Any]],
    db: Session) -> User:
    if isinstance(obj_in, dict):
        #onjがdictかどうか判定
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
        
    if "password" in update_data.keys() and update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password

    obj_data = jsonable_encoder(db_obj)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

#GET 
def get_user_by_email(email: str,db: Session) -> Optional[UserTable]:
        """
        指定したemailを持つユーザーを取得
        """
        return db.query(UserTable).filter(UserTable.email == email).options(joinedload(UserTable.profiles)).first()

def get_all_users(db:Session) ->List[UserTable]:
        """
        登録されている全てのユーザーを取得
        """
        users = db.query(UserTable).options(joinedload(UserTable.profiles)).all()
        return users

def get_user_by_id(id: str,db: Session) -> Optional[UserTable]:
        """
        指定したidを持つユーザーを取得
        """
        return db.query(UserTable).filter(UserTable.id == id).options(joinedload(UserTable.profiles)).first()

# ユーザーに関連するデータをすべて取得
def get_all_user_data(id: str,db: Session):
    """
    ホーム表示用に必要なユーザーデータを取得する

    ・ プロフィール(グループ)
    ・ すべての対局記録
    """
    # user = db.query(UserTable).\
    #     options(joinedload(UserTable.profiles)).first()
    
    # play_data = db.query(ProfileTable,GameResultTable).\
    #     outerjoin(GameResultTable,GameResultTable.profile == ProfileTable.id).all()

    # user = db.query(UserTable,ProfileTable,GameResultTable).\
    #     outerjoin(ProfileTable,ProfileTable.user == UserTable.id).\
    #         outerjoin(GameResultTable,GameResultTable.profile == ProfileTable.id).\
    #             filter(ProfileTable.is_active == True).all()

    user = db.query(UserTable,ProfileTable).\
         outerjoin(ProfileTable,ProfileTable.user == UserTable.id).\
             options(joinedload(ProfileTable.game_results)).\
                 filter(ProfileTable.is_active == True,UserTable.id == id).all()
        
    return user



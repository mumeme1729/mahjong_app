from email.mime import image
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from schemas.user import User
from datetime import datetime

from models.profiles import ProfileTable

def set_profile(user:User,group_id:UUID,db:Session):
    """
    userのデータを受け取りプロフィールを作成する
    """
    dt = datetime.now()
    dt.strftime("%Y/%m/%d %H:%M:%S")

    profile = ProfileTable(
            nick_name = user.nick_name,
            image = user.image,
            created_at = dt,
            update_at = dt,
            group = group_id,
            user = user.id
    )

    db.add(profile)
    db.commit()
    return profile.id
    

def get_profile_by_user_id(user_id:UUID,db:Session)-> List[ProfileTable]:
    """
    user_idを受け取り、それに一致するprofileを返す
    """
    return db.query(ProfileTable).options(joinedload(ProfileTable.groups)).filter(ProfileTable.user == user_id).all()

def get_profile_by_id(id:UUID,db:Session)-> ProfileTable:
    """
    idを複数受け取り、それに一致するprofileを返す
    """
    return db.query(ProfileTable).filter(ProfileTable.id == id).first()

def get_profile_by_user_and_group(user_id:UUID,group_id:UUID,db:Session)->Optional[ProfileTable]:
    """
    ユーザーidとグループidからプロフィールを取得する
    """
    return db.query(ProfileTable).filter(ProfileTable.user == user_id,ProfileTable.group == group_id).first()

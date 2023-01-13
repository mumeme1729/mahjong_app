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
    try:
        dt = datetime.now()
        dt.strftime("%Y/%m/%d %H:%M:%S")

        profile = ProfileTable(
                nick_name = user.nick_name,
                image = user.image,
                created_at = dt,
                update_at = dt,
                group = group_id,
                user = user.id,
                rate4 = 1500,
                rate3 = 1500
        )

        db.add(profile)
        db.commit()
        return profile.id
    except Exception as e:
            raise e

def update_profile_rate(db:Session):
    """
    レートを更新する
    """
    try:
        db.commit()
        return True
    except Exception as e:
        raise e

def activate_profile(profile:ProfileTable,db:Session)->UUID:
    """
    対象のプロフィールを有効化(グループに参加)
    """
    try:
        profile.is_active = True
        db.commit()
        return profile
    except Exception as e:
            raise e

def dis_activate_profile(profile:ProfileTable,db:Session)->UUID:
    """
    対象のプロフィールを非アクティブ化(グループ離脱)
    """
    try:
        profile.is_active = False
        db.commit()
        return profile
    except Exception as e:
            raise e

def get_profile_by_user_id(user_id:UUID,db:Session)-> List[ProfileTable]:
    """
    user_idを受け取り、それに一致するprofileを返す
    """
    try:
        return db.query(ProfileTable).options(joinedload(ProfileTable.groups)).filter(ProfileTable.user == user_id).all()
    except Exception as e:
        raise e

def get_profile_by_id(id:UUID,db:Session)-> ProfileTable:
    """
    idを複数受け取り、それに一致するprofileを返す
    """
    try:
        return db.query(ProfileTable).filter(ProfileTable.id == id).first()
    except Exception as e:
            raise e

def get_profile_by_user_and_group(user_id:UUID, group_id:UUID,db:Session)->Optional[ProfileTable]:
    """
    ユーザーidとグループidからプロフィールを取得する
    """
    try:
        return db.query(ProfileTable).filter(ProfileTable.user == user_id,ProfileTable.group == group_id).first()
    except Exception as e:
            raise e

def get_profile_by_profile_and_group(profile_id:UUID, group_id:UUID,db:Session)->Optional[ProfileTable]:
    """
    profileidとグループidからプロフィールを取得する
    """
    try:
        return db.query(ProfileTable).filter(ProfileTable.id == profile_id, ProfileTable.group == group_id).first()
    except Exception as e:
            raise e
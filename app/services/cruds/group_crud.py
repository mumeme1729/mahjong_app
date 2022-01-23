"""
profileのCRUD処理を実装

"""

from typing import List
from uuid import UUID
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from services.cruds.profile_crud import dis_activate_profile
from services.cruds.profile_crud import activate_profile
from models.games import GamesTable
from services.cruds.profile_crud import get_profile_by_user_and_group, set_profile
from services.cruds.profile_crud import get_profile_by_user_id,get_profile_by_id
from schemas.group import GroupCreate
from services.cruds.user_crud import get_user_by_id
from schemas.user import User
from models.groups import GroupsTable
from services.logs.set_logs import set_logger
from fastapi import HTTPException,status
from datetime import datetime

 #ロガーの作成
_logger = set_logger(__name__)

#post
def set_group(group:GroupCreate,user:User,db:Session)->dict:
    """
    postされたgroup情報をDBに格納する
    """
    dt = datetime.now()
    dt.strftime("%Y/%m/%d %H:%M:%S")

    group = GroupsTable(
            title = group.title,
            password = group.password,
            text = group.text,
            image = group.image,
            created_at = dt,
            update_at = dt,
    )

    #group.users.append(get_user_by_id(user.id,db))

    db.add(group)
    db.commit()
    return group.id

#update
def join_group(group_id:UUID,password:str,user_id:UUID,db:Session)->UUID:
    """
    指定したグループに追加する
    パスワードが一致した場合に追加
    """
    target_group = get_group_by_id(group_id,db)
    if target_group:
        # passwordチェック
        if target_group.password != password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password does not match",
            )
        # 既に参加しているかどうかチェック
        profile = get_profile_by_user_and_group(user_id,target_group.id,db)
        if profile is not None:
            if profile.is_active:
                # 既に参加している場合
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="already joined this group",
                )
            else:
                # プロフィールを有効化させる
                res = activate_profile(profile,db)
                if res: 
                    return target_group.id
        
        # グループに参加させる
        # profileを作成
        user = get_user_by_id(user_id,db)
        profile_id = set_profile(user, group_id, db)
        if profile_id is None:
            _logger.error(f"Cloud not create user profile user_id:{user_id} group_id:{group_id}")
            raise  HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cloud not create user profile",
            )
        db.commit()
        return profile_id
    else:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group does not exist",
        )

#GET(idより)
def get_group_by_id(group_id:UUID,db:Session)-> GroupsTable:
    """
    idを複数受け取り、それに一致するグループを返す
    """
    return db.query(GroupsTable).options(joinedload(GroupsTable.profiles)).filter(GroupsTable.id == group_id).first()


def get_all_groups(db:Session)->List[GroupsTable]:
    """
    すべてのグループを返す
    """
    groups = db.query(GroupsTable).options(joinedload(GroupsTable.profiles)).options(joinedload(GroupsTable.games)).all()
    return groups

### DELETE ###
def leave_group(group_id:UUID,user_id:UUID,db:Session)->UUID:
    """
    ユーザーをグループから離脱させる
    """
    target_group = get_group_by_id(group_id,db)
    if target_group:
        # 既に参加しているかどうかチェック
        profile = get_profile_by_user_and_group(user_id,target_group.id,db)
        if profile is not None:
            if profile.is_active:
                # 既に参加している場合、非アクティブに
                res = dis_activate_profile(profile,db)
                return target_group.id
            else:
                _logger.warning(f"this user has already leaved this group")
                # 既に非アクティブ 
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="this user has already leaved this group",
                )
        else:
            _logger.warning(f"this user doesn't join this group")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="this user doesn't join this group",
            )
    else:
        _logger.warning(f"Group does not exist")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group does not exist",
        )
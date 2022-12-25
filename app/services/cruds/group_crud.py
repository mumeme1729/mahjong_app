"""
profileのCRUD処理を実装

"""

from typing import List
from uuid import UUID
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from utils.errors import ApiException
from services.cruds.game_crud import get_recently_game
from services.cruds.profile_crud import dis_activate_profile
from services.cruds.profile_crud import activate_profile
from models.games import GamesTable
from services.cruds.profile_crud import get_profile_by_user_and_group, set_profile
from services.cruds.profile_crud import get_profile_by_user_id,get_profile_by_id
from schemas.group import GroupCreate
from services.cruds.user_crud import get_user_by_id
from schemas.user import User
from models.groups import GroupsTable
from fastapi import HTTPException,status
from datetime import datetime


#post
def set_group(group:GroupCreate,user:User,db:Session)->dict:
    """
    postされたgroup情報をDBに格納する
    """
    try:
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
    except Exception as e:
            raise e

#update
def join_group(group_id:UUID,password:str,user_id:UUID,db:Session)->UUID:
    """
    指定したグループに追加する
    パスワードが一致した場合に追加
    """
    try:
        target_group = get_group_by_id(group_id,db)
        if target_group:
            # passwordチェック
            if target_group.password != password:
                raise ApiException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    status="fail",
                    detail="Password does not match",
                )
            # 既に参加しているかどうかチェック
            profile = get_profile_by_user_and_group(user_id,target_group.id,db)
            if profile is not None:
                if profile.is_active:
                    # 既に参加している場合
                    raise ApiException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        status="fail",
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
                raise  ApiException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status="fail",
                    detail="Cloud not create user profile",
                )
            db.commit()
            return profile_id
        else:
            return ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="Group does not exist",
            )
    except ApiException as e:
        raise e
    
    except Exception as e:
            raise e

#GET(idより)
def get_group_by_id(group_id:UUID,db:Session)-> GroupsTable:
    """
    idを複数受け取り、それに一致するグループを返す
    """
    try:
        return db.query(GroupsTable).options(joinedload(GroupsTable.profiles)).filter(GroupsTable.id == group_id).first()
    except Exception as e:
            raise e

def get_all_groups(db:Session)->List[GroupsTable]:
    """
    すべてのグループを返す
    """
    try:
        groups = db.query(GroupsTable).options(joinedload(GroupsTable.profiles)).options(joinedload(GroupsTable.games)).all()
        return groups
    except Exception as e:
            raise e

def get_selected_group(group_id:str,db:Session):
    """
    選択したグループを返す

    """
    try:
        group = db.query(GroupsTable).\
            options(joinedload(GroupsTable.profiles)).\
                filter(GroupsTable.id == group_id).\
                    all()
        # 直近の対局記録
        game = get_recently_game(group_id,db)
        group.append({"Games":game})
        
        return group
    except Exception as e:
        raise e
    
    # def get_alias_infos_with_pagination（user、page_id = 0、query = None）-> [AliasInfo]：
    # ret = []
    # q =（
    #     db.session.query（Alias）
    #     .options（joinedload（Alias.mailbox））
    #     .filter（Alias.user_id == user.id）
    #     .order_by(Alias.created_at.desc())
    # )

    # if query:
    #     q = q.filter(
    #         or_(Alias.email.ilike(f"%{query}%"), Alias.note.ilike(f"%{query}%"))
    #     )

    # q = q.limit(PAGE_LIMIT).offset(page_id * PAGE_LIMIT)

    # for alias in q:
    #     ret.append(get_alias_info(alias))

    # return ret 



### DELETE ###
def leave_group(group_id:UUID,user_id:UUID,db:Session)->UUID:
    """
    ユーザーをグループから離脱させる
    """
    try:
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
                    # 既に非アクティブ 
                    raise ApiException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        status="fail",
                        detail="this user has already leaved this group",
                    )
            else:
                raise ApiException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status="fail",
                    detail="this user doesn't join this group",
                )
        else:
            raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="Group does not exist",
            )

    except ApiException as e:
        raise e
    
    except Exception as e:
            raise e
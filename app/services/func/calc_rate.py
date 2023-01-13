
from typing import List
from services.cruds.profile_crud import update_profile_rate
from models.profiles import ProfileTable
from schemas.game import GameCreate
from sqlalchemy.orm.session import Session

def calc_rate_4(game_data:GameCreate, profiles:List[ProfileTable], db:Session):
    """
    4人麻雀時のレートを計算する
    """
    
    # 参加者全員のレート合計から平均値を算出する
    total_rate = 0
    for profile in profiles:
        total_rate += profile.rate4
    # 同卓者のレートの平均値
    average_rate = round(total_rate/4)
    #レート更新
    results = game_data.game_results
    for result in results:
        for profile in profiles:
            # プロフィールが一致するもの
            if result.profile == profile.id:
                if result.rank == 1:
                    profile.rate4 = round(profile.rate4+(50+((average_rate - profile.rate4)/70)*0.2))
                elif result.rank == 2:
                    profile.rate4 = round(profile.rate4+(10+((average_rate - profile.rate4)/70)*0.2))
                elif result.rank == 3:
                    profile.rate4 = round(profile.rate4+(-20+((average_rate - profile.rate4)/70)*0.2))
                else:
                    profile.rate4 = round(profile.rate4+(-40+((average_rate - profile.rate4)/70)*0.2))
    # 結果をコミットする
    update_profile_rate(db)

def calc_rate_3(game_data:GameCreate, profiles:List[ProfileTable], db:Session):
    """
    3麻雀時のレートを計算する
    """
    
    # 参加者全員のレート合計から平均値を算出する
    total_rate = 0
    for profile in profiles:
        total_rate += profile.rate3
    # 同卓者のレートの平均値
    average_rate = round(total_rate/3)
    #レート更新
    results = game_data.game_results
    for result in results:
        for profile in profiles:
            # プロフィールが一致するもの
            if result.profile == profile.id:
                if result.rank == 1:
                    profile.rate3 = round(profile.rate3+(50+((average_rate - profile.rate3)/70)*0.2))
                elif result.rank == 2:
                    profile.rate3 = round(profile.rate3+(10+((average_rate - profile.rate3)/70)*0.2))
                else:
                    profile.rate3 = round(profile.rate3+(-50+((average_rate - profile.rate3)/70)*0.2))
    # 結果をコミットする
    update_profile_rate(db)

from models.users import UserTable
from services.authenticates.hash_and_verify_the_password import verify_password
from services.logs.set_logs import set_logger

 #ロガーの作成
_logger = set_logger(__name__)
def authenticate_user(user_data: UserTable, password: str) -> UserTable:
    """
    ログインしたユーザーの認証を確認する。
    
    Parameters
    
    ----------
    user_data : UserTable
        ログインするユーザー情報
    password : str
        ログイン時に入力したパスワード
    
    """

    # DBからユーザー情報を検証する
    user = user_data
    if not user:
        _logger.warning("User does not exist.")
        return False
    # 保存されているパスワードのハッシュと入力されたパスワードのハッシュを検証
    if not verify_password(password, user.hashed_password):
        _logger.warning("Passwords do not match.")
        return False
    _logger.info("authenticate: OK")
    return user
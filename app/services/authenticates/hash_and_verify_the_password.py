from passlib.context import CryptContext #パスワードをハッシュ化するために使用

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    """
    パスワードが保存されているハッシュと等しいかどうか検証する
    
    Parameters

    ----------
    plain_password : str
        平文のパスワード
    hashed_password : str
        ハッシュ化されたパスワード
    """
    return _pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """
    パスワードをハッシュ化
    
    Parameters

    ----------
    password : str
        平文のパスワード
    """
    return _pwd_context.hash(password)


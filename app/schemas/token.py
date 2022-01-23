from pydantic import BaseModel,EmailStr
from typing import Optional

class Token(BaseModel):
    """
    JWTのschema
    """
    access_token: str
    token_type: str

class LoginInfo(BaseModel):
    """
    ログイン時(トークン発行)に必要なschema
    """
    email: EmailStr
    password: str

class TokenData(BaseModel):
    """
    jwtの中に含める情報のschema
    """
    username: Optional[str] = None
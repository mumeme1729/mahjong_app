from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """
    JWTのschema
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    jwtの中に含める情報のschema
    """
    username: Optional[str] = None
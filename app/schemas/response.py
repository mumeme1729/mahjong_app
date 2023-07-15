from pydantic import BaseModel,EmailStr
from typing import Optional

class CommonResponseBase(BaseModel):
    """
    レスポンスの基本schema
    """
    # email: Optional[EmailStr] = None
    status: Optional[str] = None
    detail: Optional[str] = None

class CommonResponseSuccess(CommonResponseBase):
    """
    status OKを返す場合のスキーマ
    """
    status: str
    






        

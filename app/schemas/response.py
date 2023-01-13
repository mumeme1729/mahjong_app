from pydantic import BaseModel,EmailStr
from typing import Optional

class CommonResponseBase(BaseModel):
    """
    レスポンスの基本schema
    """
    # email: Optional[EmailStr] = None
    status: Optional[str] = None

class CommonResponseSuccess(CommonResponseBase):
    """
    status OKだけを返す場合のスキーマ
    """
    status: str







        

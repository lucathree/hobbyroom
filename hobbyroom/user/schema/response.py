from pydantic import BaseModel, EmailStr


class UserToken(BaseModel):
    token: str


class UserInfo(BaseModel):
    email: EmailStr

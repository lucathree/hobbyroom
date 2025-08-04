from pydantic import BaseModel, EmailStr


class AuthorizeUser(BaseModel):
    email: EmailStr
    password: str

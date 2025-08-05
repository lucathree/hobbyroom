from pydantic import BaseModel, EmailStr


class AuthorizeUser(BaseModel):
    email: EmailStr
    password: str


class AuthorizePersona(BaseModel):
    persona_id: str
    user_jwt: str | None = None

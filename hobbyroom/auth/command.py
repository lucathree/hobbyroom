from uuid import UUID

from pydantic import BaseModel, EmailStr


class AuthorizeUser(BaseModel):
    email: EmailStr
    password: str


class AuthorizePersona(BaseModel):
    persona_id: UUID
    user_jwt: str | None = None

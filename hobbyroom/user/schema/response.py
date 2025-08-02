from typing import Self

from pydantic import BaseModel, EmailStr

from hobbyroom import auth


class UserToken(BaseModel):
    token: str


class UserPersona(BaseModel):
    id: str
    name: str


class UserInfo(BaseModel):
    email: EmailStr
    personas: list[UserPersona]

    @classmethod
    def from_auth_vo(cls, user: auth.User) -> Self:
        return cls(
            email=user.email,
            personas=[
                UserPersona(id=str(persona.id), name=persona.name)
                for persona in user.personas
            ],
        )

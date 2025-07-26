from typing import Self

from pydantic import BaseModel, EmailStr

from hobbyroom.user import domain


class UserToken(BaseModel):
    token: str


class UserPersona(BaseModel):
    id: str
    name: str


class UserInfo(BaseModel):
    email: EmailStr
    personas: list[UserPersona]

    @classmethod
    def from_domain(cls, user: domain.User) -> Self:
        return cls(
            email=user.email,
            personas=[
                UserPersona(id=str(persona.id), name=persona.name)
                for persona in user.personas
            ],
        )

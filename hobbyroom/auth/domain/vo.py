from collections.abc import Callable
from typing import Self
from uuid import UUID

import pendulum
from pydantic import BaseModel, EmailStr, Field

from hobbyroom import database
from hobbyroom.settings import settings


class JWTPayload(BaseModel):
    sub: str
    iat: int
    exp: int
    persona: str | None = None
    affiliated_gatherings: list[UUID] | None = None

    @classmethod
    def create(cls, user_email: str, clock: Callable[..., pendulum.DateTime]) -> Self:
        current_time = clock()
        expiration_time = current_time + settings.jwt_expiration_timedelta

        return cls(
            sub=user_email,
            iat=int(current_time.timestamp()),
            exp=int(expiration_time.timestamp()),
        )

    def is_expired(self, current_time: pendulum.DateTime) -> bool:
        return self.exp < current_time.timestamp()


class Persona(BaseModel):
    id: UUID
    name: str


class User(BaseModel):
    id: UUID
    email: EmailStr
    password: str | None = None
    personas: list[Persona] = Field(default_factory=list)

    @classmethod
    def from_orm(cls, user_obj: database.User) -> Self:
        return cls(
            id=user_obj.id,
            email=user_obj.email,
            password=user_obj.password,
            personas=[
                Persona.model_validate(persona.to_dict())
                for persona in user_obj.personas
            ],
        )


class Affiliation(BaseModel):
    persona_id: UUID
    gathering_id: UUID

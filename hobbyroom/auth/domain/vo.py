from collections.abc import Callable
from typing import Self
from uuid import UUID

import pendulum
from pydantic import BaseModel, EmailStr, Field

from hobbyroom import database, exceptions
from hobbyroom.settings import settings


class JWTPayload(BaseModel):
    sub: str
    iat: int
    exp: int
    persona: str | None = None
    affiliated_gatherings: list[str] | None = None

    @classmethod
    def create(cls, user_email: str, clock: Callable[..., pendulum.DateTime]) -> Self:
        current_time = clock()
        expiration_time = current_time + settings.jwt_expiration_timedelta

        return cls(
            sub=user_email,
            iat=int(current_time.timestamp()),
            exp=int(expiration_time.timestamp()),
        )

    @property
    def persona_id(self) -> UUID | None:
        return UUID(self.persona) if self.persona else None

    def is_expired(self, current_time: pendulum.DateTime) -> bool:
        return self.exp < current_time.timestamp()

    def update_persona_info(
        self,
        persona_id: str,
        affiliated_gathering_ids: list[str],
        clock: Callable[..., pendulum.DateTime],
    ) -> Self:
        current_time = clock()
        expiration_time = current_time + settings.jwt_expiration_timedelta

        return self.model_copy(
            update={
                "persona": persona_id,
                "affiliated_gatherings": affiliated_gathering_ids,
                "iat": int(current_time.timestamp()),
                "exp": int(expiration_time.timestamp()),
            }
        )


class Persona(BaseModel):
    id: UUID
    name: str
    _gathering_id: UUID | None = None

    @property
    def gathering_id(self) -> UUID:
        if self._gathering_id is None:
            raise exceptions.DomainValidationError("현재 모임 정보가 없습니다.")
        return self._gathering_id

    def add_gathering_id(
        self, affiliated_gathering_ids: list[str], current_gathering_id: UUID
    ) -> None:
        gathering_ids = [UUID(id) for id in affiliated_gathering_ids]
        if current_gathering_id not in gathering_ids:
            raise exceptions.UnauthorizedError(
                "현재 모임 정보에 소속되어 있지 않은 페르소나입니다."
            )
        self._gathering_id = current_gathering_id


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

    def find_persona(self, persona_id: UUID) -> Persona | None:
        return next(
            (persona for persona in self.personas if persona.id == persona_id),
            None,
        )


class Affiliation(BaseModel):
    persona_id: UUID
    gathering_id: UUID

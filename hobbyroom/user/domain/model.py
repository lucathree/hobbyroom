import datetime
from typing import Self
from uuid import UUID

import pendulum
from pydantic import BaseModel, EmailStr

from hobbyroom import exceptions


class User(BaseModel):
    id: UUID
    email: EmailStr
    password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @classmethod
    def create(
        cls,
        id: UUID,
        email: EmailStr,
        hashed_password: str,
        created_at: pendulum.DateTime,
    ) -> Self:
        return cls(
            id=id,
            email=email,
            password=hashed_password,
            created_at=created_at,
            updated_at=created_at,
        )


class Persona(BaseModel):
    id: UUID
    name: str
    user_id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @classmethod
    def create(
        cls,
        id: UUID,
        name: str,
        user_id: UUID,
        created_at: pendulum.DateTime,
    ) -> Self:
        if user_id is None:
            raise exceptions.DomainValidationError(
                "페르소나 생성을 위해서는 사용자 ID가 필요합니다."
            )
        return cls(
            id=id,
            name=name,
            user_id=user_id,
            created_at=created_at,
            updated_at=created_at,
        )

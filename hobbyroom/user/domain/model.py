import datetime
from typing import Self
import pendulum
from pydantic import BaseModel, EmailStr
from uuid import UUID


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

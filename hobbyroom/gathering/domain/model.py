import datetime
from typing import Self
from uuid import UUID

import pendulum
from pydantic import BaseModel


class Gathering(BaseModel):
    id: UUID
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @classmethod
    def create(
        cls,
        id: UUID,
        name: str,
        description: str,
        created_at: pendulum.DateTime,
    ) -> Self:
        return cls(
            id=id,
            name=name,
            description=description,
            created_at=created_at,
            updated_at=created_at,
        )


class Affiliation(BaseModel):
    persona_id: UUID
    gathering_id: UUID
    is_leader: bool
    joined_at: datetime.datetime

    @classmethod
    def create_leader(
        cls,
        persona_id: UUID,
        gathering_id: UUID,
        joined_at: pendulum.DateTime,
    ) -> Self:
        return cls(
            persona_id=persona_id,
            gathering_id=gathering_id,
            is_leader=True,
            joined_at=joined_at,
        )

    @classmethod
    def create_member(
        cls,
        persona_id: UUID,
        gathering_id: UUID,
        joined_at: pendulum.DateTime,
    ) -> Self:
        return cls(
            persona_id=persona_id,
            gathering_id=gathering_id,
            is_leader=False,
            joined_at=joined_at,
        )

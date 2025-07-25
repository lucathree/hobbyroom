import datetime
from uuid import UUID

from pydantic import BaseModel


class Gathering(BaseModel):
    id: UUID
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class Affiliation(BaseModel):
    persona_id: UUID
    gathering_id: UUID
    is_leader: bool
    joined_at: datetime.datetime


class Persona(BaseModel):
    id: UUID
    name: str
    user_id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime

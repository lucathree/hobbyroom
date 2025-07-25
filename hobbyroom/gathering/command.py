from uuid import UUID

from pydantic import BaseModel

from hobbyroom.gathering import domain


class CreateGathering(BaseModel):
    name: str
    description: str
    persona_id: UUID
    user: domain.User | None = None

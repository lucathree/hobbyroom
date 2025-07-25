from uuid import UUID

from pydantic import BaseModel, Field

from hobbyroom.gathering.domain import model


class User(BaseModel):
    id: UUID
    personas: list[model.Persona] = Field(default_factory=list)

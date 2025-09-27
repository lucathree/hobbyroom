from uuid import UUID

from pydantic import BaseModel


class ConnectionInfo(BaseModel):
    persona_id: UUID
    persona_name: str
    gathering_id: UUID

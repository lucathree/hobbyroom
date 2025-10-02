from typing import Self
from uuid import UUID

from fastapi import WebSocket
from pydantic import BaseModel, ConfigDict, Field


class ConnectionInfo(BaseModel):
    persona_id: UUID
    persona_name: str
    gathering_id: UUID


class PersonaConnection(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    persona_id: UUID
    persona_name: str
    connections: set[WebSocket]

    @classmethod
    def create(cls, connection_info: ConnectionInfo, websocket: WebSocket) -> Self:
        return cls(
            persona_id=connection_info.persona_id,
            persona_name=connection_info.persona_name,
            connections={websocket},
        )

    @property
    def has_single_connection(self) -> bool:
        return len(self.connections) == 1

    def remove_connection(self, websocket: WebSocket) -> None:
        self.connections.remove(websocket)


class GatheringConnection(BaseModel):
    gathering_id: UUID
    persona_connections: list[PersonaConnection] = Field(default_factory=list)

    @property
    def active_websockets(self) -> set[WebSocket]:
        return {
            websocket for pc in self.persona_connections for websocket in pc.connections
        }

    @property
    def has_connections(self) -> bool:
        self.refresh_connections()
        return bool(self.persona_connections)

    def refresh_connections(self) -> None:
        self.persona_connections = [
            pc for pc in self.persona_connections if pc.connections
        ]

    def upsert_persona_connection(
        self, connection_info: ConnectionInfo, websocket: WebSocket
    ) -> PersonaConnection:
        persona_connection = self.find_persona_connection(connection_info.persona_id)
        if persona_connection is None:
            persona_connection = PersonaConnection.create(connection_info, websocket)
            self.persona_connections.append(persona_connection)
        else:
            persona_connection.connections.add(websocket)
        return persona_connection

    def find_persona_connection(self, persona_id: UUID) -> PersonaConnection | None:
        return next(
            (pc for pc in self.persona_connections if pc.persona_id == persona_id), None
        )

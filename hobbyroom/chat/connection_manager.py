from collections import defaultdict
from collections.abc import Callable
from uuid import UUID

import pendulum
from fastapi import WebSocket, WebSocketDisconnect, WebSocketException, status

from hobbyroom import auth
from hobbyroom.chat import enums, schema


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[UUID, list[WebSocket]] = defaultdict(list)
        self.clock: Callable[..., pendulum.DateTime]

    async def connect(self, websocket: WebSocket, persona: auth.Persona):
        await websocket.accept()
        self.active_connections[persona.gathering_id].append(websocket)

        join_message = schema.UserMessage(
            content=f"{persona.name}님이 채팅방에 입장했습니다.",
            message_type=enums.MessageType.JOIN,
            persona_id=persona.id,
            persona_name=persona.name,
            timestamp=self.clock(),
        )
        await self.broadcast_to_gathering(
            gathering_id=persona.gathering_id,
            message=join_message,
        )

    async def disconnect(self, websocket: WebSocket, persona: auth.Persona):
        self.active_connections[persona.gathering_id].remove(websocket)
        if not self.active_connections[persona.gathering_id]:
            self.refresh_connections()
            return

        leave_message = schema.UserMessage(
            content=f"{persona.name}님이 채팅방을 나갔습니다.",
            message_type=enums.MessageType.LEAVE,
            persona_id=persona.id,
            persona_name=persona.name,
            timestamp=self.clock(),
        )
        await self.broadcast_to_gathering(
            gathering_id=persona.gathering_id,
            message=leave_message,
        )

    async def broadcast_to_gathering(
        self, gathering_id: UUID, message: schema.OutgoingMessage
    ):
        connections: list[WebSocket] = self.active_connections.get(gathering_id, [])
        if not connections:
            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="해당 모임에 연결된 사용자가 없습니다.",
            )
        message_data = message.model_dump_json()
        for websocket in connections:
            try:
                await websocket.send_text(message_data)
            except WebSocketDisconnect:
                continue

    def refresh_connections(self):
        self.active_connections = {
            gathering_id: connections
            for gathering_id, connections in self.active_connections.items()
            if connections
        }

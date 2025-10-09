import json
from collections import defaultdict
from collections.abc import Callable
from uuid import UUID

import pendulum
import pydantic
from fastapi import WebSocket, WebSocketDisconnect

from hobbyroom import exceptions
from hobbyroom.chat import adapter, domain, enums, schema
from hobbyroom.logging import get_logger

logger = get_logger()


class ConnectionManager:
    def __init__(
        self,
        connection_info_repository: adapter.RedisConnectionInfoRepository,
        clock: Callable[..., pendulum.DateTime],
    ):
        self.active_connections: dict[UUID, list[WebSocket]] = defaultdict(list)
        self.connection_info_repository = connection_info_repository
        self.clock = clock

    async def connect(
        self, websocket: WebSocket, connection_info: domain.ConnectionInfo
    ) -> None:
        await websocket.accept()

        await self.connection_info_repository.add_connection_info(
            gathering_id=connection_info.gathering_id,
            persona_id=connection_info.persona_id,
        )
        self.active_connections[connection_info.gathering_id].append(websocket)
        logger.info(f"Connection Added: {connection_info}")

        connection_count = (
            await self.connection_info_repository.retrieve_persona_connection_count(
                gathering_id=connection_info.gathering_id,
                persona_id=connection_info.persona_id,
            )
        )
        if connection_count == 1:
            join_message = schema.UserMessage(
                content=f"{connection_info.persona_name}님이 채팅방에 입장했습니다.",
                message_type=enums.MessageType.JOIN,
                persona_id=connection_info.persona_id,
                persona_name=connection_info.persona_name,
                timestamp=self.clock(),
            )
            await self.broadcast_to_gathering(
                gathering_id=connection_info.gathering_id,
                message=join_message,
            )

    async def disconnect(
        self, websocket: WebSocket, connection_info: domain.ConnectionInfo
    ) -> None:
        try:
            persona_connection = self.retrieve_persona_connection(
                gathering_id=connection_info.gathering_id,
                persona_id=connection_info.persona_id,
            )
        except exceptions.DomainValidationError:
            logger.warning(
                f"Persona connection not found during disconnect: {connection_info}"
            )
            return

        persona_connection.remove_connection(websocket)
        if not persona_connection.connections:
            leave_message = schema.UserMessage(
                content=f"{connection_info.persona_name}님이 채팅방을 나갔습니다.",
                message_type=enums.MessageType.LEAVE,
                persona_id=connection_info.persona_id,
                persona_name=connection_info.persona_name,
                timestamp=self.clock(),
            )
            await self.broadcast_to_gathering(
                gathering_id=connection_info.gathering_id,
                message=leave_message,
            )
        logger.info(f"Connection Removed: {connection_info}")

    async def receive_message(
        self, websocket: WebSocket, connection_info: domain.ConnectionInfo
    ) -> None:
        try:
            message_data = await websocket.receive_json()
            incoming_message = schema.IncomingMessage.model_validate(message_data)
        except (json.JSONDecodeError, pydantic.ValidationError):
            error_message = schema.SystemMessage(
                content="잘못된 메시지 형식입니다.",
                timestamp=self.clock(),
            )
            await websocket.send_text(error_message.model_dump_json())
            return

        outgoing_message = schema.UserMessage(
            content=incoming_message.content,
            message_type=incoming_message.message_type,
            persona_id=connection_info.persona_id,
            persona_name=connection_info.persona_name,
            timestamp=self.clock(),
        )
        await self.broadcast_to_gathering(
            gathering_id=connection_info.gathering_id,
            message=outgoing_message,
        )

    async def broadcast_to_gathering(
        self, gathering_id: UUID, message: schema.OutgoingMessage
    ) -> None:
        gathering_connections = self.active_connections.get(gathering_id, [])
        message_data = message.model_dump_json()
        logger.info(f"Broadcasting message: {message_data}")

        for websocket in gathering_connections:
            try:
                await websocket.send_text(message_data)
            except WebSocketDisconnect:
                logger.warning("WebSocket disconnected during broadcast")
                continue

    def refresh_connections(self) -> None:
        active_connections = {}
        for gathering_id, gathering_connection in self.active_connections.items():
            gathering_connection.refresh_persona_connections()
            if gathering_connection.has_connections:
                active_connections[gathering_id] = gathering_connection

        self.active_connections = active_connections
        logger.info(f"Refreshed connections: {self.active_connections}")

    def retrieve_gathering_connection(
        self, gathering_id: UUID
    ) -> domain.GatheringConnection:
        connection = self.active_connections.get(gathering_id)
        if connection is None:
            raise exceptions.DomainValidationError("모임 연결 정보를 찾을 수 없습니다.")
        return connection

    def retrieve_persona_connection(
        self, gathering_id: UUID, persona_id: UUID
    ) -> domain.PersonaConnection:
        gathering_connection = self.retrieve_gathering_connection(gathering_id)
        persona_connection = gathering_connection.find_persona_connection(persona_id)
        if persona_connection is None:
            raise exceptions.DomainValidationError(
                "페르소나 연결 정보를 찾을 수 없습니다."
            )
        return persona_connection

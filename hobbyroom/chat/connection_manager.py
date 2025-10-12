import asyncio
import json
from collections import defaultdict
from collections.abc import Callable
from uuid import UUID

import pendulum
import pydantic
from fastapi import WebSocket

from hobbyroom.chat import adapter, domain, enums, schema
from hobbyroom.logging import get_logger

logger = get_logger()


class ConnectionManager:
    def __init__(
        self,
        connection_repository: adapter.RedisConnectionRepository,
        clock: Callable[..., pendulum.DateTime],
    ):
        self.local_connections: dict[UUID, list[WebSocket]] = defaultdict(list)
        self.connection_repository = connection_repository
        self.clock = clock
        self.redis_pubsub = None
        self.listener_task = None

    async def start(self):
        self.redis_pubsub = self.connection_repository.get_pubsub()
        self.listener_task = asyncio.create_task(self.listen_to_messages())

    async def stop(self):
        if self.listener_task:
            self.listener_task.cancel()
            try:
                await self.listener_task
            except asyncio.CancelledError:
                pass
        if self.redis_pubsub:
            await self.redis_pubsub.close()

    async def connect(
        self, websocket: WebSocket, connection_info: domain.ConnectionInfo
    ) -> None:
        await websocket.accept()
        await self.connection_repository.add_connection_info(
            gathering_id=connection_info.gathering_id,
            persona_id=connection_info.persona_id,
        )
        gathering_connections = self.local_connections[connection_info.gathering_id]
        if not gathering_connections:
            await self.redis_pubsub.subscribe(
                f"chat:gathering:{connection_info.gathering_id}"
            )
        gathering_connections.append(websocket)

        connection_count = (
            await self.connection_repository.retrieve_persona_connection_count(
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
            await self.connection_repository.publish_message(
                gathering_id=connection_info.gathering_id,
                json_message=join_message.model_dump_json(),
            )
        logger.info(f"Connection Added: {connection_info} | Count: {connection_count}")

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
        await self.connection_repository.publish_message(
            gathering_id=connection_info.gathering_id,
            json_message=outgoing_message.model_dump_json(),
        )

    async def disconnect(
        self, websocket: WebSocket, connection_info: domain.ConnectionInfo
    ) -> None:
        self.local_connections[connection_info.gathering_id].remove(websocket)
        await self.connection_repository.remove_connection_info(
            gathering_id=connection_info.gathering_id,
            persona_id=connection_info.persona_id,
        )
        connection_count = (
            await self.connection_repository.retrieve_persona_connection_count(
                gathering_id=connection_info.gathering_id,
                persona_id=connection_info.persona_id,
            )
        )
        if connection_count < 1:
            leave_message = schema.UserMessage(
                content=f"{connection_info.persona_name}님이 채팅방을 나갔습니다.",
                message_type=enums.MessageType.LEAVE,
                persona_id=connection_info.persona_id,
                persona_name=connection_info.persona_name,
                timestamp=self.clock(),
            )
            await self.connection_repository.publish_message(
                gathering_id=connection_info.gathering_id,
                json_message=leave_message.model_dump_json(),
            )
        logger.info(
            f"Connection Removed: {connection_info} | Count: {connection_count}"
        )
        if not self.local_connections[connection_info.gathering_id]:
            await self.redis_pubsub.unsubscribe(
                f"chat:gathering:{connection_info.gathering_id}"
            )

    async def listen_to_messages(self) -> None:
        try:
            async for message in self.redis_pubsub.listen():
                if message["type"] == "message":
                    gathering_id = UUID(message["channel"].split(":")[-1])
                    await self.broadcast_message(gathering_id, message["data"])
        except Exception as e:
            logger.error(f"Error while listening to messages: {e}")

    async def broadcast_message(self, gathering_id: UUID, json_message: str) -> None:
        connections = self.local_connections[gathering_id]
        disconnected_connections = []

        for websocket in connections:
            try:
                await websocket.send_json(json_message)
            except Exception as e:
                logger.error(f"Error sending message to WebSocket: {e}")
                disconnected_connections.append(websocket)

        for websocket in disconnected_connections:
            connections.remove(websocket)

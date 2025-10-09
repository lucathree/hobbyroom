from uuid import UUID

from redis.asyncio import Redis


class RedisConnectionInfoRepository:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def _connection_namespace(self, gathering_id: UUID, persona_id: UUID) -> str:
        return f"chat:gathering:{gathering_id}:persona:{persona_id}:connections"

    async def add_connection_info(
        self,
        gathering_id: UUID,
        persona_id: UUID,
    ) -> None:
        await self.redis_client.incr(
            self._connection_namespace(gathering_id, persona_id)
        )

    async def remove_connection_info(
        self,
        gathering_id: UUID,
        persona_id: UUID,
    ) -> None:
        await self.redis_client.decr(
            self._connection_namespace(gathering_id, persona_id)
        )

    async def retrieve_persona_connection_count(
        self,
        gathering_id: UUID,
        persona_id: UUID,
    ) -> int:
        count = await self.redis_client.get(
            self._connection_namespace(gathering_id, persona_id)
        )
        return int(count) if count else 0

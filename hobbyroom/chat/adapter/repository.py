from uuid import UUID

from redis.asyncio import Redis


class RedisConnectionInfoRepository:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def add_connection_info(
        self,
        connection_id: UUID,
        gathering_id: UUID,
        persona_id: UUID,
    ) -> None:
        namespace = f"chat:gathering:{gathering_id}:persona:{persona_id}:connections"
        await self.redis_client.rpush(namespace, connection_id)

    async def count_persona_connections(
        self,
        gathering_id: UUID,
        persona_id: UUID,
    ) -> int:
        namespace = f"chat:gathering:{gathering_id}:persona:{persona_id}:connections"
        return await self.redis_client.llen(namespace)

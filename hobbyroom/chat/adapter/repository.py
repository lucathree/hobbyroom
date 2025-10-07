from uuid import UUID

from redis.asyncio import Redis


class RedisConnectionInfoRepository:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def add_connection_info(
        self,
        gathering_id: UUID,
        persona_id: UUID,
    ) -> None:
        namespace = f"chat:gathering:{gathering_id}:persona:{persona_id}:connections"
        await self.redis_client.incr(namespace)

    async def retrieve_persona_connection_count(
        self,
        gathering_id: UUID,
        persona_id: UUID,
    ) -> int:
        namespace = f"chat:gathering:{gathering_id}:persona:{persona_id}:connections"
        return int(await self.redis_client.get(namespace)) or 0

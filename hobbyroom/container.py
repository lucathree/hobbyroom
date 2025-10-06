import pendulum
from dependency_injector import containers, providers
from redis.asyncio import ConnectionPool, Redis
from sqlalchemy.orm import sessionmaker
from uuid6 import uuid7

from hobbyroom.auth.dependency import AuthContainer
from hobbyroom.chat.dependency import ChatContainer
from hobbyroom.database.connection import postgres_db
from hobbyroom.gathering.dependency import GatheringContainer
from hobbyroom.settings import settings
from hobbyroom.user.dependency import UserContainer


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            ".depends",
            ".auth.entrypoint",
            ".chat.entrypoint",
            ".gathering.entrypoint",
            ".user.entrypoint",
        ]
    )

    db_engine = providers.Factory(lambda: postgres_db)
    db_session_factory = providers.Factory(
        lambda db_engine: sessionmaker(bind=db_engine), db_engine
    )
    redis_pool = providers.Singleton(
        ConnectionPool.from_url,
        url=settings.redis_url,
        decode_responses=True,
        max_connections=settings.max_redis_connections,
    )
    redis_client = providers.Factory(Redis, connection_pool=redis_pool)

    id_generator = providers.Factory(lambda: uuid7)
    clock = providers.Factory(lambda: (lambda: pendulum.now("UTC")))

    auth = providers.Container(
        AuthContainer,
        session_factory=db_session_factory,
        id_generator=id_generator,
        clock=clock,
    )
    chat = providers.Container(
        ChatContainer,
        clock=clock,
        id_generator=id_generator,
        redis_client=redis_client,
    )
    gathering = providers.Container(
        GatheringContainer,
        session_factory=db_session_factory,
        id_generator=id_generator,
        clock=clock,
    )
    user = providers.Container(
        UserContainer,
        session_factory=db_session_factory,
        id_generator=id_generator,
        clock=clock,
    )

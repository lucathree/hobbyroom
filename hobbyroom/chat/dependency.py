from dependency_injector import containers, providers

from hobbyroom.chat import adapter, connection_manager


class AdapterContainer(containers.DeclarativeContainer):
    redis_client = providers.Dependency()

    redis_connection_repository = providers.Factory(
        adapter.RedisConnectionRepository,
        redis_client=redis_client,
    )


class ServiceContainer(containers.DeclarativeContainer):
    adapter = providers.DependenciesContainer()

    clock = providers.Dependency()
    redis_client = providers.Dependency()

    connection_manager = providers.Singleton(
        connection_manager.ConnectionManager,
        clock=clock,
        connection_repository=adapter.redis_connection_repository,
    )


class ChatContainer(containers.DeclarativeContainer):
    clock = providers.Dependency()
    redis_client = providers.Dependency()

    adapter = providers.Container(
        AdapterContainer,
        redis_client=redis_client,
    )
    service = providers.Container(
        ServiceContainer,
        adapter=adapter,
        clock=clock,
        redis_client=redis_client,
    )

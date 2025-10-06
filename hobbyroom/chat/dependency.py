from dependency_injector import containers, providers

from hobbyroom.chat import adapter, connection_manager


class AdapterContainer(containers.DeclarativeContainer):
    redis_client = providers.Dependency()

    redis_connection_info_repository = providers.Factory(
        adapter.RedisConnectionInfoRepository,
        redis_client=redis_client,
    )


class ServiceContainer(containers.DeclarativeContainer):
    adapter = providers.DependenciesContainer()

    clock = providers.Dependency()
    id_generator = providers.Dependency()
    redis_client = providers.Dependency()

    connection_manager = providers.Singleton(
        connection_manager.ConnectionManager,
        clock=clock,
        id_generator=id_generator,
        connection_info_repository=adapter.redis_connection_info_repository,
    )


class ChatContainer(containers.DeclarativeContainer):
    clock = providers.Dependency()
    id_generator = providers.Dependency()
    redis_client = providers.Dependency()

    adapter = providers.Container(
        AdapterContainer,
        redis_client=redis_client,
    )
    service = providers.Container(
        ServiceContainer,
        adapter=adapter,
        clock=clock,
        id_generator=id_generator,
        redis=redis_client,
    )

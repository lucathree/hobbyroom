from dependency_injector import containers, providers

from hobbyroom.chat import connection_manager


class ServiceContainer(containers.DeclarativeContainer):
    clock = providers.Dependency()

    connection_manager = providers.Singleton(
        connection_manager.ConnectionManager,
        clock=clock,
    )


class ChatContainer(containers.DeclarativeContainer):
    clock = providers.Dependency()

    service = providers.Container(
        ServiceContainer,
        clock=clock,
    )

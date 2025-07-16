from hobbyroom.user import adapter, service
from dependency_injector import containers, providers


class AdapterContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()

    user_repo_factory = providers.Factory(lambda: adapter.UserRepository)
    user_unit_of_work = providers.Factory(
        adapter.UserUnitOfWork,
        session_factory=session_factory,
        user_repo_factory=user_repo_factory,
    )


class ServiceContainer(containers.DeclarativeContainer):
    adapter = providers.DependenciesContainer()
    id_generator = providers.Dependency()
    clock = providers.Dependency()

    create_user_handler = providers.Factory(
        service.CreateUserHandler,
        user_unit_of_work=adapter.user_unit_of_work,
        id_generator=id_generator,
        clock=clock,
    )


class UserContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()
    id_generator = providers.Dependency()
    clock = providers.Dependency()

    adapter = providers.Container(
        AdapterContainer,
        session_factory=session_factory,
    )
    service = providers.Container(
        ServiceContainer,
        adapter=adapter,
        id_generator=id_generator,
        clock=clock,
    )

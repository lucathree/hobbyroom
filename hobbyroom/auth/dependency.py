from dependency_injector import containers, providers

from hobbyroom.auth import adapter, service
from hobbyroom.settings import settings


class AdapterContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()

    user_repo_factory = providers.Factory(lambda: adapter.UserRepository)
    auth_unit_of_work = providers.Factory(
        adapter.AuthUnitOfWork,
        session_factory=session_factory,
        user_repo_factory=user_repo_factory,
    )


class ServiceContainer(containers.DeclarativeContainer):
    adapter = providers.DependenciesContainer()
    id_generator = providers.Dependency()
    clock = providers.Dependency()

    jwt_handler = providers.Factory(
        service.JWTHandler,
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        clock=clock,
    )
    authorize_user_handler = providers.Factory(
        service.AuthorizeUserHandler,
        auth_unit_of_work=adapter.auth_unit_of_work,
        jwt_handler=jwt_handler,
    )


class AuthContainer(containers.DeclarativeContainer):
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

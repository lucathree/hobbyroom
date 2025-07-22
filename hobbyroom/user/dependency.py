from dependency_injector import containers, providers

from hobbyroom.settings import settings
from hobbyroom.user import adapter, service


class AdapterContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()

    user_repo_factory = providers.Factory(lambda: adapter.UserRepository)
    persona_repo_factory = providers.Factory(lambda: adapter.PersonaRepository)
    user_unit_of_work = providers.Factory(
        adapter.UserUnitOfWork,
        session_factory=session_factory,
        user_repo_factory=user_repo_factory,
        persona_repo_factory=persona_repo_factory,
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
    jwt_handler = providers.Factory(
        service.JWTHandler,
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        clock=clock,
    )
    authorize_user_handler = providers.Factory(
        service.AuthorizeUserHandler,
        user_unit_of_work=adapter.user_unit_of_work,
        jwt_handler=jwt_handler,
    )
    create_persona_handler = providers.Factory(
        service.CreatePersonaHandler,
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

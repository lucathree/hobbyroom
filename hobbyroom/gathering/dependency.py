from dependency_injector import containers, providers

from hobbyroom.gathering import adapter, service


class AdapterContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()

    gathering_repo_factory = providers.Factory(lambda: adapter.GatheringRepository)
    affiliation_repo_factory = providers.Factory(lambda: adapter.AffiliationRepository)
    gathering_unit_of_work = providers.Factory(
        adapter.GatheringUnitOfWork,
        session_factory=session_factory,
        gathering_repo_factory=gathering_repo_factory,
        affiliation_repo_factory=affiliation_repo_factory,
    )


class ServiceContainer(containers.DeclarativeContainer):
    adapter = providers.DependenciesContainer()
    id_generator = providers.Dependency()
    clock = providers.Dependency()

    create_gathering_handler = providers.Factory(
        service.CreateGatheringHandler,
        gathering_unit_of_work=adapter.gathering_unit_of_work,
        id_generator=id_generator,
        clock=clock,
    )


class GatheringContainer(containers.DeclarativeContainer):
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

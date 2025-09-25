from dependency_injector import containers, providers

from hobbyroom.gathering import adapter, service


class AdapterContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()

    gathering_repo_factory = providers.Factory(lambda: adapter.GatheringRepository)
    affiliation_repo_factory = providers.Factory(lambda: adapter.AffiliationRepository)
    post_repo_factory = providers.Factory(lambda: adapter.PostRepository)
    gathering_unit_of_work = providers.Factory(
        adapter.GatheringUnitOfWork,
        session_factory=session_factory,
        gathering_repo_factory=gathering_repo_factory,
        affiliation_repo_factory=affiliation_repo_factory,
        post_repo_factory=post_repo_factory,
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
    join_gathering_handler = providers.Factory(
        service.JoinGatheringHandler,
        gathering_unit_of_work=adapter.gathering_unit_of_work,
        id_generator=id_generator,
        clock=clock,
    )
    create_post_handler = providers.Factory(
        service.CreatePostHandler,
        gathering_unit_of_work=adapter.gathering_unit_of_work,
        id_generator=id_generator,
        clock=clock,
    )
    list_posts_handler = providers.Factory(
        service.ListPostsHandler,
        gathering_unit_of_work=adapter.gathering_unit_of_work,
    )
    retrieve_post_handler = providers.Factory(
        service.RetrievePostHandler,
        gathering_unit_of_work=adapter.gathering_unit_of_work,
    )
    update_post_handler = providers.Factory(
        service.UpdatePostHandler,
        gathering_unit_of_work=adapter.gathering_unit_of_work,
        clock=clock,
    )
    delete_post_handler = providers.Factory(
        service.DeletePostHandler,
        gathering_unit_of_work=adapter.gathering_unit_of_work,
    )
    list_gatherings_handler = providers.Factory(
        service.ListGatheringsHandler,
        gathering_unit_of_work=adapter.gathering_unit_of_work,
    )
    list_user_gatherings_handler = providers.Factory(
        service.ListUserGatheringsHandler,
        gathering_unit_of_work=adapter.gathering_unit_of_work,
    )
    retrieve_gathering_handler = providers.Factory(
        service.RetrieveGatheringHandler,
        gathering_unit_of_work=adapter.gathering_unit_of_work,
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

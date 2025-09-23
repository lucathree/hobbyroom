from hobbyroom import exceptions
from hobbyroom.gathering import adapter, domain, query, schema


class ListPostsHandler:
    def __init__(self, gathering_unit_of_work: adapter.GatheringUnitOfWork):
        self.gathering_unit_of_work = gathering_unit_of_work

    def handle(self, query: query.ListPosts) -> schema.ListedPosts:
        with self.gathering_unit_of_work as uow:
            gathering = uow.gathering.find_by_id(query.gathering_id)
            if not gathering:
                raise exceptions.NotFoundError("존재하지 않는 모임입니다.")
            total = uow.post.count_total_per_gathering(query.gathering_id)
            posts = uow.post.list_by_query(query)

        return schema.ListedPosts(total=total, posts=posts)


class RetrievePostHandler:
    def __init__(self, gathering_unit_of_work: adapter.GatheringUnitOfWork):
        self.gathering_unit_of_work = gathering_unit_of_work

    def handle(self, query: query.RetrievePost) -> domain.SearchedPost:
        with self.gathering_unit_of_work as uow:
            post = uow.post.find_by_gathering_and_post_id(
                gathering_id=query.gathering_id, post_id=query.post_id
            )
            if post is None:
                raise exceptions.NotFoundError("존재하지 않는 게시글입니다.")
        return post


class ListGatheringsHandler:
    def __init__(self, gathering_unit_of_work: adapter.GatheringUnitOfWork):
        self.gathering_unit_of_work = gathering_unit_of_work

    def handle(self, query: query.ListGatherings) -> schema.ListedGatherings:
        with self.gathering_unit_of_work as uow:
            total = uow.gathering.count_total()
            gatherings = uow.gathering.list_by_query(query)

        return schema.ListedGatherings(total=total, gatherings=gatherings)

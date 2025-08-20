from uuid import UUID

from sqlalchemy import asc, desc
from sqlalchemy.orm import selectinload

from hobbyroom import database
from hobbyroom.gathering import domain, query


class GatheringRepository(database.SQLAlchemyRepository[domain.Gathering]):
    __model_cls__ = database.Gathering


class AffiliationRepository(database.SQLAlchemyRepository[domain.Affiliation]):
    __model_cls__ = database.Affiliation

    def find_by_persona_and_gathering_ids(
        self, persona_id: UUID, gathering_id: UUID
    ) -> domain.Affiliation | None:
        return self.find_by(persona_id=persona_id, gathering_id=gathering_id)


class PostRepository(database.SQLAlchemyRepository[domain.Post]):
    __model_cls__ = database.Post

    def list_by_query(self, query: query.ListPosts) -> list[domain.SearchedPost]:
        order_by = asc(database.Post.created_at) if query.ascending else desc(database.Post.created_at)
        posts = (
            self.session.query(database.Post)
            .filter_by(gathering_id=query.gathering_id)
            .order_by(order_by)
            .offset(query.offset)
            .limit(query.per_page)
            .options(selectinload(database.Post.persona))
            .all()
        )
        return [
            domain.SearchedPost(
                id=post.id,
                title=post.title,
                content=post.content,
                writer=post.persona.name,
                created_at=post.created_at,
                updated_at=post.updated_at,
            )
            for post in posts
        ]

    def count_total_per_gathering(self, gathering_id: UUID) -> int:
        return self.session.query(database.Post).filter_by(gathering_id=gathering_id).count()

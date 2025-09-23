from uuid import UUID

import pendulum
from sqlalchemy import asc, desc, update
from sqlalchemy.orm import selectinload

from hobbyroom import database
from hobbyroom.gathering import domain, query


class GatheringRepository(database.SQLAlchemyRepository[domain.Gathering]):
    __model_cls__ = database.Gathering

    def list_by_query(self, query: query.ListGatherings) -> list[domain.Gathering]:
        order_by = (
            asc(database.Gathering.created_at)
            if query.ascending
            else desc(database.Gathering.created_at)
        )
        gatherings = (
            self.session.query(database.Gathering)
            .order_by(order_by)
            .offset(query.offset)
            .limit(query.per_page)
            .all()
        )
        return [
            domain.Gathering(
                id=gathering.id,
                name=gathering.name,
                description=gathering.description,
                created_at=gathering.created_at,
                updated_at=gathering.updated_at,
            )
            for gathering in gatherings
        ]

    def count_total(self) -> int:
        return self.session.query(database.Gathering).count()


class AffiliationRepository(database.SQLAlchemyRepository[domain.Affiliation]):
    __model_cls__ = database.Affiliation

    def find_by_persona_and_gathering_ids(
        self, persona_id: UUID, gathering_id: UUID
    ) -> domain.Affiliation | None:
        return self.find_by(persona_id=persona_id, gathering_id=gathering_id)


class PostRepository(database.SQLAlchemyRepository[domain.Post]):
    __model_cls__ = database.Post

    def list_by_query(self, query: query.ListPosts) -> list[domain.SearchedPost]:
        order_by = (
            asc(database.Post.created_at)
            if query.ascending
            else desc(database.Post.created_at)
        )
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
        return (
            self.session.query(database.Post)
            .filter_by(gathering_id=gathering_id)
            .count()
        )

    def find_by_gathering_and_post_id(
        self, gathering_id: UUID, post_id: UUID
    ) -> domain.SearchedPost | None:
        post = (
            self.session.query(database.Post)
            .filter_by(gathering_id=gathering_id, id=post_id)
            .first()
        )
        if post:
            return domain.SearchedPost(
                id=post.id,
                title=post.title,
                content=post.content,
                writer=post.persona.name,
                created_at=post.created_at,
                updated_at=post.updated_at,
            )
        return None

    def update_post(
        self, post_id: UUID, title: str, content: str, updated_at: pendulum.DateTime
    ) -> None:
        stmt = (
            update(database.Post)
            .where(database.Post.id == post_id)
            .values(title=title, content=content, updated_at=updated_at)
            .execution_options(synchronize_session="fetch")
        )
        self.session.execute(stmt)

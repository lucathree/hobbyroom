from uuid import UUID

import pendulum
from sqlalchemy import update

from hobbyroom import database
from hobbyroom.gathering import domain, query


class GatheringRepository(database.SQLAlchemyRepository[domain.Gathering]):
    __model_cls__ = database.Gathering

    def list_by_query(self, query: query.PaginationQuery) -> list[domain.Gathering]:
        gatherings: list[database.Gathering] = (
            self.session.execute(query.statement).scalars().all()
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

    def count_total_by_personas(self, persona_ids: list[UUID]) -> int:
        return (
            self.session.query(database.Gathering)
            .join(
                database.Affiliation,
                database.Gathering.id == database.Affiliation.gathering_id,
            )
            .filter(database.Affiliation.persona_id.in_(persona_ids))
            .count()
        )


class AffiliationRepository(database.SQLAlchemyRepository[domain.Affiliation]):
    __model_cls__ = database.Affiliation

    def find_by_persona_and_gathering_ids(
        self, persona_id: UUID, gathering_id: UUID
    ) -> domain.Affiliation | None:
        return self.find_by(persona_id=persona_id, gathering_id=gathering_id)

    def find_gathering_leader(self, gathering_id: UUID) -> domain.Persona | None:
        result = (
            self.session.query(database.Persona.id, database.Persona.name)
            .join(
                database.Affiliation,
                database.Persona.id == database.Affiliation.persona_id,
            )
            .filter(
                database.Affiliation.gathering_id == gathering_id,
                database.Affiliation.is_leader,
            )
            .first()
        )
        if result:
            return domain.Persona(
                id=result.id,
                name=result.name,
            )
        return None

    def count_gathering_members(self, gathering_id: UUID) -> int:
        return (
            self.session.query(database.Affiliation)
            .filter_by(gathering_id=gathering_id)
            .count()
        )


class PostRepository(database.SQLAlchemyRepository[domain.Post]):
    __model_cls__ = database.Post

    def list_by_query(self, query: query.PaginationQuery) -> list[domain.SearchedPost]:
        posts: list[database.Post] = (
            self.session.execute(query.statement).scalars().all()
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

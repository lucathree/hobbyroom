import abc
from typing import Self
from uuid import UUID

from pydantic import BaseModel, Field
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select

from hobbyroom import auth, database


class PaginationQuery(BaseModel, abc.ABC):
    ascending: bool = False
    page: int = Field(ge=1, default=1)
    per_page: int = Field(le=100, default=10)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page

    @property
    @abc.abstractmethod
    def statement(self) -> Select:
        raise NotImplementedError


class ListGatherings(PaginationQuery):
    @property
    def statement(self) -> Select:
        order_by = (
            asc(database.Gathering.created_at)
            if self.ascending
            else desc(database.Gathering.created_at)
        )
        return (
            select(database.Gathering)
            .order_by(order_by)
            .offset(self.offset)
            .limit(self.per_page)
        )


class ListUserGatherings(PaginationQuery):
    persona_ids: list[UUID]

    @classmethod
    def create(cls, user: auth.User, ascending: bool, page: int, per_page: int) -> Self:
        return cls(
            persona_ids=[persona.id for persona in user.personas],
            ascending=ascending,
            page=page,
            per_page=per_page,
        )

    @property
    def statement(self) -> Select:
        order_by = (
            asc(database.Gathering.created_at)
            if self.ascending
            else desc(database.Gathering.created_at)
        )
        return (
            select(database.Gathering)
            .join(
                database.Affiliation,
                database.Gathering.id == database.Affiliation.gathering_id,
            )
            .where(database.Affiliation.persona_id.in_(self.persona_ids))
            .order_by(order_by)
            .offset(self.offset)
            .limit(self.per_page)
        )


class ListPosts(PaginationQuery):
    gathering_id: UUID

    @property
    def statement(self) -> Select:
        order_by = (
            asc(database.Post.created_at)
            if self.ascending
            else desc(database.Post.created_at)
        )
        return (
            select(database.Post)
            .where(database.Post.gathering_id == self.gathering_id)
            .order_by(order_by)
            .offset(self.offset)
            .limit(self.per_page)
            .options(selectinload(database.Post.persona))
        )


class RetrievePost(BaseModel):
    gathering_id: UUID
    post_id: UUID

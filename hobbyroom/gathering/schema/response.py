import datetime
from uuid import UUID

from pydantic import BaseModel

from hobbyroom.gathering import domain


class ListedGatherings(BaseModel):
    total: int
    gatherings: list[domain.Gathering]


class ListedPosts(BaseModel):
    total: int
    posts: list[domain.SearchedPost]


class RetrievedGathering(BaseModel):
    id: UUID
    name: str
    description: str
    leader: domain.Persona
    member_count: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

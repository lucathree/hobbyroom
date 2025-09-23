from uuid import UUID

from pydantic import BaseModel, Field


class ListGatherings(BaseModel):
    ascending: bool = False
    page: int = Field(ge=1, default=1)
    per_page: int = Field(le=100, default=10)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


class ListPosts(BaseModel):
    gathering_id: UUID
    ascending: bool
    page: int = Field(ge=1)
    per_page: int = Field(le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


class RetrievePost(BaseModel):
    gathering_id: UUID
    post_id: UUID

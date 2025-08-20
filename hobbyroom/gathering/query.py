from uuid import UUID

from pydantic import BaseModel, Field


class ListPosts(BaseModel):
    gathering_id: UUID
    ascending: bool
    page: int = Field(ge=1)
    per_page: int = Field(le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page

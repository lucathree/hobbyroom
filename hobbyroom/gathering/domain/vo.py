import datetime
from uuid import UUID

from pydantic import BaseModel


class SearchedPost(BaseModel):
    id: UUID
    title: str
    content: str
    writer: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class Persona(BaseModel):
    id: UUID
    name: str

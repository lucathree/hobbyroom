from pydantic import BaseModel

from hobbyroom.gathering import domain


class ListedGatherings(BaseModel):
    total: int
    gatherings: list[domain.Gathering]


class ListedPosts(BaseModel):
    total: int
    posts: list[domain.SearchedPost]

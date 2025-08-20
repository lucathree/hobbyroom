from pydantic import BaseModel

from hobbyroom.gathering import domain


class ListedPosts(BaseModel):
    total: int
    posts: list[domain.SearchedPost]

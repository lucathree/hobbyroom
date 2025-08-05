from pydantic import BaseModel


class AuthorizedToken(BaseModel):
    token: str

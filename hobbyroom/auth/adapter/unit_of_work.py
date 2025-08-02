from collections.abc import Callable
from typing import Self

from sqlalchemy.orm import Session, sessionmaker

from hobbyroom import database
from hobbyroom.auth.adapter import repository


class AuthUnitOfWork(database.BaseUnitOfWork):
    def __init__(
        self,
        session_factory: sessionmaker,
        user_repo_factory: Callable[[Session], repository.UserRepository],
    ):
        super().__init__(session_factory)
        self.user_repo_factory = user_repo_factory

    def __enter__(self) -> Self:
        super().__enter__()
        self.user: repository.UserRepository = self.user_repo_factory(self.session)

        return self

from collections.abc import Callable
from typing import Self

from sqlalchemy.orm import Session, sessionmaker

from hobbyroom import database
from hobbyroom.gathering.adapter import repository


class GatheringUnitOfWork(database.BaseUnitOfWork):
    def __init__(
        self,
        session_factory: sessionmaker,
        gathering_repo_factory: Callable[[Session], repository.GatheringRepository],
        affiliation_repo_factory: Callable[[Session], repository.AffiliationRepository],
    ):
        super().__init__(session_factory)
        self.gathering_repo_factory = gathering_repo_factory
        self.affiliation_repo_factory = affiliation_repo_factory

    def __enter__(self) -> Self:
        super().__enter__()
        self.gathering = self.gathering_repo_factory(self.session)
        self.affiliation = self.affiliation_repo_factory(self.session)

        return self

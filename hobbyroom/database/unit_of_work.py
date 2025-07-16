from types import TracebackType
from typing import Self
from sqlalchemy.orm import Session, sessionmaker


class BaseUnitOfWork:
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    def __enter__(self) -> Self:
        self.session: Session = self.session_factory()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.session.rollback()
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

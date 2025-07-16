from typing import Any, Self
import pendulum
from uuid6 import uuid7
from sqlalchemy import Column, UUID, VARCHAR, TEXT, BOOLEAN, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7)

    @classmethod
    def parse_obj(cls, obj: Any) -> Self:
        if not isinstance(obj, dict):
            try:
                obj = dict(obj)
            except (TypeError, ValueError):
                raise TypeError(
                    f"{cls.__name__} expected dict not {obj.__class__.__name__}"
                )
        return cls(**obj)

    def to_dict(self) -> dict[str, Any]:
        result = dict(self.__dict__)
        result.pop("_sa_instance_state")
        return result


class User(Base):
    __tablename__ = "user"

    email = Column(VARCHAR(320), unique=True, nullable=False)
    password = Column(TEXT, nullable=False)
    is_deactivated = Column(BOOLEAN, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: pendulum.now("UTC"))
    updated_at = Column(DateTime(timezone=True), default=created_at)

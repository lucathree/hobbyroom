import datetime
from typing import Any, Self

import pendulum
from sqlalchemy import TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from uuid6 import uuid7


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)

    type_annotation_map = {
        UUID: UUID(as_uuid=True),
        datetime.datetime: TIMESTAMP(timezone=True),
    }

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

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_deactivated: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=lambda: pendulum.now("UTC")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(default=created_at)

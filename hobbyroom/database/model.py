import datetime
from typing import Any, Self

import pendulum
from sqlalchemy import TIMESTAMP, UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from uuid6 import uuid7


class Base(DeclarativeBase):
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


class IdentifierBase(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)


class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=lambda: pendulum.now("UTC")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(default=created_at)


class User(IdentifierBase, TimestampMixin):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_deactivated: Mapped[bool] = mapped_column(default=False)

    personas: Mapped[list["Persona"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )


class Persona(IdentifierBase, TimestampMixin):
    __tablename__ = "persona"

    name: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship("User", back_populates="personas")
    affiliations: Mapped[list["Affiliation"]] = relationship(
        back_populates="persona", cascade="all, delete-orphan"
    )


class Gathering(IdentifierBase, TimestampMixin):
    __tablename__ = "gathering"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]

    affiliations: Mapped[list["Affiliation"]] = relationship(
        back_populates="gathering", cascade="all, delete-orphan"
    )


class Affiliation(Base):
    __tablename__ = "affiliation"

    persona_id: Mapped[UUID] = mapped_column(ForeignKey("persona.id"), primary_key=True)
    gathering_id: Mapped[UUID] = mapped_column(
        ForeignKey("gathering.id"), primary_key=True
    )
    is_leader: Mapped[bool] = mapped_column(default=False)
    joined_at: Mapped[datetime.datetime] = mapped_column(
        default=lambda: pendulum.now("UTC")
    )

    persona: Mapped["Persona"] = relationship(back_populates="affiliations")
    gathering: Mapped["Gathering"] = relationship(back_populates="affiliations")

    __table_args__ = (
        UniqueConstraint("persona_id", "gathering_id", name="uq_persona_gathering"),
    )

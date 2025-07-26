from typing import ClassVar, Generic, TypeVar, get_args
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.orm import Session

from hobbyroom.database import model

EntityType = TypeVar("EntityType", bound=BaseModel)


class SQLAlchemyRepository(Generic[EntityType]):
    __model_cls__: ClassVar[type[model.Base]] = None

    def __init__(self, session: Session):
        self.session = session

    def __init_subclass__(cls, **kwargs):
        if cls.__model_cls__ is None:
            raise ValueError("`__model_cls__` must be defined.")

    def add(self, entity: EntityType) -> None:
        model_obj = self.__model_cls__.parse_obj(entity)
        self.session.add(model_obj)

    def find_by(self, **kwargs) -> EntityType | None:
        entity_type: EntityType = get_args(self.__class__.__orig_bases__[0])[0]
        obj = self.session.query(self.__model_cls__).filter_by(**kwargs).first()
        return obj and entity_type.model_validate(obj.to_dict())

    def find_by_id(self, id: UUID) -> EntityType | None:
        return self.find_by(id=id)

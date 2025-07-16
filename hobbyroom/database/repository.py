from typing import ClassVar, Generic, TypeVar
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

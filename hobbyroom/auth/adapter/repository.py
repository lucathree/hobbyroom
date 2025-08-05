from uuid import UUID

from hobbyroom import database
from hobbyroom.auth import domain


class UserRepository(database.SQLAlchemyRepository[domain.User]):
    __model_cls__ = database.User

    def find_by(self, **kwargs) -> domain.User | None:
        obj = self.session.query(self.__model_cls__).filter_by(**kwargs).first()
        return obj and domain.User.from_orm(obj)

    def find_by_email(self, email: str) -> domain.User | None:
        return self.find_by(email=email)


class AffiliationRepository(database.SQLAlchemyRepository[domain.Affiliation]):
    __model_cls__ = database.Affiliation

    def list_by_persona_id(self, persona_id: UUID) -> list[domain.Affiliation]:
        return self.list_by(persona_id=persona_id)

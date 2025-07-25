from hobbyroom import database
from hobbyroom.user import domain


class UserRepository(database.SQLAlchemyRepository[domain.User]):
    __model_cls__ = database.User

    def find_by_email(self, email: str) -> domain.User | None:
        return self.find_by(email=email)


class PersonaRepository(database.SQLAlchemyRepository[domain.Persona]):
    __model_cls__ = database.Persona

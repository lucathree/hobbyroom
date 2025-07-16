from hobbyroom import database
from hobbyroom.user import domain


class UserRepository(database.SQLAlchemyRepository[domain.User]):
    __model_cls__ = database.User

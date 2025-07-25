from hobbyroom import database
from hobbyroom.gathering import domain


class GatheringRepository(database.SQLAlchemyRepository[domain.Gathering]):
    __model_cls__ = database.Gathering


class AffiliationRepository(database.SQLAlchemyRepository[domain.Affiliation]):
    __model_cls__ = database.Affiliation


class PersonaRepository(database.SQLAlchemyRepository[domain.Persona]):
    __model_cls__ = database.Persona

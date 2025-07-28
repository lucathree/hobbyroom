from uuid import UUID

from hobbyroom import database
from hobbyroom.gathering import domain


class GatheringRepository(database.SQLAlchemyRepository[domain.Gathering]):
    __model_cls__ = database.Gathering


class AffiliationRepository(database.SQLAlchemyRepository[domain.Affiliation]):
    __model_cls__ = database.Affiliation

    def find_by_persona_and_gathering_ids(
        self, persona_id: UUID, gathering_id: UUID
    ) -> domain.Affiliation | None:
        return self.find_by(persona_id=persona_id, gathering_id=gathering_id)

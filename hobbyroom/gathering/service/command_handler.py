from collections.abc import Callable
from uuid import UUID

import pendulum

from hobbyroom.gathering import adapter, command, domain


class CreateGatheringHandler:
    def __init__(
        self,
        gathering_unit_of_work: adapter.GatheringUnitOfWork,
        id_generator: Callable[..., UUID],
        clock: Callable[..., pendulum.DateTime],
    ):
        self.gathering_unit_of_work = gathering_unit_of_work
        self.id_generator = id_generator
        self.clock = clock

    def handle(self, cmd: command.CreateGathering) -> None:
        gathering_id = self.id_generator()
        creation_time = self.clock()
        with self.gathering_unit_of_work as uow:
            gathering = domain.Gathering.create(
                id=gathering_id,
                name=cmd.name,
                created_at=creation_time,
                description=cmd.description,
            )
            affiliation = domain.Affiliation.create_leader(
                persona_id=cmd.persona_id,
                gathering_id=gathering_id,
                joined_at=creation_time,
            )
            uow.gathering.add(gathering)
            uow.affiliation.add(affiliation)
            uow.commit()

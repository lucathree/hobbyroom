from collections.abc import Callable
from uuid import UUID

import pendulum

from hobbyroom import exceptions
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
                description=cmd.description,
                created_at=creation_time,
            )
            affiliation = domain.Affiliation.create_leader(
                persona_id=cmd.persona_id,
                gathering_id=gathering_id,
                joined_at=creation_time,
            )
            uow.gathering.add(gathering)
            uow.affiliation.add(affiliation)
            uow.commit()


class JoinGatheringHandler:
    def __init__(
        self,
        gathering_unit_of_work: adapter.GatheringUnitOfWork,
        id_generator: Callable[..., UUID],
        clock: Callable[..., pendulum.DateTime],
    ):
        self.gathering_unit_of_work = gathering_unit_of_work
        self.id_generator = id_generator
        self.clock = clock

    def handle(self, cmd: command.JoinGathering) -> None:
        with self.gathering_unit_of_work as uow:
            affiliation = uow.affiliation.find_by_persona_and_gathering_ids(
                persona_id=cmd.persona_id, gathering_id=cmd.gathering_id
            )
            if affiliation is not None:
                raise exceptions.DuplicateEntityError(
                    "이미 해당 모임에 참여하고 있습니다."
                )
            entity = domain.Affiliation.create_member(
                persona_id=cmd.persona_id,
                gathering_id=cmd.gathering_id,
                joined_at=self.clock(),
            )
            uow.affiliation.add(entity)
            uow.commit()

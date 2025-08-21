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


class CreatePostHandler:
    def __init__(
        self,
        gathering_unit_of_work: adapter.GatheringUnitOfWork,
        id_generator: Callable[..., UUID],
        clock: Callable[..., pendulum.DateTime],
    ):
        self.gathering_unit_of_work = gathering_unit_of_work
        self.id_generator = id_generator
        self.clock = clock

    def handle(self, cmd: command.CreatePost) -> None:
        post_id = self.id_generator()
        creation_time = self.clock()
        with self.gathering_unit_of_work as uow:
            post = domain.Post.create(
                id=post_id,
                title=cmd.title,
                content=cmd.content,
                gathering_id=cmd.gathering_id,
                persona_id=cmd.persona_id,
                created_at=creation_time,
            )
            uow.post.add(post)
            uow.commit()


class UpdatePostHandler:
    def __init__(
        self,
        gathering_unit_of_work: adapter.GatheringUnitOfWork,
        clock: Callable[..., pendulum.DateTime],
    ):
        self.gathering_unit_of_work = gathering_unit_of_work
        self.clock = clock

    def handle(self, cmd: command.UpdatePost) -> None:
        if not cmd.has_entity_ids:
            raise exceptions.DomainValidationError(
                "게시글 수정을 위한 정보가 입력되지 않았습니다."
            )
        with self.gathering_unit_of_work as uow:
            post = uow.post.find_by_id(cmd.post_id)
            if post is None or post.gathering_id != cmd.gathering_id:
                raise exceptions.NotFoundError("게시글을 찾을 수 없습니다.")
            uow.post.update_post(
                post_id=post.id,
                title=cmd.title or post.title,
                content=cmd.content or post.content,
                updated_at=self.clock(),
            )
            uow.commit()

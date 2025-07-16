from collections.abc import Callable
from uuid import UUID

import pendulum
from hobbyroom.user import command, adapter, domain


class CreateUserHandler:
    def __init__(
        self,
        user_unit_of_work: adapter.UserUnitOfWork,
        id_generator: Callable[..., UUID],
        clock: Callable[..., pendulum.DateTime],
    ):
        self.user_unit_of_work = user_unit_of_work
        self.id_generator = id_generator
        self.clock = clock

    def handle(self, cmd: command.CreateUser) -> None:
        user = domain.User.create(
            id=self.id_generator(),
            email=cmd.email,
            hashed_password=cmd.hashed_password,
            created_at=self.clock(),
        )
        with self.user_unit_of_work as uow:
            uow.user.add(user)
            uow.commit()

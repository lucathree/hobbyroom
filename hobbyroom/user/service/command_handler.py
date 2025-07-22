from collections.abc import Callable
from uuid import UUID

import bcrypt
import pendulum

from hobbyroom import exceptions
from hobbyroom.user import adapter, command, domain, schema
from hobbyroom.user.service import jwt_handler


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


class AuthorizeUserHandler:
    def __init__(
        self,
        user_unit_of_work: adapter.UserUnitOfWork,
        jwt_handler: jwt_handler.JWTHandler,
    ):
        self.user_unit_of_work = user_unit_of_work
        self.jwt_handler = jwt_handler

    def handle(self, cmd: command.AuthorizeUser) -> schema.UserToken:
        with self.user_unit_of_work as uow:
            user = uow.user.find_by_email(cmd.email)
        if not user:
            raise exceptions.NotFoundError("User not found")
        self._validate_password(password=cmd.password, hashed_password=user.password)
        token = self.jwt_handler.issue(user_email=user.email)
        return schema.UserToken(token=token)

    def _validate_password(self, password: str, hashed_password: str) -> None:
        is_valid = bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password.encode(),
        )
        if not is_valid:
            raise exceptions.UnauthorizedError("Invalid password")


class CreatePersonaHandler:
    def __init__(
        self,
        user_unit_of_work: adapter.UserUnitOfWork,
        id_generator: Callable[..., UUID],
        clock: Callable[..., pendulum.DateTime],
    ):
        self.user_unit_of_work = user_unit_of_work
        self.id_generator = id_generator
        self.clock = clock

    def handle(self, cmd: command.CreatePersona) -> None:
        persona = domain.Persona.create(
            id=self.id_generator(),
            name=cmd.name,
            user_id=cmd.user_id,
            created_at=self.clock(),
        )
        with self.user_unit_of_work as uow:
            uow.persona.add(persona)
            uow.commit()

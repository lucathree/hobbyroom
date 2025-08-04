import bcrypt

from hobbyroom import exceptions
from hobbyroom.auth import adapter, command, schema
from hobbyroom.auth.service import jwt_handler


class AuthorizeUserHandler:
    def __init__(
        self,
        auth_unit_of_work: adapter.AuthUnitOfWork,
        jwt_handler: jwt_handler.JWTHandler,
    ):
        self.auth_unit_of_work = auth_unit_of_work
        self.jwt_handler = jwt_handler

    def handle(self, cmd: command.AuthorizeUser) -> schema.UserToken:
        with self.auth_unit_of_work as uow:
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

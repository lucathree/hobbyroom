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

    def handle(self, cmd: command.AuthorizeUser) -> schema.AuthorizedToken:
        with self.auth_unit_of_work as uow:
            user = uow.user.find_by_email(cmd.email)
        if not user:
            raise exceptions.NotFoundError("User not found")
        self._validate_password(password=cmd.password, hashed_password=user.password)
        token = self.jwt_handler.issue(user_email=user.email)
        return schema.AuthorizedToken(token=token)

    def _validate_password(self, password: str, hashed_password: str) -> None:
        is_valid = bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password.encode(),
        )
        if not is_valid:
            raise exceptions.UnauthorizedError("Invalid password")


class AuthorizePersonaHandler:
    def __init__(
        self,
        auth_unit_of_work: adapter.AuthUnitOfWork,
        jwt_handler: jwt_handler.JWTHandler,
    ):
        self.auth_unit_of_work = auth_unit_of_work
        self.jwt_handler = jwt_handler

    def handle(self, cmd: command.AuthorizePersona) -> schema.AuthorizedToken:
        payload = self.jwt_handler.decode(cmd.user_jwt)

        with self.auth_unit_of_work as uow:
            user = uow.user.find_by_email(payload.sub)
            if not user:
                raise exceptions.UnauthorizedError("인증 정보가 유효하지 않습니다.")

            persona = next(
                (persona for persona in user.personas if persona.id == cmd.persona_id),
                None,
            )
            if persona is None:
                raise exceptions.NotFoundError(
                    "유효한 페르소나 정보가 사용자에게 없습니다."
                )

            affiliations = uow.affiliation.list_by_persona_id(cmd.persona_id)
            if not affiliations:
                raise exceptions.NotFoundError("페르소나에 대한 소속 정보가 없습니다.")

            token = self.jwt_handler.update_persona_info(
                payload=payload, persona_id=persona.id, affiliations=affiliations
            )
            return schema.AuthorizedToken(token=token)

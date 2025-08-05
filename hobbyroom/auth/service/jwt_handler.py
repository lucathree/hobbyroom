from collections.abc import Callable
from uuid import UUID

import jwt
import pendulum

from hobbyroom import exceptions
from hobbyroom.auth import domain


class JWTHandler:
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        clock: Callable[..., pendulum.DateTime],
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.clock = clock

    def issue(self, user_email: str) -> str:
        payload = domain.JWTPayload.create(
            user_email=user_email,
            clock=self.clock,
        )
        return jwt.encode(
            payload=payload.model_dump(),
            key=self.secret_key,
            algorithm=self.algorithm,
        )

    def decode(self, token: str) -> domain.JWTPayload:
        try:
            decoded = jwt.decode(
                jwt=token.encode(), key=self.secret_key, algorithms=[self.algorithm]
            )
        except jwt.exceptions.InvalidTokenError:
            raise exceptions.UnauthorizedError(
                "인증 토큰이 만료되었거나 올바르지 않습니다."
            )

        payload = domain.JWTPayload.model_validate(decoded)
        if payload.is_expired(current_time=self.clock()):
            raise exceptions.UnauthorizedError("인증 토큰이 만료되었습니다.")

        return payload

    def update_persona_info(
        self,
        payload: domain.JWTPayload,
        persona_id: UUID,
        affiliations: list[domain.Affiliation],
    ) -> str:
        updated_payload = payload.update_persona_info(
            persona_id=str(persona_id),
            affiliated_gathering_ids=[
                str(affiliation.gathering_id) for affiliation in affiliations
            ],
            clock=self.clock,
        )
        return jwt.encode(
            payload=updated_payload.model_dump(),
            key=self.secret_key,
            algorithm=self.algorithm,
        )

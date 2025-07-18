from collections.abc import Callable

import jwt
import pendulum

from hobbyroom.user import domain


class JWTIssuer:
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        clock: Callable[..., pendulum.DateTime],
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.clock = clock

    def create_token(self, user_email: str) -> str:
        payload = domain.JWTPayload.create(
            user_email=user_email,
            clock=self.clock,
        )
        return jwt.encode(
            payload=payload.model_dump(),
            key=self.secret_key,
            algorithm=self.algorithm,
        )

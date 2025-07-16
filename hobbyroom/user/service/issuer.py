from collections.abc import Callable

import jwt
import pendulum


class JWTIssuer:
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        clock: Callable[..., pendulum.DateTime],
        expiration_timedelta: pendulum.Duration,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.clock = clock
        self.expiration_timedelta = expiration_timedelta

    def create_token(self, user_email: str) -> str:
        current_time = self.clock()
        payload = {
            "sub": user_email,
            "iat": int(current_time.timestamp()),
            "exp": int((current_time + self.expiration_timedelta).timestamp()),
        }
        return jwt.encode(
            payload=payload,
            key=self.secret_key,
            algorithm=self.algorithm,
        )

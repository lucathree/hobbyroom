from collections.abc import Callable
from typing import Self

import pendulum
from pydantic import BaseModel

from hobbyroom.settings import settings


class JWTPayload(BaseModel):
    sub: str
    iat: int
    exp: int

    @classmethod
    def create(cls, user_email: str, clock: Callable[..., pendulum.DateTime]) -> Self:
        current_time = clock()
        expiration_time = current_time + settings.jwt_expiration_timedelta

        return cls(
            sub=user_email,
            iat=int(current_time.timestamp()),
            exp=int(expiration_time.timestamp()),
        )

    def is_expired(self, current_time: pendulum.DateTime) -> bool:
        return self.exp < current_time.timestamp()

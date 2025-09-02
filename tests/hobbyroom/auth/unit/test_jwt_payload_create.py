from collections.abc import Callable
from unittest import mock

import pendulum
import pytest

from hobbyroom.auth.domain import JWTPayload


@pytest.fixture
def fixed_clock() -> Callable[..., pendulum.DateTime]:
    def _clock() -> pendulum.DateTime:
        return pendulum.datetime(2025, 8, 30, 12, 0, 0)

    return _clock


@pytest.fixture
def expected(base_jwt_payload: JWTPayload) -> JWTPayload:
    return base_jwt_payload.model_copy(
        update=dict(
            sub="test_user@example.com",
            iat=1756555200,
            exp=1756557000,
            persona=None,
            affiliated_gatherings=None,
        )
    )


@mock.patch("hobbyroom.settings.settings.jwt_expiration_minutes", 30)
def test_create(
    fixed_clock: Callable[..., pendulum.DateTime],
    expected: JWTPayload,
):
    result = JWTPayload.create(user_email="test_user@example.com", clock=fixed_clock)

    assert result == expected

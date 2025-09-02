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
def jwt_payload(base_jwt_payload: JWTPayload) -> JWTPayload:
    return base_jwt_payload.model_copy(
        update=dict(
            sub="test_user@example.com",
            iat=1756355200,
            exp=1756357200,
            persona=None,
            affiliated_gatherings=None,
        )
    )


@pytest.fixture
def expected(base_jwt_payload: JWTPayload) -> JWTPayload:
    return base_jwt_payload.model_copy(
        update=dict(
            sub="test_user@example.com",
            iat=1756555200,
            exp=1756557000,
            persona="test_persona_id",
            affiliated_gatherings=["test_gathering_id1", "test_gathering_id2"],
        )
    )


@mock.patch("hobbyroom.settings.settings.jwt_expiration_minutes", 30)
def test_update_persona_info(
    jwt_payload: JWTPayload,
    fixed_clock: Callable[..., pendulum.DateTime],
    expected: JWTPayload,
):
    persona_id = "test_persona_id"
    affiliated_gathering_ids = ["test_gathering_id1", "test_gathering_id2"]

    result = jwt_payload.update_persona_info(
        persona_id=persona_id,
        affiliated_gathering_ids=affiliated_gathering_ids,
        clock=fixed_clock,
    )
    assert result == expected

import pendulum
import pytest

from hobbyroom.auth.domain import JWTPayload


@pytest.fixture
def jwt_payload(
    base_jwt_payload: JWTPayload,
    request: pytest.FixtureRequest,
) -> JWTPayload:
    return base_jwt_payload.model_copy(
        update=dict(exp=pendulum.datetime(2025, 8, 30, 12, 0, 0).timestamp())
    )


@pytest.mark.parametrize(
    "current_time, expected",
    [
        (pendulum.datetime(2025, 8, 29, 12, 0, 0), False),
        (pendulum.datetime(2025, 8, 30, 11, 59, 59), False),
        (pendulum.datetime(2025, 8, 30, 12, 0, 0), True),
        (pendulum.datetime(2025, 8, 30, 13, 0, 0), True),
    ],
)
def test_is_expired(
    jwt_payload: JWTPayload,
    current_time: pendulum.DateTime,
    expected: bool,
):
    assert jwt_payload.is_expired(current_time) == expected

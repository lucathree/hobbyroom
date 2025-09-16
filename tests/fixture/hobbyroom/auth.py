import pytest

from hobbyroom.auth.domain import JWTPayload


@pytest.fixture
def base_jwt_payload() -> JWTPayload:
    return JWTPayload(
        sub="user@example.com",
        iat=123456789,
        exp=987654321,
        persona=None,
        affiliated_gatherings=None,
    )

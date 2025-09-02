from uuid import UUID

import pytest

from hobbyroom.auth.domain import JWTPayload


@pytest.fixture
def jwt_payload(
    base_jwt_payload: JWTPayload,
    request: pytest.FixtureRequest,
) -> JWTPayload:
    return base_jwt_payload.model_copy(update=dict(persona=request.param))


@pytest.mark.parametrize(
    "jwt_payload, expected",
    [
        (None, None),
        (
            "019905aa-2414-73ff-9075-48bc89130e68",
            UUID("019905aa-2414-73ff-9075-48bc89130e68"),
        ),
    ],
    indirect=["jwt_payload"],
)
def test_persona_id(
    jwt_payload: JWTPayload,
    expected: UUID | None,
):
    assert jwt_payload.persona_id == expected

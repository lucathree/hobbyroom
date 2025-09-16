import uuid

import pendulum
import pytest

from hobbyroom.user import Persona, User


@pytest.fixture
def base_user() -> User:
    return User(
        id=uuid.UUID("019905aa-2414-73ff-9075-48bc89130e67"),
        email="test@example.com",
        password="hashed_password",
        created_at=pendulum.DateTime(2025, 8, 30, 12, 0, 0),
        updated_at=pendulum.DateTime(2025, 8, 30, 12, 0, 0),
    )


@pytest.fixture
def base_persona() -> Persona:
    return Persona(
        id=uuid.UUID("019905aa-2414-73ff-9075-48bc89130e68"),
        name="Test",
        user_id=uuid.UUID("019905aa-2414-73ff-9075-48bc89130e67"),
        created_at=pendulum.DateTime(2025, 8, 1, 13, 0, 0),
        updated_at=pendulum.DateTime(2025, 8, 1, 13, 0, 0),
    )

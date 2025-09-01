import uuid

import pendulum
import pytest

from hobbyroom import database
from hobbyroom.user import Persona, User


@pytest.fixture
def persona_orm_obj() -> database.Persona:
    return database.Persona(
        id=uuid.UUID("019905aa-2414-73ff-9075-48bc89130e68"),
        name="Test Persona",
        user_id=uuid.UUID("019905aa-2414-73ff-9075-48bc89130e67"),
        created_at=pendulum.datetime(2025, 8, 1, 13, 0, 0),
        updated_at=pendulum.datetime(2025, 8, 1, 13, 0, 0),
    )


@pytest.fixture
def user_orm_obj(persona_orm_obj: database.Persona) -> database.User:
    return database.User(
        id=uuid.UUID("019905aa-2414-73ff-9075-48bc89130e67"),
        email="user@example.com",
        password="test_hashed_password",
        is_deactivated=False,
        personas=[persona_orm_obj],
        created_at=pendulum.datetime(2025, 8, 30, 16, 0, 0),
        updated_at=pendulum.datetime(2025, 8, 30, 16, 0, 0),
    )


@pytest.fixture
def persona(base_persona: Persona) -> Persona:
    return base_persona.model_copy(
        update={
            "id": uuid.UUID("019905aa-2414-73ff-9075-48bc89130e68"),
            "name": "Test Persona",
            "user_id": uuid.UUID("019905aa-2414-73ff-9075-48bc89130e67"),
            "created_at": pendulum.datetime(2025, 8, 1, 13, 0, 0),
            "updated_at": pendulum.datetime(2025, 8, 1, 13, 0, 0),
        }
    )


@pytest.fixture
def expected(base_user: User, persona: Persona) -> User:
    return base_user.model_copy(
        update={
            "id": uuid.UUID("019905aa-2414-73ff-9075-48bc89130e67"),
            "email": "user@example.com",
            "password": "test_hashed_password",
            "personas": [persona],
            "created_at": pendulum.datetime(2025, 8, 30, 16, 0, 0),
            "updated_at": pendulum.datetime(2025, 8, 30, 16, 0, 0),
        }
    )


def test_from_orm(user_orm_obj: database.User, expected: User):
    user = User.from_orm(user_orm_obj)

    assert user == expected

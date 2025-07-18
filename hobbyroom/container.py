import pendulum
from dependency_injector import containers, providers
from sqlalchemy.orm import sessionmaker
from uuid6 import uuid7

from hobbyroom.database.connection import postgres_db
from hobbyroom.user.dependency import UserContainer


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            ".auth",
            ".user.entrypoint",
        ]
    )

    db_engine = providers.Factory(lambda: postgres_db)
    db_session_factory = providers.Factory(
        lambda db_engine: sessionmaker(bind=db_engine), db_engine
    )

    id_generator = providers.Factory(lambda: uuid7)
    clock = providers.Factory(lambda: (lambda: pendulum.now("UTC")))

    user = providers.Container(
        UserContainer,
        session_factory=db_session_factory,
        id_generator=id_generator,
        clock=clock,
    )

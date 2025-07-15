import http
from fastapi import FastAPI, Response
from hobbyroom.database import model
from hobbyroom.database.connection import postgres_db


def create_app() -> FastAPI:
    _app = FastAPI(
        title="Hobbyroom API",
        description="취미모임 프로젝트 API 서버",
    )

    model.Base.metadata.create_all(bind=postgres_db)

    _app.get("/health-check", include_in_schema=False)(
        lambda: Response(status_code=http.HTTPStatus.OK)
    )

    return _app


app = create_app()

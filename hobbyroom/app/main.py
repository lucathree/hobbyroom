import http

from fastapi import FastAPI, Response
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse

from hobbyroom.container import Container
from hobbyroom.database import model
from hobbyroom.database.connection import postgres_db
from hobbyroom.user.entrypoint import router as user_router


def create_app() -> FastAPI:
    _app = FastAPI(
        title="Hobbyroom API",
        description="취미모임 프로젝트 API 서버",
        version="0.1.0",
    )
    inject_dependencies(_app)
    add_routers(_app)
    add_docs_routes(_app)

    model.Base.metadata.create_all(bind=postgres_db)

    _app.get("/health-check", include_in_schema=False)(
        lambda: Response(status_code=http.HTTPStatus.OK)
    )

    return _app


def inject_dependencies(_app: FastAPI) -> None:
    container = Container()
    _app.container = container


def add_routers(_app: FastAPI) -> None:
    _app.include_router(user_router)


def add_docs_routes(_app: FastAPI) -> None:
    @_app.get(
        "/docs",
        response_class=HTMLResponse,
        include_in_schema=False,
    )
    async def get_swagger_documentation():
        return get_swagger_ui_html(
            openapi_url="/openapi.json", title=f"{_app.title} - Swagger"
        )

    @_app.get(
        "/redoc",
        include_in_schema=False,
        response_class=HTMLResponse,
    )
    async def get_redoc_documentation():
        return get_redoc_html(
            openapi_url="/openapi.json", title=f"{_app.title} - Redoc"
        )

    @_app.get(
        "/openapi.json",
        include_in_schema=False,
    )
    async def openapi():
        return get_openapi(title=_app.title, version=_app.version, routes=_app.routes)


app = create_app()

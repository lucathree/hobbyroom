import http
from collections.abc import Awaitable, Callable
from typing import ClassVar

from fastapi import Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

type ExceptionHandler[E: Exception] = Callable[
    [Request, E], Response | Awaitable[Response]
]


class ErrorSchema(BaseModel):
    type: str
    message: str
    detail: str | None = None


class ApplicationError(Exception):
    """Base class for application exceptions."""

    default_message: ClassVar[str] = "An error occurred in the application."
    status_code: ClassVar[int] = http.HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(
        self,
        message: str | None = None,
        detail: str | None = None,
    ):
        self.message = message or self.default_message
        self.detail = detail

    def __str__(self):
        return self.message

    @property
    def error_schema(self) -> ErrorSchema:
        return ErrorSchema(
            type=self.__class__.__name__,
            message=self.message,
            detail=self.detail,
        )

    @classmethod
    def create_exception_handler(cls) -> ExceptionHandler:
        async def exception_handler(
            request: Request, exc: ApplicationError
        ) -> JSONResponse:
            return JSONResponse(
                status_code=cls.status_code, content=jsonable_encoder(exc.error_schema)
            )

        return exception_handler


class NotFoundError(ApplicationError):
    default_message: ClassVar[str] = "Resource not found."
    status_code: ClassVar[int] = http.HTTPStatus.NOT_FOUND


class DomainValidationError(ApplicationError):
    default_message: ClassVar[str] = "Domain validation failed."
    status_code: ClassVar[int] = http.HTTPStatus.UNPROCESSABLE_ENTITY


class UnauthorizedError(ApplicationError):
    default_message: ClassVar[str] = "Unauthorized access."
    status_code: ClassVar[int] = http.HTTPStatus.UNAUTHORIZED


class NotAllowedError(ApplicationError):
    default_message: ClassVar[str] = "Operation not allowed."
    status_code: ClassVar[int] = http.HTTPStatus.FORBIDDEN


APPLICATION_EXCEPTIONS: list[type[ApplicationError]] = [
    NotFoundError,
    DomainValidationError,
    UnauthorizedError,
    NotAllowedError,
]


def get_responses(*http_statuses: http.HTTPStatus) -> dict[int, dict[str, str]]:
    """Utility function to create response schemas for FastAPI endpoints."""
    return {
        status.value: {
            "model": ErrorSchema,
            "description": status.phrase,
        }
        for status in http_statuses
    }

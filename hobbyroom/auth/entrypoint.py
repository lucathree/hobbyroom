import http

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from hobbyroom import constants, exceptions
from hobbyroom.auth import command, schema, service
from hobbyroom.container import Container

router = APIRouter()


@router.post(
    "/v1/auth/user",
    response_model=schema.UserToken,
    status_code=http.HTTPStatus.OK,
    tags=[constants.OpenApiTag.AUTH],
    summary="사용자 계정 인증",
    description="사용자 계정 정보를 확인하고 인증 정보를 반환합니다.",
    responses=exceptions.get_responses(
        http.HTTPStatus.UNPROCESSABLE_ENTITY,
        http.HTTPStatus.UNAUTHORIZED,
    ),
)
@inject
async def authorize_user(
    cmd: command.AuthorizeUser,
    handler: service.AuthorizeUserHandler = Depends(
        Provide[Container.auth.service.authorize_user_handler]
    ),
):
    return handler.handle(cmd)

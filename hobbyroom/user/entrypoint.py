import http

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from hobbyroom import constants, exceptions
from hobbyroom.container import Container
from hobbyroom.user import command, schema, service

router = APIRouter()


@router.post(
    "/v1/users",
    status_code=http.HTTPStatus.CREATED,
    tags=[constants.OpenApiTag.USER],
    summary="사용자 계정 생성",
    responses=exceptions.get_responses(http.HTTPStatus.UNPROCESSABLE_ENTITY),
)
@inject
async def create_user(
    cmd: command.CreateUser,
    handler: service.CreateUserHandler = Depends(
        Provide[Container.user.service.create_user_handler]
    ),
):
    handler.handle(cmd)
    return Response(status_code=http.HTTPStatus.CREATED)


@router.post(
    "/v1/users/auth",
    response_model=schema.UserToken,
    status_code=http.HTTPStatus.OK,
    tags=[constants.OpenApiTag.USER],
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
        Provide[Container.user.service.authorize_user_handler]
    ),
):
    return handler.handle(cmd)

import http

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from hobbyroom import constants
from hobbyroom.container import Container
from hobbyroom.user import command, service

router = APIRouter()


@router.post(
    "/v1/users",
    status_code=http.HTTPStatus.CREATED,
    tags=[constants.OpenApiTag.USER],
    summary="사용자 계정 생성",
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

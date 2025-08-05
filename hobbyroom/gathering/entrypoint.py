import http

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Response
from fastapi.routing import APIRouter

from hobbyroom import auth, constants, depends, exceptions
from hobbyroom.container import Container
from hobbyroom.gathering import command, service

router = APIRouter()


@router.post(
    "/v1/gatherings",
    status_code=http.HTTPStatus.CREATED,
    summary="모임 생성",
    description="새로운 모임을 생성합니다.",
    tags=[constants.OpenApiTag.GATHERING],
    responses=exceptions.get_responses(
        http.HTTPStatus.UNPROCESSABLE_ENTITY,
        http.HTTPStatus.UNAUTHORIZED,
        http.HTTPStatus.NOT_FOUND,
    ),
)
@inject
async def create_gathering(
    cmd: command.CreateGathering,
    user: auth.User = Depends(depends.get_current_user),
    handler: service.CreateGatheringHandler = Depends(
        Provide[Container.gathering.service.create_gathering_handler]
    ),
):
    cmd.validate_persona_id(user)
    handler.handle(cmd)
    return Response(status_code=http.HTTPStatus.CREATED)


@router.post(
    "/v1/gatherings/join",
    status_code=http.HTTPStatus.CREATED,
    summary="모임 참여",
    description="기존 모임에 일원으로 참여하여 소속을 만듭니다.",
    tags=[constants.OpenApiTag.GATHERING],
    responses=exceptions.get_responses(
        http.HTTPStatus.UNPROCESSABLE_ENTITY,
        http.HTTPStatus.UNAUTHORIZED,
        http.HTTPStatus.NOT_FOUND,
    ),
)
@inject
async def join_gathering(
    cmd: command.JoinGathering,
    user: auth.User = Depends(depends.get_current_user),
    handler: service.JoinGatheringHandler = Depends(
        Provide[Container.gathering.service.join_gathering_handler]
    ),
):
    cmd.validate_persona_id(user)
    handler.handle(cmd)
    return Response(status_code=http.HTTPStatus.CREATED)

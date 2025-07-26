import http

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Response
from fastapi.routing import APIRouter

from hobbyroom import auth, constants, exceptions, user
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
    user: user.User = Depends(auth.get_current_user),
    handler: service.CreateGatheringHandler = Depends(
        Provide[Container.gathering.service.create_gathering_handler]
    ),
):
    cmd.validate_persona_id(user)
    handler.handle(cmd)
    return Response(status_code=http.HTTPStatus.CREATED)

import http

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from hobbyroom import auth, constants, depends, exceptions
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


@router.get(
    "/v1/users/me",
    response_model=schema.UserInfo,
    status_code=http.HTTPStatus.OK,
    tags=[constants.OpenApiTag.USER],
    summary="현 사용자 정보 확인",
    description="현재 API에 요청을 보내는 사용자의 정보를 반환합니다.",
    responses=exceptions.get_responses(
        http.HTTPStatus.UNAUTHORIZED,
    ),
)
async def get_user_info(
    user: auth.User = Depends(depends.get_current_user),
) -> schema.UserInfo:
    return schema.UserInfo.from_auth_vo(user)


@router.post(
    "/v1/personas",
    status_code=http.HTTPStatus.CREATED,
    tags=[constants.OpenApiTag.USER],
    summary="사용자 페르소나 생성",
    description="그룹 활동에 사용할 사용자 페르소나를 생성합니다.",
    responses=exceptions.get_responses(
        http.HTTPStatus.UNPROCESSABLE_ENTITY,
        http.HTTPStatus.UNAUTHORIZED,
    ),
)
@inject
async def create_persona(
    cmd: command.CreatePersona,
    user: auth.User = Depends(depends.get_current_user),
    handler: service.CreatePersonaHandler = Depends(
        Provide[Container.user.service.create_persona_handler]
    ),
):
    cmd.user_id = user.id
    handler.handle(cmd)
    return Response(status_code=http.HTTPStatus.CREATED)

import http
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Response
from fastapi.routing import APIRouter

from hobbyroom import auth, constants, depends, exceptions
from hobbyroom.container import Container
from hobbyroom.gathering import command, domain, query, schema, service

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


@router.post(
    "/v1/gatherings/{gathering_id}/posts",
    status_code=http.HTTPStatus.CREATED,
    summary="게시글 작성",
    description="모임에 게시글을 작성합니다.",
    tags=[constants.OpenApiTag.GATHERING],
    responses=exceptions.get_responses(
        http.HTTPStatus.UNPROCESSABLE_ENTITY,
        http.HTTPStatus.UNAUTHORIZED,
        http.HTTPStatus.NOT_FOUND,
    ),
)
@inject
async def create_post(
    cmd: command.CreatePost,
    persona: auth.Persona = Depends(depends.get_current_persona),
    handler: service.CreatePostHandler = Depends(
        Provide[Container.gathering.service.create_post_handler]
    ),
):
    cmd.add_affiliation_info(persona=persona)
    handler.handle(cmd)
    return Response(status_code=http.HTTPStatus.CREATED)


@router.get(
    "/v1/gatherings/{gathering_id}/posts",
    response_model=schema.ListedPosts,
    status_code=http.HTTPStatus.OK,
    summary="게시글 목록 조회",
    description="모임에 작성된 게시글 목록을 조회합니다.",
    tags=[constants.OpenApiTag.GATHERING],
    responses=exceptions.get_responses(
        http.HTTPStatus.UNPROCESSABLE_ENTITY,
        http.HTTPStatus.UNAUTHORIZED,
        http.HTTPStatus.NOT_FOUND,
    ),
    dependencies=[Depends(depends.get_current_persona)],
)
@inject
async def list_posts(
    gathering_id: UUID,
    ascending: bool = False,
    page: int = 1,
    per_page: int = 10,
    handler: service.ListPostsHandler = Depends(
        Provide[Container.gathering.service.list_posts_handler]
    ),
):
    qry = query.ListPosts(
        gathering_id=gathering_id,
        ascending=ascending,
        page=page,
        per_page=per_page,
    )
    return handler.handle(qry)


@router.get(
    "/v1/gatherings/{gathering_id}/posts/{post_id}",
    response_model=domain.SearchedPost,
    status_code=http.HTTPStatus.OK,
    summary="게시글 조회",
    description="모임에 작성된 게시글을 조회합니다.",
    tags=[constants.OpenApiTag.GATHERING],
    responses=exceptions.get_responses(
        http.HTTPStatus.UNPROCESSABLE_ENTITY,
        http.HTTPStatus.UNAUTHORIZED,
        http.HTTPStatus.NOT_FOUND,
    ),
    dependencies=[Depends(depends.get_current_persona)],
)
@inject
async def retrieve_post(
    gathering_id: UUID,
    post_id: UUID,
    handler: service.RetrievePostHandler = Depends(
        Provide[Container.gathering.service.retrieve_post_handler]
    ),
):
    qry = query.RetrievePost(
        gathering_id=gathering_id,
        post_id=post_id,
    )
    return handler.handle(qry)


@router.patch(
    "/v1/gatherings/{gathering_id}/posts/{post_id}",
    status_code=http.HTTPStatus.OK,
    summary="게시글 수정",
    description="모임에 작성된 게시글을 수정합니다.",
    tags=[constants.OpenApiTag.GATHERING],
    responses=exceptions.get_responses(
        http.HTTPStatus.UNPROCESSABLE_ENTITY,
        http.HTTPStatus.UNAUTHORIZED,
        http.HTTPStatus.NOT_FOUND,
    ),
)
@inject
async def update_post(
    gathering_id: UUID,
    post_id: UUID,
    cmd: command.UpdatePost,
    persona: auth.Persona = Depends(depends.get_current_persona),
    handler: service.UpdatePostHandler = Depends(
        Provide[Container.gathering.service.update_post_handler]
    ),
):
    cmd.add_entity_ids(post_id=post_id, persona=persona)
    handler.handle(cmd)
    return Response(status_code=http.HTTPStatus.OK)

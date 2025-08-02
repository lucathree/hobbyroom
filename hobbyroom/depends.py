from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from hobbyroom import exceptions
from hobbyroom.auth import adapter, domain, service
from hobbyroom.container import Container

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/v1/users/auth")


@inject
def get_current_user(
    token: str = Depends(oauth2_schema),
    jwt_handler: service.JWTHandler = Depends(
        Provide[Container.auth.service.jwt_handler]
    ),
    auth_unit_of_work: adapter.AuthUnitOfWork = Depends(
        Provide[Container.auth.adapter.auth_unit_of_work]
    ),
) -> domain.User:
    payload = jwt_handler.decode(token)

    with auth_unit_of_work as uow:
        user = uow.user.find_by_email(payload.sub)

    if not user:
        raise exceptions.UnauthorizedError("인증 정보가 유효하지 않습니다.")

    return user

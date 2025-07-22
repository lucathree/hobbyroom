from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from hobbyroom import exceptions, user
from hobbyroom.container import Container

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/v1/users/auth")


@inject
def get_current_user(
    token: str = Depends(oauth2_schema),
    jwt_handler: user.JWTHandler = Depends(Provide[Container.user.service.jwt_handler]),
    user_unit_of_work: user.UserUnitOfWork = Depends(
        Provide[Container.user.adapter.user_unit_of_work]
    ),
) -> user.User:
    payload = jwt_handler.decode(token)

    with user_unit_of_work as uow:
        user = uow.user.find_by_email(payload.sub)

    if not user:
        raise exceptions.UnauthorizedError("인증 정보가 유효하지 않습니다.")

    return user

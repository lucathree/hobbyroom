from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from hobbyroom import auth, exceptions
from hobbyroom.container import Container


@inject
def get_current_user(
    token: str = Depends(auth.user_oauth2_schema),
    jwt_handler: auth.JWTHandler = Depends(Provide[Container.auth.service.jwt_handler]),
    auth_unit_of_work: auth.AuthUnitOfWork = Depends(
        Provide[Container.auth.adapter.auth_unit_of_work]
    ),
) -> auth.User:
    payload = jwt_handler.decode(token)

    with auth_unit_of_work as uow:
        user = uow.user.find_by_email(payload.sub)

    if not user:
        raise exceptions.UnauthorizedError("인증 정보가 유효하지 않습니다.")

    return user

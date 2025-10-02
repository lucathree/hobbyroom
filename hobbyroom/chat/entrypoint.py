from dependency_injector.wiring import Provide, inject
from fastapi import Depends, WebSocket
from fastapi.routing import APIRouter

from hobbyroom import auth, depends
from hobbyroom.chat import connection_manager, domain
from hobbyroom.container import Container
from hobbyroom.logging import get_logger

router = APIRouter()
logger = get_logger()


@router.websocket("/v1/chat/{gathering_id}")
@inject
async def chat_endpoint(
    websocket: WebSocket,
    persona: auth.Persona = Depends(depends.get_current_persona_ws),
    connection_manager: connection_manager.ConnectionManager = Depends(
        Provide[Container.chat.service.connection_manager]
    ),
):
    connection_info = domain.ConnectionInfo(
        persona_id=persona.id,
        persona_name=persona.name,
        gathering_id=persona.gathering_id,
    )
    try:
        await connection_manager.connect(websocket, connection_info)
        while True:
            await connection_manager.receive_message(websocket, connection_info)
    except Exception:
        await connection_manager.disconnect(websocket, connection_info)
    finally:
        connection_manager.refresh_connections()

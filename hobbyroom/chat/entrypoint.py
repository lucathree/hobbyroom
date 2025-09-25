from dependency_injector.wiring import Provide, inject
from fastapi import Depends, WebSocket
from fastapi.routing import APIRouter

from hobbyroom import auth, depends
from hobbyroom.chat import connection_manager
from hobbyroom.container import Container

router = APIRouter()


@router.websocket("/v1/chat/{gathering_id}")
@inject
async def chat_endpoint(
    websocket: WebSocket,
    persona: auth.Persona = Depends(depends.get_current_persona_ws),
    connection_manager: connection_manager.ConnectionManager = Depends(
        Provide[Container.chat.service.connection_manager]
    ),
):
    try:
        await connection_manager.connect(websocket, persona)
        while True:
            await connection_manager.receive_message(websocket, persona)
    except Exception:
        await connection_manager.disconnect(websocket, persona)

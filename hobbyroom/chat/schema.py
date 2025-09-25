import datetime
from uuid import UUID

from pydantic import BaseModel

from hobbyroom.chat import enums


class IncomingMessage(BaseModel):
    content: str
    message_type: enums.MessageType = enums.MessageType.TEXT


class OutgoingMessage(BaseModel):
    content: str
    message_type: enums.MessageType
    timestamp: datetime.datetime


class UserMessage(OutgoingMessage):
    persona_id: UUID
    persona_name: str


class SystemMessage(OutgoingMessage):
    message_type: enums.MessageType = enums.MessageType.SYSTEM

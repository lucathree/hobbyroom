import enum


class MessageType(str, enum.Enum):
    TEXT = enum.auto()
    JOIN = enum.auto()
    LEAVE = enum.auto()
    SYSTEM = enum.auto()

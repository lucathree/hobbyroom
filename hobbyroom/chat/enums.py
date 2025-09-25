import enum


class MessageType(enum.StrEnum):
    TEXT = enum.auto()
    JOIN = enum.auto()
    LEAVE = enum.auto()
    SYSTEM = enum.auto()

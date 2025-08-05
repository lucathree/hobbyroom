import enum


class OpenApiTag(enum.StrEnum):
    AUTH = enum.auto()
    USER = enum.auto()
    GATHERING = enum.auto()

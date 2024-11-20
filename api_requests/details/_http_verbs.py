"""Enums representing the HTTP verbs, i.e., GET, POST, etc."""

from enum import IntEnum, auto, unique


@unique
class HttpVerbs(IntEnum):
    """HTTP verbs."""

    GET = auto()
    OPTIONS = auto()
    HEAD = auto()
    POST = auto()
    PUT = auto()
    PATCH = auto()
    DELETE = auto()

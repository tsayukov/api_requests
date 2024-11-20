"""Interface for an error handler."""

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Concatenate


@dataclass(slots=True, frozen=True, eq=False, match_args=False, kw_only=True)
class ErrorHandler[Cls: object, R, **P]:
    error_handler: Callable[Concatenate[Cls, P], R]
    api_methods: Iterable[str]
    error_codes: int | Iterable[int] | None

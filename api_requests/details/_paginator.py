"""Interface of a paginator."""

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Concatenate


@dataclass(slots=True, frozen=True, eq=False, match_args=False, kw_only=True)
class Paginator[Cls: object, R, **P]:
    paginator: Callable[Concatenate[Cls, P], R]
    api_methods: Iterable[str]

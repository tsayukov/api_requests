"""Interface and properties of an API method."""

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Concatenate

from api_requests.details._http_verbs import HttpVerbs


@dataclass(slots=True, frozen=True, eq=False, match_args=False, kw_only=True)
class ApiMethodProperties:
    http_verb: HttpVerbs
    api_method: str
    ok_codes: int | Iterable[int]
    error_codes: int | Iterable[int] | None
    pagination: bool
    kwargs: Mapping[str, Any]


@dataclass(slots=True, frozen=True, eq=False, match_args=False, kw_only=True)
class ApiMethod[Cls: object, R, **P]:
    method: Callable[Concatenate[Cls, P], R]
    properties: ApiMethodProperties

"""HTTP query string."""

from dataclasses import dataclass, field

from api_requests.details._common import Missing, MISSING


@dataclass(slots=True, frozen=True)
class QueryPart:
    """Part of an HTTP query string."""

    key: str
    value: str | Missing = field(default=MISSING)

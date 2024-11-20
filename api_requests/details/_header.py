"""HTTP header."""

from dataclasses import dataclass, field

from api_requests.details._common import Missing, MISSING


@dataclass(slots=True, frozen=True)
class HeaderPart:
    """Part of an HTTP header."""

    key: str
    value: str | Missing = field(default=MISSING)

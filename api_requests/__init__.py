"""Generating API client classes."""

from api_requests.init_args import (
    header,
    query,
)
from api_requests.decorators import (
    configure,
)


__all__ = [
    "configure",
    "header",
    "query",
]

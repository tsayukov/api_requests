"""Generating API client classes."""

from api_requests.init_args import (
    header,
    query,
)
from api_requests.decorators import (
    configure,
    get,
    options,
    head,
    post,
    put,
    patch,
    delete,
)


__all__ = [
    "configure",
    "header",
    "query",
    "get",
    "options",
    "head",
    "post",
    "put",
    "patch",
    "delete",
]

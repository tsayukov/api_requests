"""Decorators for generating API client classes and their methods."""

from fractions import Fraction
from typing import Any, Callable


def _configure_api_client[
    Cls: object
](
    cls: type[Cls],
    /,
    *,
    suffix: str | None,
    requests_per_sec: Fraction | None,
    request_timeout_sec: float,
    attempts_after_timeout: int,
    delay_before_attempt_sec: float,
    **kwargs: Any,
) -> type[Cls]:
    raise NotImplementedError


def configure[
    Cls: object
](
    cls: type[Cls] | None = None,
    suffix: str | None = None,
    /,
    *,
    requests_per_sec: tuple[int, int] | None = None,
    request_timeout_sec: float = 5,
    attempts_after_timeout: int = 10,
    delay_before_attempt_sec: float = 5,
    **kwargs: Any,
) -> (Cls | Callable[[type[Cls]], type[Cls]]):
    """Configure a class as an API client class.

    TODO: add parameter's description
    """

    def wraps(cls: type[Cls]) -> type[Cls]:
        return _configure_api_client(
            cls,
            suffix=suffix,
            requests_per_sec=Fraction(requests_per_sec[0], requests_per_sec[1]),
            request_timeout_sec=request_timeout_sec,
            attempts_after_timeout=attempts_after_timeout,
            delay_before_attempt_sec=delay_before_attempt_sec,
            **kwargs,
        )

    if cls is None:
        return wraps

    return wraps(cls)

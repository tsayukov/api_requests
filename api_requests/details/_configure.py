"""API client class configuration."""

from fractions import Fraction
from typing import Any


def configure_impl[
    Cls: object
](
    cls: type[Cls],
    /,
    *,
    suffix: str | None,
    requests_per_sec: tuple[int, int] | None,
    request_timeout_sec: float,
    attempts_after_timeout: int,
    delay_before_attempt_sec: float,
    **kwargs: Any,
) -> type[Cls]:
    raise NotImplementedError

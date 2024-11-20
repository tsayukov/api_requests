"""Decorators for generating API client classes and their methods."""

from collections.abc import Iterable
from fractions import Fraction
from typing import Any, Callable, Concatenate, Final

from api_requests.details._api_method import ApiMethodInterface, ApiMethodProperties
from api_requests.details._http_verbs import HttpVerbs


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


def _make_api_method_decorator(http_verb: HttpVerbs):
    def decorator[
        Cls: object, R, **P
    ](
        api_method: str,
        /,
        *,
        ok_codes: int | Iterable[int] = 200,
        error_codes: int | Iterable[int] | None = None,
        pagination: bool = False,
        **kwargs: Any,
    ) -> Callable[[Callable[Concatenate[Cls, P], R]], ApiMethodInterface[Cls, R, P]]:
        """Add an API method to request to the server. The name of this decorator
        indicates the appropriate HTTP request method, i.e., GET, POST, etc.

        Use this decorator only for methods of an API client class.

        TODO: add parameter's description
        """

        def wraps(method: Callable[Concatenate[Cls, P], R]):
            return ApiMethodInterface(
                method=method,
                properties=ApiMethodProperties(
                    http_verb=http_verb,
                    api_method=api_method,
                    ok_codes=ok_codes,
                    error_codes=error_codes,
                    pagination=pagination,
                    kwargs=kwargs,
                ),
            )

        return wraps

    return decorator


get: Final = _make_api_method_decorator(HttpVerbs.GET)
options: Final = _make_api_method_decorator(HttpVerbs.OPTIONS)
head: Final = _make_api_method_decorator(HttpVerbs.HEAD)
post: Final = _make_api_method_decorator(HttpVerbs.POST)
put: Final = _make_api_method_decorator(HttpVerbs.PUT)
patch: Final = _make_api_method_decorator(HttpVerbs.PATCH)
delete: Final = _make_api_method_decorator(HttpVerbs.DELETE)

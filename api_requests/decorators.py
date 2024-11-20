"""Decorators for generating API client classes and their methods."""

from collections.abc import Iterable
from typing import Any, Callable, Concatenate, Final

from api_requests.details._api_method import ApiMethodInterface, ApiMethodProperties
from api_requests.details._common import BASE_FIELD_NAME
from api_requests.details._configure import configure_impl
from api_requests.details._error_handler import ErrorHandlerInterface
from api_requests.details._http_verbs import HttpVerbs
from api_requests.details._paginator import PaginatorInterface


def configure[
    Cls: object
](
    cls: type[Cls] | None = None,
    suffix: str | None = None,
    /,
    *,
    keep_alive: bool = True,
    requests_per_sec: tuple[int, int] | None = None,
    request_timeout_sec: float = 5,
    attempts_after_timeout: int = 10,
    delay_before_attempt_sec: float = 5,
    rename_base_field: str = BASE_FIELD_NAME,
    **kwargs: Any,
) -> (Cls | Callable[[type[Cls]], type[Cls]]):
    """Configure a class as an API client class.

    TODO: add parameter's description
    """

    def wraps(cls: type[Cls]) -> type[Cls]:
        return configure_impl(
            cls,
            suffix=suffix,
            keep_alive=keep_alive,
            requests_per_sec=requests_per_sec,
            request_timeout_sec=request_timeout_sec,
            attempts_after_timeout=attempts_after_timeout,
            delay_before_attempt_sec=delay_before_attempt_sec,
            rename_base_field=rename_base_field,
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


def error_handler[
    Cls: object, R, **P
](
    method: Callable[Concatenate[Cls, P], R] | None = None,
    /,
    *api_methods: str,
    error_codes: int | Iterable[int] | None = None,
) -> (
    ErrorHandlerInterface[Cls, R, P]
    | Callable[[Callable[Concatenate[Cls, P], R]], ErrorHandlerInterface[Cls, R, P]]
):
    """Mark a method as an error handler for API methods that raise errors.

    Use this decorator only for methods of an API client class.
    If 'api_methods' is present, use this error handler only for those API methods.
    If 'error_codes' is present, use this error handler only if the API methods
    return one of those error codes.
    """

    def wraps(method: Callable[Concatenate[Cls, P], R]):
        return ErrorHandlerInterface(
            error_handler=method, api_methods=api_methods, error_codes=error_codes
        )

    if method is None:
        return wraps

    return wraps(method)


def paginator[
    Cls: object, R, **P
](
    method: Callable[Concatenate[Cls, P], R] | None = None,
    /,
    *api_methods: str,
) -> (
    PaginatorInterface[Cls, R, P]
    | Callable[[Callable[Concatenate[Cls, P], R]], PaginatorInterface[Cls, R, P]]
):
    """Mark a method as a paginator for API methods that return data page by page.

    Use this decorator only for methods of an API client class.
    If 'api_methods' is present, use this paginator only for those API methods.
    """

    def wraps(method: Callable[Concatenate[Cls, P], R]):
        return PaginatorInterface(paginator=method, api_methods=api_methods)

    if method is None:
        return wraps

    return wraps(method)

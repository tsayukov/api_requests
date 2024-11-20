"""Functions to add keyword-only arguments to '__init__' of an API client class."""

from typing import TypeAlias

from api_requests.details._header import HeaderPart
from api_requests.details._query import QueryPart


KeyOrKeyWithDefault: TypeAlias = str | tuple[str, str]


def _header_query_impl[
    TPart: (HeaderPart, QueryPart)
](part_type: type[TPart], *args: KeyOrKeyWithDefault) -> list[TPart]:
    parts: list[TPart] = []
    for k_or_kwdef in args:
        if isinstance(k_or_kwdef, str):
            key = k_or_kwdef
            parts.append(part_type(key))
        elif len(k_or_kwdef) == 2:
            key = k_or_kwdef[0]
            default = k_or_kwdef[1]
            parts.append(part_type(key, default))
        else:
            raise TypeError("Expected either a key or a tuple of key-value.")

    return parts


def header(
    key_or_key_with_default: KeyOrKeyWithDefault, /, *args: KeyOrKeyWithDefault
) -> list[HeaderPart]:
    """Add mandatory keys to the HTTP header.

    Call this function only inside an API client class definition.
    Use the name of the variable or the names of the variables in the tuple
    to which the result of this function call is assigned as keyword-only
    arguments during the initialization of the API client class. Each
    keyword-only argument will have a default value if the corresponding
    key and that value in this function call are represented as a tuple.

    Usage:

        import api_requests
        import os

        @api_requests.configure()
        class Client:
            api_key = api_requests.header("Api-Key")
            key_1, key_2 = api_requests.header(("Key-1", "default-value"), "Key-2")

            # Some API methods...

        # Read a secret key from the environment or file
        secret_key = os.environ.get("YOUR_SECRET_KEY_ENV_VARIABLE")

        client = Client(
            url="https://example.com",
            api_key=secret_key,
            # 'key_1' has the default value 'default-value' and can be omitted
            key_2="user-value",
        )

        # Each HTTP request via 'client' will send the following header:
        # {
        #     "Api-Key": secret_key,
        #     "Key-1": "default-value",
        #     "Key-2": "user-value",
        #     # the rest of the header the 'requests' module takes care about
        # }
    """

    return _header_query_impl(HeaderPart, key_or_key_with_default, *args)


def query(
    key_or_key_with_default: KeyOrKeyWithDefault, /, *args: KeyOrKeyWithDefault
) -> list[QueryPart]:
    """Set a query string that will be a mandatory part of the URL API.

    Call this function only inside an API client class definition.
    Use the name of the variable or the names of the variables in the tuple
    to which the result of this function call is assigned as keyword-only
    arguments during the initialization of the API client class. Each
    keyword-only argument will have a default value if the corresponding
    key and that value in this function call are represented as a tuple.

    Usage:

        import api_requests
        import os

        @api_requests.configure()
        class Client:
            api_key = api_requests.query("Api-Key")
            key_1, key_2 = api_requests.query(("Key-1", "default-value"), "Key-2")

            # Some API methods...

        # Read a secret key from the environment or file
        secret_key = os.environ.get("YOUR_SECRET_KEY_ENV_VARIABLE")

        client = Client(
            url="https://example.com",
            api_key=<secret_key>,
            # 'key_1' has the default value 'default-value' and can be omitted
            key_2="value",
        )

        # Each HTTP request via 'client' will have the following URL
        # (the indents are shown for clarity):
        #
        # https://example.com/<api_method>?Api-Key=<secret_key>
        #                                 &Key-1=default-value
        #                                 &Key-2=user-value
        #                                 &<rest-of-api-method-parameters-if-any>
    """

    return _header_query_impl(QueryPart, key_or_key_with_default, *args)

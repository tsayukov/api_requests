"""Common types and variables."""

from typing import Final


class Missing:
    """Represent a missing value when 'None' is not suitable, e.g., 'None' is a valid value."""


MISSING: Final = Missing()

BASE_FIELD_NAME: Final = "_api_requests_base"

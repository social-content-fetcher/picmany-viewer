"""Exceptions raised by picmany-viewer."""

from __future__ import annotations

from typing import Optional


class PicmanyError(Exception):
    """Base class for every error this package raises.

    ``web_url``, when set, is the same profile, post, reel or topic on picmany.com, which anyone can open in a browser.
    """

    def __init__(self, message: str, web_url: Optional[str] = None) -> None:
        super().__init__(message)
        self.web_url = web_url


class InvalidInputError(PicmanyError, ValueError):
    """The input is not an Instagram/PicMany link, username, shortcode or topic this package understands."""


class AccessRestrictedError(PicmanyError):
    """PicMany refused a data request.

    PicMany has no open data API: requests without an access key are refused before they leave your machine, and
    requests with a key the service does not accept are refused by the service. ``web_url`` is the same content on
    picmany.com.
    """

    def __init__(self, message: str, web_url: Optional[str] = None, status: Optional[int] = None) -> None:
        super().__init__(message, web_url)
        self.status = status


class RateLimitedError(PicmanyError):
    """The service asked the client to slow down (HTTP 429)."""

    def __init__(self, message: str, web_url: Optional[str] = None, retry_after: Optional[int] = None) -> None:
        super().__init__(message, web_url)
        self.retry_after = retry_after


class ServiceError(PicmanyError):
    """Any other failure: a network error, a 5xx answer or a body that is not the JSON the client expects."""

"""picmany-viewer: open Instagram profiles, posts, reels and topics on PicMany (https://picmany.com), the free
Instagram viewer, from Python or the command line."""

__version__ = "0.1.0"

from .client import PicmanyClient  # noqa: E402
from .errors import (  # noqa: E402
    AccessRestrictedError,
    InvalidInputError,
    PicmanyError,
    RateLimitedError,
    ServiceError,
)
from .links import resolve, to_picmany_url  # noqa: E402

__all__ = [
    "PicmanyClient",
    "PicmanyError",
    "AccessRestrictedError",
    "InvalidInputError",
    "RateLimitedError",
    "ServiceError",
    "resolve",
    "to_picmany_url",
    "__version__",
]

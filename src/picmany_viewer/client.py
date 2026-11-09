"""Data client for PicMany.

PicMany (https://picmany.com) is a website for people, not a data API. The data endpoints this client speaks are
closed:

* without an access key (``api_key=`` or the ``PICMANY_API_KEY`` environment variable) every data call raises
  :class:`~picmany_viewer.errors.AccessRestrictedError` before any request is sent;
* with a key, the request is sent and the service's refusal (401, 403, 404) is raised as the same error.

Every error a data call raises carries ``web_url``: the same profile, post, reel or topic on picmany.com, which anyone
can open in a browser without an Instagram account. That is the supported way to view Instagram through PicMany.
"""

from __future__ import annotations

import json
import os
from typing import Any, Callable, Dict, List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from . import __version__, links
from .errors import AccessRestrictedError, InvalidInputError, RateLimitedError, ServiceError
from .models import Highlight, Page, Post, Profile, Story, Topic

API_PATH = "/api/v1"
ENV_KEY = "PICMANY_API_KEY"

_CLOSED = (
    "PicMany has no open data API, so this request was not sent. "
    "Open the page in your browser instead (no Instagram account needed): {url}"
)
_REFUSED = "PicMany refused the data request (HTTP {status}). Open the page in your browser instead: {url}"

Opener = Callable[..., Any]


class PicmanyClient:
    """Typed access to PicMany pages; see the module docstring for what works without an access key (only links)."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = links.DEFAULT_BASE_URL,
        timeout: float = 15.0,
        opener: Optional[Opener] = None,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.environ.get(ENV_KEY) or None
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._open = opener or urlopen

    # -- links: always available, no network ---------------------------------------------------------------------

    def url_for(self, value: str) -> str:
        """The PicMany page of an Instagram link, ``@username``, ``username`` or ``#topic``."""
        return links.to_picmany_url(value, self.base_url)

    # -- data: needs an access key ---------------------------------------------------------------------------------

    def profile(self, username: str) -> Profile:
        t = links.profile(username)
        return Profile.from_dict(self._get(f"/users/{quote(t.username or '')}", t))

    def posts(self, username: str, cursor: Optional[str] = None) -> Page:
        t = links.profile(username)
        return Page.from_dict(self._get(f"/users/{quote(t.username or '')}/posts", t, {"cursor": cursor}))

    def reels(self, username: str, cursor: Optional[str] = None) -> Page:
        t = links.profile(username)
        return Page.from_dict(self._get(f"/users/{quote(t.username or '')}/reels", t, {"cursor": cursor}))

    def stories(self, username: str) -> List[Story]:
        t = links.profile(username)
        data = self._get(f"/users/{quote(t.username or '')}/stories", t)
        return [Story.from_dict(s) for s in data.get("items") or []]

    def highlights(self, username: str) -> List[Highlight]:
        t = links.profile(username)
        data = self._get(f"/users/{quote(t.username or '')}/highlights", t)
        return [Highlight.from_dict(h) for h in data.get("items") or []]

    def post(self, link_or_shortcode: str) -> Post:
        value = link_or_shortcode.strip()
        t = links.resolve(value) if "/" in value or "." in value else links.post(value)
        if t.kind not in ("post", "reel"):
            raise InvalidInputError(f"not an Instagram post or reel: {link_or_shortcode!r}")
        return Post.from_dict(self._get(f"/media/{quote(t.shortcode or '')}", t))

    def popular(self, keyword: str, cursor: Optional[str] = None) -> Topic:
        t = links.popular(keyword)
        return Topic.from_dict(self._get(f"/popular/{quote(t.keyword or '', safe='')}", t, {"cursor": cursor}))

    def popular_reels(self, cursor: Optional[str] = None) -> Page:
        t = links.popular_reels()
        return Page.from_dict(self._get("/reels/popular", t, {"cursor": cursor}))

    # -- transport ---------------------------------------------------------------------------------------------------

    def _get(self, path: str, target: links.Target, params: Optional[Dict[str, Optional[str]]] = None) -> Dict[str, Any]:
        web_url = target.url(self.base_url)
        if not self.api_key:
            raise AccessRestrictedError(_CLOSED.format(url=web_url), web_url=web_url)

        query = urlencode({k: v for k, v in (params or {}).items() if v})
        url = f"{self.base_url}{API_PATH}{path}" + (f"?{query}" if query else "")
        req = Request(
            url,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": f"picmany-viewer/{__version__} (+https://github.com/social-content-fetcher/picmany-viewer)",
            },
        )
        try:
            with self._open(req, timeout=self.timeout) as resp:
                body = resp.read()
        except HTTPError as e:
            if e.code in (401, 403, 404, 410):
                raise AccessRestrictedError(_REFUSED.format(status=e.code, url=web_url), web_url=web_url, status=e.code) from None
            if e.code == 429:
                retry = e.headers.get("Retry-After") if e.headers else None
                raise RateLimitedError(
                    f"PicMany asked to slow down (HTTP 429). Open the page in your browser instead: {web_url}",
                    web_url=web_url,
                    retry_after=int(retry) if retry and retry.isdigit() else None,
                ) from None
            raise ServiceError(f"PicMany answered HTTP {e.code}. Open the page in your browser: {web_url}", web_url) from None
        except URLError as e:
            raise ServiceError(f"could not reach PicMany: {e.reason}", web_url) from None

        try:
            data = json.loads(body)
        except ValueError:
            raise ServiceError(f"PicMany's answer was not JSON. Open the page in your browser: {web_url}", web_url) from None
        if not isinstance(data, dict):
            raise ServiceError(f"PicMany's answer was not a JSON object. Open the page in your browser: {web_url}", web_url)
        return data

"""Turn Instagram links, usernames and topics into their PicMany page.

PicMany mirrors Instagram's URL structure for profiles, posts and reels, so most links only need their host swapped::

    https://www.instagram.com/natgeo/        ->  https://picmany.com/natgeo
    https://www.instagram.com/p/C8xYz12AbCd/ ->  https://picmany.com/p/C8xYz12AbCd
    https://www.instagram.com/reel/C9aBc3D/  ->  https://picmany.com/reel/C9aBc3D

Everything here is pure string handling: no network request is made.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import List, Optional
from urllib.parse import quote, unquote, urlsplit

from .errors import InvalidInputError

DEFAULT_BASE_URL = "https://picmany.com"

PICMANY_HOSTS = {"picmany.com", "www.picmany.com"}

# Same rules as Instagram (and picmany.com): lower case, letters, digits, "." and "_", at most 30 characters, no "..",
# no trailing ".", and it may not start with ".".
_USERNAME_RE = re.compile(r"^[a-z0-9_][a-z0-9._]{0,29}$")
_SHORTCODE_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
_KEYWORD_FORBIDDEN = re.compile(r"[/\\?#%]")
_MAX_KEYWORD = 120

# First path segments on instagram.com that are Instagram's own pages, not a person's.
_INSTAGRAM_PATHS = {"accounts", "direct", "developer", "legal", "web", "challenge", "emails", "session"}

# Paths that belong to picmany.com itself and are never a profile.
RESERVED_PATHS = {
    "about", "api", "contact", "explore", "health", "how-we-count", "locations", "most-followed", "p",
    "picuki-alternative", "popular", "privacy", "reel", "reels", "remove-profile", "search", "terms", "404", "500",
    "robots.txt", "sitemap.xml", "sitemap-index.xml", "sitemap-pages.xml", "opensearch.xml", "favicon.ico",
    "favicon.svg", "favicon.png", "manifest.json", "site.webmanifest", "browserconfig.xml", "og-default.png",
    "apple-touch-icon.png", "apple-touch-icon-precomposed.png", "icon-192.png", "icon-512.png",
    "icon-maskable-512.png",
}

# Information pages on picmany.com that a picmany.com link may point to.
_PICMANY_PAGES = {"about", "contact", "how-we-count", "most-followed", "picuki-alternative", "privacy",
                  "remove-profile", "terms"}


@dataclass(frozen=True)
class Target:
    """A page PicMany serves: its kind and the canonical path on picmany.com."""

    kind: str  # "profile", "post", "reel", "popular", "reels", "page", "home"
    path: str
    username: Optional[str] = None
    shortcode: Optional[str] = None
    keyword: Optional[str] = None

    def url(self, base_url: str = DEFAULT_BASE_URL) -> str:
        return base_url.rstrip("/") + self.path


# -- validation --------------------------------------------------------------------------------------------------------


def normalize_username(raw: str) -> str:
    """``@NatGeo`` -> ``natgeo``; raises :class:`InvalidInputError` when it cannot be an Instagram username."""
    u = unquote(raw).strip().lstrip("@").lower()
    if not _USERNAME_RE.match(u) or ".." in u or u.endswith("."):
        raise InvalidInputError(f"not an Instagram username: {raw!r}")
    if u in RESERVED_PATHS:
        raise InvalidInputError(f"{raw!r} is a PicMany page, not a profile")
    return u


def normalize_keyword(raw: str) -> str:
    """The one spelling picmany.com keeps a topic under: NFC, lower case, hyphens and runs of spaces folded."""
    k = unicodedata.normalize("NFC", unquote(raw)).strip().lstrip("#").lower()
    k = k.replace("i̇", "i")  # Turkish "İ" lowercases to "i" + combining dot
    k = re.sub(r"[-\s]+", " ", k).strip()
    if not k or len(k) > _MAX_KEYWORD or _KEYWORD_FORBIDDEN.search(k) or set(k) == {"."}:
        raise InvalidInputError(f"not a topic PicMany can show: {raw!r}")
    if not any(c.isalnum() for c in k) or any(ord(c) < 0x20 or ord(c) == 0x7F for c in k):
        raise InvalidInputError(f"not a topic PicMany can show: {raw!r}")
    return k


def _shortcode(raw: str) -> str:
    s = unquote(raw).strip()
    if not _SHORTCODE_RE.match(s):
        raise InvalidInputError(f"not an Instagram post or reel code: {raw!r}")
    return s


# -- targets -----------------------------------------------------------------------------------------------------------


def profile(username: str) -> Target:
    u = normalize_username(username)
    return Target("profile", f"/{quote(u)}", username=u)


def post(shortcode: str) -> Target:
    s = _shortcode(shortcode)
    return Target("post", f"/p/{quote(s)}", shortcode=s)


def reel(shortcode: str) -> Target:
    s = _shortcode(shortcode)
    return Target("reel", f"/reel/{quote(s)}", shortcode=s)


def popular(keyword: str) -> Target:
    k = normalize_keyword(keyword)
    return Target("popular", f"/popular/{quote(k, safe='')}", keyword=k)


def popular_reels() -> Target:
    return Target("reels", "/reels")


def home() -> Target:
    return Target("home", "/")


# -- links -------------------------------------------------------------------------------------------------------------


def _segments(path: str) -> List[str]:
    return [unquote(s) for s in path.split("/") if s]


def _is_instagram(host: str) -> bool:
    return host in ("instagram.com", "instagr.am") or host.endswith((".instagram.com", ".instagr.am"))


def _from_instagram(path: str, raw: str) -> Target:
    seg = _segments(path)
    if seg and seg[0] == "_u":  # the app's deep-link form of a profile
        seg = seg[1:]
    if not seg:
        return home()
    head = seg[0].lower()
    second = seg[1] if len(seg) > 1 else ""

    if head == "stories":
        if second and second.lower() != "highlights":
            return profile(second)  # stories open in the Stories tab of the profile
        raise InvalidInputError(f"PicMany has no page for this Instagram link: {raw!r}")
    if head == "explore":
        if second.lower() == "tags" and len(seg) > 2:
            return popular(seg[2])
        raise InvalidInputError(f"PicMany has no page for this Instagram link: {raw!r}")
    if head == "reels" and not second:
        return popular_reels()

    # /p/<code>, /reel/<code>, /reels/<code>, /tv/<code> and the newer /<user>/p/<code> form.
    for i in (0, 1):
        if len(seg) > i + 1:
            kind, code = seg[i].lower(), seg[i + 1]
            if kind in ("p", "tv", "reel", "reels") and code != "audio" and _SHORTCODE_RE.match(code):
                return post(code) if kind in ("p", "tv") else reel(code)

    if head in _INSTAGRAM_PATHS:
        raise InvalidInputError(f"PicMany has no page for this Instagram link: {raw!r}")
    return profile(seg[0])


def _from_picmany(path: str, raw: str) -> Target:
    seg = _segments(path)
    if not seg:
        return home()
    head = seg[0].lower()
    if head == "p" and len(seg) > 1:
        return post(seg[1])
    if head == "reel" and len(seg) > 1:
        return reel(seg[1])
    if head == "popular":
        return popular(seg[1]) if len(seg) > 1 else Target("page", "/popular")
    if head == "reels":
        return popular_reels()
    if head in _PICMANY_PAGES:
        return Target("page", "/" + "/".join(quote(s) for s in [head] + seg[1:]))
    if len(seg) == 1:
        return profile(seg[0])
    raise InvalidInputError(f"not a PicMany page this package knows: {raw!r}")


def resolve(value: str) -> Target:
    """The PicMany page for an Instagram or PicMany link, ``@username``, ``username`` or ``#topic``.

    Share parameters (``?igsh=``, ``?utm_source=``) are ignored. Raises :class:`InvalidInputError` for anything PicMany
    has no page for (direct messages, settings, place pages, private highlights links, other sites).
    """
    raw = (value or "").strip()
    if not raw:
        raise InvalidInputError("empty input")

    looks_like_link = "://" in raw or re.match(r"^(?:[a-z0-9-]+\.)*(?:instagram\.com|instagr\.am|picmany\.com)(?:[/?#]|$)", raw, re.I)
    if looks_like_link:
        parts = urlsplit(raw if "://" in raw else "https://" + raw)
        host = (parts.hostname or "").lower()
        if _is_instagram(host):
            return _from_instagram(parts.path, raw)
        if host in PICMANY_HOSTS:
            return _from_picmany(parts.path, raw)
        raise InvalidInputError(f"not an Instagram or PicMany link: {raw!r}")

    if raw.startswith("#"):
        return popular(raw)
    try:
        return profile(raw)
    except InvalidInputError:
        if raw.startswith("@"):
            raise
        return popular(raw)


def to_picmany_url(value: str, base_url: str = DEFAULT_BASE_URL) -> str:
    """The picmany.com address for an Instagram link, ``@username``, ``username`` or ``#topic``."""
    return resolve(value).url(base_url)

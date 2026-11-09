"""Typed records for PicMany data responses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _int(d: Dict[str, Any], key: str) -> int:
    try:
        return int(d.get(key) or 0)
    except (TypeError, ValueError):
        return 0


def _str(d: Dict[str, Any], key: str) -> str:
    v = d.get(key)
    return "" if v is None else str(v)


@dataclass(frozen=True)
class Profile:
    username: str
    full_name: str = ""
    biography: str = ""
    external_url: Optional[str] = None
    is_verified: bool = False
    is_private: bool = False
    followers: int = 0
    following: int = 0
    posts: int = 0
    profile_pic_url: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Profile":
        return cls(
            username=_str(d, "username"),
            full_name=_str(d, "full_name"),
            biography=_str(d, "biography"),
            external_url=d.get("external_url"),
            is_verified=bool(d.get("is_verified", False)),
            is_private=bool(d.get("is_private", False)),
            followers=_int(d, "followers"),
            following=_int(d, "following"),
            posts=_int(d, "posts"),
            profile_pic_url=d.get("profile_pic_url"),
            url=d.get("url"),
        )


@dataclass(frozen=True)
class Post:
    shortcode: str
    owner: str = ""
    media_type: str = "photo"  # "photo", "video" or "carousel"
    is_reel: bool = False
    caption: str = ""
    taken_at: Optional[str] = None
    likes: int = 0
    comments: int = 0
    views: int = 0
    hashtags: List[str] = field(default_factory=list)
    thumbnail_url: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Post":
        return cls(
            shortcode=_str(d, "shortcode"),
            owner=_str(d, "owner"),
            media_type=_str(d, "media_type") or "photo",
            is_reel=bool(d.get("is_reel", False)),
            caption=_str(d, "caption"),
            taken_at=d.get("taken_at"),
            likes=_int(d, "likes"),
            comments=_int(d, "comments"),
            views=_int(d, "views"),
            hashtags=[str(t) for t in d.get("hashtags") or []],
            thumbnail_url=d.get("thumbnail_url"),
            url=d.get("url"),
        )


@dataclass(frozen=True)
class Story:
    id: str
    owner: str = ""
    media_type: str = "photo"
    taken_at: Optional[str] = None
    expires_at: Optional[str] = None
    media_url: Optional[str] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Story":
        return cls(
            id=_str(d, "id"),
            owner=_str(d, "owner"),
            media_type=_str(d, "media_type") or "photo",
            taken_at=d.get("taken_at"),
            expires_at=d.get("expires_at"),
            media_url=d.get("media_url"),
        )


@dataclass(frozen=True)
class Highlight:
    id: str
    title: str = ""
    cover_url: Optional[str] = None
    items: int = 0

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Highlight":
        return cls(id=_str(d, "id"), title=_str(d, "title"), cover_url=d.get("cover_url"), items=_int(d, "items"))


@dataclass(frozen=True)
class Page:
    """One page of a list (a profile's posts or reels, popular reels) and the cursor of the next one."""

    items: List[Post]
    cursor: Optional[str] = None
    has_more: bool = False

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Page":
        return cls(
            items=[Post.from_dict(p) for p in d.get("items") or []],
            cursor=d.get("cursor"),
            has_more=bool(d.get("has_more", False)),
        )


@dataclass(frozen=True)
class Topic:
    """The posts Instagram ranks as popular for a search term, with its related searches."""

    keyword: str
    description: str = ""
    related: List[str] = field(default_factory=list)
    posts: List[Post] = field(default_factory=list)
    cursor: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Topic":
        return cls(
            keyword=_str(d, "keyword"),
            description=_str(d, "description"),
            related=[str(r) for r in d.get("related") or []],
            posts=[Post.from_dict(p) for p in d.get("posts") or []],
            cursor=d.get("cursor"),
            url=d.get("url"),
        )

"""``picmany-viewer`` command line.

    picmany-viewer link https://www.instagram.com/p/C8xYz12AbCd/   # print the PicMany address
    picmany-viewer open @natgeo                                    # open it in your browser
    picmany-viewer profile natgeo                                  # data call: needs an access key
"""

from __future__ import annotations

import argparse
import json
import sys
import webbrowser
from dataclasses import asdict, is_dataclass
from typing import Any, List, Optional

from . import __version__
from .client import PicmanyClient
from .errors import AccessRestrictedError, PicmanyError

_DATA_COMMANDS = (
    ("profile", "username", "profile data of a public account"),
    ("posts", "username", "a public account's posts"),
    ("reels", "username", "a public account's reels"),
    ("stories", "username", "a public account's current stories"),
    ("highlights", "username", "a public account's highlights"),
    ("post", "link_or_shortcode", "data of a post or reel"),
    ("popular", "keyword", "the popular posts for a topic"),
)


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="picmany-viewer",
        description="Open Instagram content on PicMany (https://picmany.com) without an Instagram account.",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("--base-url", default="https://picmany.com", help=argparse.SUPPRESS)
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("link", help="print the PicMany address of an Instagram link, @username or #topic")
    s.add_argument("value", nargs="+")
    s = sub.add_parser("open", help="open the PicMany page in your default browser")
    s.add_argument("value")

    for name, arg, help_ in _DATA_COMMANDS:
        s = sub.add_parser(name, help=f"{help_} (needs an access key)")
        s.add_argument(arg)
        s.add_argument("--open", action="store_true", help="open the PicMany page when the data call is refused")
    s = sub.add_parser("popular-reels", help="popular reels (needs an access key)")
    s.add_argument("--open", action="store_true", help="open the PicMany page when the data call is refused")
    return p


def _plain(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if isinstance(value, list):
        return [_plain(v) for v in value]
    return value


def main(argv: Optional[List[str]] = None) -> int:
    args = _parser().parse_args(argv)
    client = PicmanyClient(base_url=args.base_url)
    try:
        if args.command == "link":
            for v in args.value:
                print(client.url_for(v))
            return 0
        if args.command == "open":
            url = client.url_for(args.value)
            print(url)
            webbrowser.open(url)
            return 0

        calls = {
            "profile": lambda: client.profile(args.username),
            "posts": lambda: client.posts(args.username),
            "reels": lambda: client.reels(args.username),
            "stories": lambda: client.stories(args.username),
            "highlights": lambda: client.highlights(args.username),
            "post": lambda: client.post(args.link_or_shortcode),
            "popular": lambda: client.popular(args.keyword),
            "popular-reels": lambda: client.popular_reels(),
        }
        print(json.dumps(_plain(calls[args.command]()), ensure_ascii=False, indent=2))
        return 0
    except PicmanyError as e:
        print(f"picmany-viewer: {e}", file=sys.stderr)
        if getattr(args, "open", False) and e.web_url:
            webbrowser.open(e.web_url)
        return 3 if isinstance(e, AccessRestrictedError) else 2


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())

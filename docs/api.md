# Python client reference

```python
import picmany_viewer
```

## Links (always available, no network)

### `to_picmany_url(value, base_url="https://picmany.com") -> str`

The PicMany address of an Instagram or PicMany link, `@username`, `username`, `#topic` or any other words (read as a
topic). Raises `InvalidInputError` for anything PicMany has no page for: login and settings pages, direct messages,
place pages, highlight links without a username, and other sites.

```python
to_picmany_url("https://www.instagram.com/natgeo/p/C8xYz12AbCd/?img_index=2")
# 'https://picmany.com/p/C8xYz12AbCd'
to_picmany_url("https://www.instagram.com/explore/tags/StreetFood/")
# 'https://picmany.com/popular/streetfood'
to_picmany_url("#K-Pop")
# 'https://picmany.com/popular/k%20pop'
```

### `resolve(value) -> Target`

The same input as a `Target(kind, path, username, shortcode, keyword)`; `kind` is one of `profile`, `post`, `reel`,
`popular`, `reels`, `page`, `home`. `Target.url(base_url)` gives the full address.

Usernames follow Instagram's rules (lower case letters, digits, `.` and `_`, at most 30 characters). Topics are folded
the way picmany.com folds them: lower case, hyphens and runs of spaces become one space.

## Data client (closed)

### `PicmanyClient(api_key=None, base_url="https://picmany.com", timeout=15.0)`

| Method | Returns |
|---|---|
| `url_for(value)` | `str`, same as `to_picmany_url` (works without a key) |
| `profile(username)` | `Profile` |
| `posts(username, cursor=None)` | `Page` of `Post` |
| `reels(username, cursor=None)` | `Page` of `Post` |
| `stories(username)` | `list` of `Story` |
| `highlights(username)` | `list` of `Highlight` |
| `post(link_or_shortcode)` | `Post` (post or reel) |
| `popular(keyword, cursor=None)` | `Topic` |
| `popular_reels(cursor=None)` | `Page` of `Post` |

PicMany has no open data API. The data methods behave as follows:

- **No key** (`api_key` unset and no `PICMANY_API_KEY` in the environment): `AccessRestrictedError` is raised and **no
  request is sent**.
- **With a key**: the request is sent to `https://picmany.com/api/v1/…`; the refusal (HTTP 401, 403, 404, 410) raises
  `AccessRestrictedError` with `status` set.

Every error from a data call carries `web_url`, the same content on picmany.com:

```python
from picmany_viewer import PicmanyClient, PicmanyError
import webbrowser

try:
    PicmanyClient().stories("natgeo")
except PicmanyError as e:
    webbrowser.open(e.web_url)  # https://picmany.com/natgeo
```

## Errors

| Exception | When |
|---|---|
| `PicmanyError` | Base class; `web_url` is the page on picmany.com when known |
| `InvalidInputError` (also a `ValueError`) | Input is not a link, username, shortcode or topic this package understands |
| `AccessRestrictedError` | Data access refused; `status` is the HTTP status, or `None` when nothing was sent |
| `RateLimitedError` | HTTP 429; `retry_after` in seconds when given |
| `ServiceError` | Network error, other HTTP error, or a body that is not a JSON object |

## Command line

| Command | Does |
|---|---|
| `picmany-viewer link VALUE...` | Print PicMany addresses |
| `picmany-viewer open VALUE` | Open the PicMany page in the default browser |
| `picmany-viewer profile USERNAME [--open]` | Data call (exit code 3 when refused; `--open` opens the page instead) |
| `picmany-viewer posts USERNAME [--open]` | 〃 |
| `picmany-viewer reels USERNAME [--open]` | 〃 |
| `picmany-viewer stories USERNAME [--open]` | 〃 |
| `picmany-viewer highlights USERNAME [--open]` | 〃 |
| `picmany-viewer post LINK_OR_SHORTCODE [--open]` | 〃 |
| `picmany-viewer popular KEYWORD [--open]` | 〃 |
| `picmany-viewer popular-reels [--open]` | 〃 |

Exit codes: `0` success, `2` invalid input or other error, `3` data access refused.

`python -m picmany_viewer …` works the same way.

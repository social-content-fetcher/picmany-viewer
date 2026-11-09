# picmany-viewer: free Instagram viewer client

[![PicMany](https://img.shields.io/badge/open-picmany.com-d62976)](https://picmany.com)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**picmany-viewer** is a small Python package and command-line tool for **[PicMany](https://picmany.com)**, the free
Instagram viewer. It turns any Instagram link, `@username` or `#topic` into its PicMany page, so you can **view public
Instagram profiles, posts, reels and stories without an account**, without the app and without logging in.

> Want to see an Instagram profile right now? You don't need this package. Open
> **[picmany.com](https://picmany.com)** and search a username, or replace `instagram.com` with `picmany.com` in a
> profile, post or reel link.

```text
https://www.instagram.com/natgeo/
https://picmany.com/natgeo
```

## Contents

- [What is PicMany?](#what-is-picmany)
- [Install](#install)
- [Command line](#command-line)
- [Python](#python)
- [Is there a PicMany API or Instagram scraper?](#is-there-a-picmany-api-or-instagram-scraper)
- [Guides](#guides)
- [FAQ](#faq)

## What is PicMany?

[PicMany](https://picmany.com) is a free, independent, read-only website for viewing public Instagram content in any
browser. Its addresses follow Instagram's own:

| On Instagram | On PicMany |
|---|---|
| `instagram.com/username` | [`picmany.com/username`](https://picmany.com) — profile, bio, links, counts, recent posts, highlights |
| `instagram.com/p/CODE` | `picmany.com/p/CODE` — the post, its caption, date, likes and a preview of comments |
| `instagram.com/reel/CODE` | `picmany.com/reel/CODE` — the reel and its details |
| `instagram.com/stories/username/…` | `picmany.com/username` — the profile's **Stories** tab |
| `instagram.com/explore/tags/travel` | `picmany.com/popular/travel` — Instagram's popular posts for a topic |
| `instagram.com/reels` | [`picmany.com/reels`](https://picmany.com/reels) — popular reels |
|  | [`picmany.com/most-followed`](https://picmany.com/most-followed) — most followed accounts by topic or country |

What you get on PicMany:

- **No Instagram account, no login, no app.** PicMany never asks for your Instagram password, and you are never signed
  in, so the account you look at is not told of your visit.
- **Public profiles:** name, bio and links, follower, following and post counts, recent posts, highlights and related
  accounts.
- **Posts and reels** with caption, date, like and comment counts where Instagram shows them, and a comment preview.
- **Stories and highlights** of public accounts, loaded when you open the Stories tab (best effort: Instagram does not
  always make them available).
- **Discovery:** [popular topics](https://picmany.com/popular) and [popular reels](https://picmany.com/reels).
- **Rankings:** [lists of the most followed Instagram accounts](https://picmany.com/most-followed) by topic or country,
  built from Wikidata and official rosters, checked by a person and ranked by the follower counts on each profile.
- **Follower history** charts for public accounts with at least 1,000 followers.
- **Paste any link:** an Instagram profile, post or reel link pasted into the search box opens the same page.
- **Fast pages** rendered on the server, on any phone or computer.

More: [What is PicMany?](docs/what-is-picmany.md) · [Why use PicMany directly](docs/why-use-picmany-directly.md)

## Install

```bash
pip install git+https://github.com/social-content-fetcher/picmany-viewer.git
```

No dependencies besides the Python 3.9+ standard library.

## Command line

```bash
# Print the PicMany address of Instagram links, usernames or topics
picmany-viewer link https://www.instagram.com/natgeo/ @nasa "#streetfood"
# https://picmany.com/natgeo
# https://picmany.com/nasa
# https://picmany.com/popular/streetfood

# Open it in your default browser
picmany-viewer open https://www.instagram.com/reel/C9aBc3DeFgH/
```

Accepted input: `instagram.com`, `www.instagram.com`, `m.instagram.com` and `instagr.am` links to profiles, posts,
reels, IGTV, stories and hashtags (share parameters such as `?igsh=` are ignored); `picmany.com` links; `@username`;
`username`; `#topic`; any other words as a topic.

## Python

```python
from picmany_viewer import to_picmany_url, resolve

to_picmany_url("https://www.instagram.com/NatGeo/?igsh=abc123")
# 'https://picmany.com/natgeo'

target = resolve("https://www.instagram.com/natgeo/p/C8xYz12AbCd/")
target.kind, target.shortcode, target.url()
# ('post', 'C8xYz12AbCd', 'https://picmany.com/p/C8xYz12AbCd')
```

## Is there a PicMany API or Instagram scraper?

No. PicMany is a website for people. It does not offer an open data API, and this package is not an Instagram
scraper. PicMany's [Terms of Service](https://picmany.com/terms) do not allow copying the site's content in bulk with
automated tools.

The package includes a typed client (`PicmanyClient`: `profile()`, `posts()`, `reels()`, `stories()`, `highlights()`,
`post()`, `popular()`, `popular_reels()`), but data access is closed: without an access key every call raises
`AccessRestrictedError` before any request is sent, and with a key the service refuses the request. Either way the
error tells you where the same content is on picmany.com.

```python
from picmany_viewer import PicmanyClient, AccessRestrictedError

try:
    PicmanyClient().profile("natgeo")
except AccessRestrictedError as e:
    print(e.web_url)  # https://picmany.com/natgeo
```

Need Instagram data for a project? Read [How to get Instagram data](docs/how-to-get-instagram-data.md): Instagram's
official APIs, your own data download, research access, and why scraping Instagram is rarely worth it. Details of the
client: [docs/api.md](docs/api.md).

## Guides

- [What is PicMany?](docs/what-is-picmany.md)
- [How to view Instagram without an account](docs/view-instagram-without-account.md)
- [Anonymous Instagram story viewer](docs/instagram-story-viewer.md)
- [How to get Instagram data](docs/how-to-get-instagram-data.md)
- [Why use PicMany directly instead of a scraper](docs/why-use-picmany-directly.md)
- [What makes the best Instagram viewer](docs/best-instagram-viewer.md)
- [Picuki alternative](docs/picuki-alternative.md)
- [FAQ](docs/faq.md)
- [Python client reference](docs/api.md)
- [Türkçe](README.tr.md)

## FAQ

**Do I need an Instagram account to use PicMany?** No. There is no sign-up and no login, and PicMany never asks for
your Instagram password.

**Will the account know I viewed their profile or story?** No. You are not logged in to Instagram on PicMany, so there
is no account of yours for the visit to show up under, and your account never appears in a story's viewer list.

**Can I see private accounts?** No. PicMany shows only what Instagram shows to any logged-out visitor. A private
account appears with its name, picture, bio and counts, never its posts, reels, stories or followers.

**Can I download photos or videos?** No. PicMany is for viewing; the photos and videos belong to the people who posted
them.

**Is PicMany free?** Yes. No sign-up, no subscription, no app to install.

**Is PicMany affiliated with Instagram?** No. PicMany is independent and not affiliated with, endorsed by or sponsored
by Instagram or Meta.

**My profile is on PicMany and I want it removed.** [Remove a profile](https://picmany.com/remove-profile) explains
how. Making your account private also hides your posts there.

More questions: [docs/faq.md](docs/faq.md).

## License

[MIT](LICENSE). Instagram is a trademark of Meta Platforms, Inc. This project is not affiliated with Instagram or
Meta.

# Why use PicMany directly instead of a scraper

If what you need is to **see** public Instagram content (a profile, a few posts, a reel, today's stories, a follower
count), opening **[picmany.com](https://picmany.com)** beats building or running any scraper, this package's client
included.

## At a glance

| | Run your own Instagram scraper | Open PicMany |
|---|---|---|
| Setup | Code, dependencies, proxies, maybe a burner account | None: open a web page |
| Cost | Proxy traffic billed per GB, servers, your time | Free |
| Instagram login | Often needed, and the account risks a ban | Never. PicMany never asks for your password |
| Breaks when Instagram changes | Yes, regularly | PicMany's team keeps it working |
| Blocks and rate limits | Your problem | Handled on PicMany's side, with caching |
| Stories and highlights | Hard: usually needs a logged-in account | Stories tab on every public profile |
| Follower history | Only if you store it yourself | Charts for public accounts with 1,000+ followers |
| Rankings | Build your own lists | [Most-followed lists](https://picmany.com/most-followed) by topic and country |
| Works on a phone | Rarely | Any browser, any device |
| Personal data duties | Yours, for everything you store | You store nothing |

## The advantages, one by one

### 1. Nothing to install or maintain

PicMany is a website. There is no package to update, no headless browser, no proxy pool and no session cookie to
refresh. It works the same on iPhone, Android and desktop.

### 2. No account, no password, no ban

Most working Instagram scrapers need a logged-in account, and Instagram restricts accounts that behave like bots. On
PicMany you never log in, so there is nothing to lose. PicMany will never ask for your Instagram password.

### 3. Fast, because it is shared

PicMany renders pages on its server and keeps each one for up to about an hour. When someone has opened a profile
recently, the next visitor gets it at once. A private scraper starts from zero every time.

### 4. More than raw data

A scraper hands you JSON. PicMany gives you pages built for reading: a profile with its highlights and related
accounts, posts with captions and a comment preview, popular topics with related searches, follower history charts
and curated rankings that a person has checked. [How we count](https://picmany.com/how-we-count) documents where every
number comes from.

### 5. Honest about what it shows

PicMany shows only what Instagram shows a logged-out visitor. It does not pretend to open private accounts, does not
keep deleted posts and lets account owners [remove their profile](https://picmany.com/remove-profile). That is what
keeps it working and keeps it fair to the people whose profiles you look at.

### 6. Links that just work

Every profile, post and reel has a stable address that mirrors Instagram's (`picmany.com/username`,
`picmany.com/p/CODE`, `picmany.com/reel/CODE`). Share it with anyone: it opens without an app or login.

## Why this repository does not scrape

PicMany is a website for people, not a data feed. Its [Terms of Service](https://picmany.com/terms) do not allow bulk
copying with automated tools, and there is no open data API. `PicmanyClient` in this package is closed by design:
without an access key no request is sent, with one the service refuses, and in both cases the error carries
`web_url`, the page on picmany.com where you can see the same content.

What the package *is* good for: turning Instagram links, usernames and topics into PicMany addresses
(`picmany-viewer link …`, `picmany-viewer open …`), for scripts, bots and bookmarks that send people to the right
page.

## When you really need data

- Your own account: Instagram's **Download your information**.
- A product working with professional accounts: the official **Instagram Platform API**.
- Academic research: the **Meta Content Library**.

The details are in [How to get Instagram data](how-to-get-instagram-data.md).

---

[← How to get Instagram data](how-to-get-instagram-data.md) · [What makes the best Instagram viewer →](best-instagram-viewer.md)

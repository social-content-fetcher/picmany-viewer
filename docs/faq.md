# PicMany FAQ

## Using PicMany

**What is PicMany?**
A free, read-only website for viewing public Instagram profiles, posts, reels, stories and highlights without an
Instagram account. See [What is PicMany?](what-is-picmany.md)

**Do I need an Instagram account?**
No. There is no sign-up and no login, and PicMany never asks for your Instagram password.

**Do I need to install anything?**
No. PicMany works in any browser on iPhone, Android, Windows, macOS and Linux. No app, no extension.

**Is it free?**
Yes, completely.

**How do I open an Instagram link on PicMany?**
Paste it into the search box on [picmany.com](https://picmany.com), or replace `instagram.com` with `picmany.com` in a
profile, post or reel link. From a terminal: `picmany-viewer open <link>`.

**How do I see someone's stories?**
Open their profile on PicMany and use the **Stories** tab. See
[Anonymous Instagram story viewer](instagram-story-viewer.md).

**Can I browse popular posts and reels?**
Yes: [popular topics](https://picmany.com/popular), [popular reels](https://picmany.com/reels) and
[most-followed rankings](https://picmany.com/most-followed).

## Privacy

**Will the account know I viewed their profile or story?**
No. You are not logged in to Instagram on PicMany, so there is no account of yours for the visit to show up under, and
you never appear in a story's viewer list.

**What does PicMany know about me?**
There are no accounts on PicMany and no advertising trackers. Visits are counted with Google Analytics. The
[Privacy Policy](https://picmany.com/privacy) lists everything that is processed.

**Does Instagram see my visit?**
Instagram never sees an account of yours. Photos come through PicMany's own address; when you play a video or story,
your browser loads it from Instagram's servers, like any embedded video.

## What PicMany shows

**Can I see private accounts?**
No. PicMany shows only what Instagram shows to any logged-out visitor. A private account appears with its name,
picture, bio and counts, never its posts, reels, stories or followers. Sites that claim otherwise are scams.

**Can I download photos, videos or stories?**
No. PicMany is for viewing.

**Why is a count on PicMany different from Instagram?**
Pages are kept for up to about an hour so they open quickly, so a count can be up to an hour behind Instagram, now and
then a little more when Instagram is slow to answer. [How we count](https://picmany.com/how-we-count) explains every
number.

**A profile or its stories did not load. Why?**
The account may be private, renamed or deleted, or Instagram may be slow to answer. Stories are best effort: try again
a little later.

**Does PicMany keep deleted posts?**
No. PicMany is not an archive. A post or account deleted on Instagram disappears from PicMany too, normally within
about an hour.

**Can I browse places or locations?**
No. Instagram stopped showing place pages to logged-out visitors in October 2026, so PicMany removed its location
pages.

## Account owners

**My profile is on PicMany. Can I remove it?**
Yes. [Remove a profile](https://picmany.com/remove-profile) explains how. Making your account private also hides your
posts on PicMany, as it does everywhere else.

**Is PicMany affiliated with Instagram or Meta?**
No. PicMany is an independent website, not affiliated with, endorsed by or sponsored by Instagram or Meta.

## Developers

**Does PicMany have an API?**
No open data API. PicMany is a website for people, and its [Terms of Service](https://picmany.com/terms) do not allow
bulk copying with automated tools. This package's data client is closed and points you to the page on picmany.com;
the link helpers work offline. See [Python client reference](api.md) and
[How to get Instagram data](how-to-get-instagram-data.md).

**Is this package an Instagram scraper?**
No. It converts Instagram links, usernames and topics into PicMany addresses. It does not fetch Instagram.

**How do I contact PicMany?**
Write to [info@picmany.com](mailto:info@picmany.com), or see the [contact page](https://picmany.com/contact).

---

[← Picuki alternative](picuki-alternative.md) · [Python client reference →](api.md)

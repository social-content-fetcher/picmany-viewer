# How to get Instagram data

"Getting Instagram data" means different things. Pick the route by what you actually need:

| You want to… | Best route |
|---|---|
| **Look at** a public profile, post, reel or story | [PicMany](https://picmany.com): open it in your browser, no account |
| Get **your own** posts, messages, followers and activity | Instagram's *Download your information* |
| Manage and measure **your own professional** account in an app | Instagram Platform API (official) |
| Read basic data of **other business or creator** accounts | Business Discovery in the Instagram Platform API |
| Study public content **as a researcher** | Meta Content Library and its API |
| Embed a public post on your website | Instagram's embed button or oEmbed |

## 1. Just looking: use a viewer

Most people who search for an "Instagram scraper" only want to see a profile, check a follower count or watch a
story. That needs no code: open **[picmany.com](https://picmany.com)**, search a username or paste a link. PicMany also
charts the follower history of public accounts with at least 1,000 followers and publishes
[most-followed rankings](https://picmany.com/most-followed), which covers many "I need numbers" cases too.

## 2. Your own data: Download your information

Instagram lets every account holder export their own data: posts, stories, comments, likes, messages, followers and
following, in **HTML or JSON**. In the app or on the web go to **Settings → Accounts Center → Your information and
permissions → Download your information**. The export is prepared in the background and you get a notification when
it is ready.

## 3. Official APIs: the Instagram Platform

Meta's official APIs work with **professional accounts** (Business or Creator) and require a Meta developer app,
permissions and, for most uses, App Review.

- **Instagram API with Instagram Login:** an app can publish content, manage comments and messages, and read insights
  for the professional accounts that log in to it.
- **Instagram API with Facebook Login:** the same for professional accounts linked to a Facebook Page, plus:
  - **Business Discovery:** basic profile data and media of *other* Business and Creator accounts;
  - **Hashtag Search:** recent and top public media for a hashtag, with a limit on how many hashtags an account can
    query per week.
- **Personal accounts have no official API anymore.** The Instagram Basic Display API was shut down on
  **4 December 2024**.

Official access is limited, but it is stable, documented and allowed.

## 4. Research access: Meta Content Library

Researchers at qualified academic and non-profit institutions can apply for the **Meta Content Library** and its API,
which give search access to public content on Facebook and Instagram. It replaced CrowdTangle, which Meta shut down in
August 2024.

## 5. Embedding

To show a public post on your own site, use the **Embed** option on the post, or Instagram's oEmbed endpoint through a
Meta app. Embeds stay up to date and respect the owner's choices: a deleted post disappears from the embed too.

## 6. What about scraping Instagram?

Writing your own Instagram scraper is possible in theory and rarely worth it in practice:

- **Terms:** Instagram's Terms of Use forbid collecting information in an automated way without permission, and
  accounts used for scraping get restricted or banned.
- **Login walls and blocks:** logged-out access is limited and rate-limited, and data-center IPs are blocked quickly.
  Getting around that means paid residential proxies, and the cost is charged per gigabyte.
- **Constant breakage:** the internal endpoints and page structure change without notice, so a scraper that works this
  week may return nothing next week.
- **Personal data law:** profiles are personal data. Storing and processing them in bulk falls under laws such as the
  GDPR in the EU and KVKK in Turkey, whatever the technical route.
- **Third-party sites are not an API either.** Viewer sites, PicMany included, are built for people. PicMany's
  [Terms of Service](https://picmany.com/terms) do not allow copying its content in bulk with automated tools, and it
  offers no open data API. This repository's `PicmanyClient` is closed for the same reason: its data calls point you
  to the page on picmany.com instead of returning data.

If you need a handful of profiles, open them on PicMany. If you need your own account's data, download it. If you
need data at scale for a product, use the official APIs; for research, apply for the Content Library.

---

[← Anonymous Instagram story viewer](instagram-story-viewer.md) · [Why use PicMany directly →](why-use-picmany-directly.md)

# How to view Instagram without an account

You can view any **public** Instagram profile, post, reel or story without an Instagram account. The easiest way is
an Instagram viewer such as **[PicMany](https://picmany.com)**, which needs no login, no app and no sign-up.

## Option 1: Search on PicMany (fastest)

1. Open **[picmany.com](https://picmany.com)** on your phone or computer.
2. Type the **username** (for example `natgeo` or `@natgeo`) or a **topic** (for example `street food`) into the
   search box.
3. The profile opens with its bio, counts, recent posts and highlights. Use the **Reels** and **Stories** tabs for the
   rest.

Nothing to install, nothing to sign in to.

## Option 2: Change the link

Got an Instagram link? Replace `instagram.com` with `picmany.com`:

```text
https://www.instagram.com/natgeo/              →  https://picmany.com/natgeo
https://www.instagram.com/p/C8xYz12AbCd/       →  https://picmany.com/p/C8xYz12AbCd
https://www.instagram.com/reel/C9aBc3DeFgH/    →  https://picmany.com/reel/C9aBc3DeFgH
```

Or paste the whole Instagram link into PicMany's search box: profile, post and reel links open the same page on
PicMany, and share parameters such as `?igsh=` are ignored.

With this package installed you can do the same from a terminal:

```bash
picmany-viewer open "https://www.instagram.com/natgeo/?igsh=abc123"
```

## Option 3: instagram.com in a browser

Instagram shows logged-out visitors a limited view of public profiles and asks them to log in after a few posts or
taps. That is enough for a quick look, but not for scrolling a profile, opening stories or seeing reels comfortably.

## Option 4: Search engines

Searching `username instagram` on Google or Bing often finds the profile, on Instagram or on PicMany. PicMany's profile
pages are built to be found this way, so the result opens without a login.

## What you can and cannot see without an account

| | Without an account (PicMany) |
|---|---|
| Public profile: bio, links, counts | ✅ |
| Public posts and reels | ✅ |
| Public stories and highlights | ✅ when Instagram makes them available |
| Follower history of large public accounts | ✅ (accounts with at least 1,000 followers) |
| Private accounts' posts, stories, followers | ❌ Nobody can show these without the owner's approval |
| Liking, commenting, following, messaging | ❌ PicMany is read-only |

## Is it anonymous?

You are not logged in, so there is no Instagram account of yours for the visit to show up under. The account you look
at is not told of your visit, and you never appear in a story's viewer list. When you play a video, your browser loads
it from Instagram's servers, like any embedded video. Details: [About PicMany](https://picmany.com/about) and the
[Privacy Policy](https://picmany.com/privacy).

## Watch out for fake "private Instagram viewers"

Sites that promise to show **private** accounts, ask for your Instagram password, or make you complete a survey or
"human verification" before showing anything are scams. A real viewer shows only public content and never asks for a
login. See [What makes the best Instagram viewer](best-instagram-viewer.md).

---

[← What is PicMany?](what-is-picmany.md) · [Anonymous Instagram story viewer →](instagram-story-viewer.md)

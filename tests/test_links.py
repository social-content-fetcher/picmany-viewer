import unittest

from picmany_viewer import InvalidInputError, resolve, to_picmany_url


class LinkTests(unittest.TestCase):
    def test_instagram_links(self):
        cases = {
            "https://www.instagram.com/NatGeo/": "https://picmany.com/natgeo",
            "https://www.instagram.com/natgeo/?igsh=abc123&utm_source=qr": "https://picmany.com/natgeo",
            "instagram.com/natgeo": "https://picmany.com/natgeo",
            "https://m.instagram.com/_u/natgeo": "https://picmany.com/natgeo",
            "https://instagr.am/natgeo": "https://picmany.com/natgeo",
            "https://www.instagram.com/p/C8xYz12AbCd/": "https://picmany.com/p/C8xYz12AbCd",
            "https://www.instagram.com/natgeo/p/C8xYz12AbCd/?img_index=2": "https://picmany.com/p/C8xYz12AbCd",
            "https://www.instagram.com/tv/B1aB2cD3eF4/": "https://picmany.com/p/B1aB2cD3eF4",
            "https://www.instagram.com/reel/C9aBc3DeFgH/": "https://picmany.com/reel/C9aBc3DeFgH",
            "https://www.instagram.com/reels/C9aBc3DeFgH/": "https://picmany.com/reel/C9aBc3DeFgH",
            "https://www.instagram.com/reels/": "https://picmany.com/reels",
            "https://www.instagram.com/stories/natgeo/3456789012345678901/": "https://picmany.com/natgeo",
            "https://www.instagram.com/explore/tags/Street-Food/": "https://picmany.com/popular/street%20food",
            "https://www.instagram.com/": "https://picmany.com/",
            "https://picmany.com/natgeo": "https://picmany.com/natgeo",
            "https://www.picmany.com/p/C8xYz12AbCd": "https://picmany.com/p/C8xYz12AbCd",
            "https://picmany.com/most-followed/footballers": "https://picmany.com/most-followed/footballers",
        }
        for value, want in cases.items():
            with self.subTest(value=value):
                self.assertEqual(to_picmany_url(value), want)

    def test_shorthands(self):
        self.assertEqual(to_picmany_url("@NASA"), "https://picmany.com/nasa")
        self.assertEqual(to_picmany_url("cristiano"), "https://picmany.com/cristiano")
        self.assertEqual(to_picmany_url("leo.messi"), "https://picmany.com/leo.messi")
        self.assertEqual(to_picmany_url("#Travel"), "https://picmany.com/popular/travel")
        self.assertEqual(to_picmany_url("İstanbul"), "https://picmany.com/popular/istanbul")
        self.assertEqual(to_picmany_url("united nations"), "https://picmany.com/popular/united%20nations")
        self.assertEqual(to_picmany_url("@natgeo", "http://localhost:3002/"), "http://localhost:3002/natgeo")

    def test_kinds(self):
        self.assertEqual(resolve("https://www.instagram.com/reel/C9aBc3DeFgH/").kind, "reel")
        self.assertEqual(resolve("https://www.instagram.com/reel/C9aBc3DeFgH/").shortcode, "C9aBc3DeFgH")
        self.assertEqual(resolve("@natgeo").username, "natgeo")
        self.assertEqual(resolve("#k-pop").keyword, "k pop")

    def test_rejected(self):
        for value in (
            "",
            "@",
            "#",
            "@" + "a" * 31,
            "@bad..name",
            "@about",
            "https://www.instagram.com/accounts/login/",
            "https://www.instagram.com/direct/inbox/",
            "https://www.instagram.com/explore/locations/212988663/berlin-germany/",
            "https://www.instagram.com/stories/highlights/17912345678901234/",
            "https://example.com/natgeo",
            "https://notinstagram.com/natgeo",
        ):
            with self.subTest(value=value):
                with self.assertRaises(InvalidInputError):
                    to_picmany_url(value)


if __name__ == "__main__":
    unittest.main()

import io
import os
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock
from urllib.error import HTTPError

from picmany_viewer import AccessRestrictedError, InvalidInputError, PicmanyClient, ServiceError
from picmany_viewer.cli import main


def _refusing_opener(code):
    calls = []

    def opener(req, timeout):
        calls.append(req)
        raise HTTPError(req.full_url, code, "refused", hdrs=None, fp=None)

    return opener, calls


class _Html:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self):
        return b"<!doctype html><title>PicMany</title>"


class ClientTests(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.dict(os.environ, {}, clear=False)
        patcher.start()
        os.environ.pop("PICMANY_API_KEY", None)
        self.addCleanup(patcher.stop)

    def test_no_key_sends_nothing(self):
        opener, calls = _refusing_opener(200)
        client = PicmanyClient(opener=opener)
        for call, want in (
            (lambda: client.profile("NatGeo"), "https://picmany.com/natgeo"),
            (lambda: client.posts("natgeo"), "https://picmany.com/natgeo"),
            (lambda: client.reels("natgeo"), "https://picmany.com/natgeo"),
            (lambda: client.stories("natgeo"), "https://picmany.com/natgeo"),
            (lambda: client.highlights("natgeo"), "https://picmany.com/natgeo"),
            (lambda: client.post("https://www.instagram.com/p/C8xYz12AbCd/"), "https://picmany.com/p/C8xYz12AbCd"),
            (lambda: client.post("https://www.instagram.com/reel/C9aBc3DeFgH/"), "https://picmany.com/reel/C9aBc3DeFgH"),
            (lambda: client.post("C8xYz12AbCd"), "https://picmany.com/p/C8xYz12AbCd"),
            (lambda: client.popular("#travel"), "https://picmany.com/popular/travel"),
            (lambda: client.popular_reels(), "https://picmany.com/reels"),
        ):
            with self.assertRaises(AccessRestrictedError) as ctx:
                call()
            self.assertEqual(ctx.exception.web_url, want)
            self.assertIsNone(ctx.exception.status)
        self.assertEqual(calls, [])

    def test_refused_with_key(self):
        for code in (401, 403, 404, 410):
            opener, calls = _refusing_opener(code)
            client = PicmanyClient(api_key="k", opener=opener)
            with self.assertRaises(AccessRestrictedError) as ctx:
                client.profile("someone")
            self.assertEqual(ctx.exception.status, code)
            self.assertEqual(ctx.exception.web_url, "https://picmany.com/someone")
            self.assertEqual(calls[0].full_url, "https://picmany.com/api/v1/users/someone")
            self.assertEqual(calls[0].get_header("Authorization"), "Bearer k")

    def test_key_from_environment(self):
        opener, calls = _refusing_opener(404)
        with mock.patch.dict(os.environ, {"PICMANY_API_KEY": "env-key"}):
            client = PicmanyClient(opener=opener)
        with self.assertRaises(AccessRestrictedError):
            client.popular("street food", cursor="abc")
        self.assertEqual(calls[0].full_url, "https://picmany.com/api/v1/popular/street%20food?cursor=abc")

    def test_html_answer_is_an_error_with_the_page(self):
        client = PicmanyClient(api_key="k", opener=lambda req, timeout: _Html())
        with self.assertRaises(ServiceError) as ctx:
            client.post("C8xYz12AbCd")
        self.assertEqual(ctx.exception.web_url, "https://picmany.com/p/C8xYz12AbCd")

    def test_post_rejects_profiles(self):
        with self.assertRaises(InvalidInputError):
            PicmanyClient().post("https://www.instagram.com/natgeo/")

    def test_url_for(self):
        self.assertEqual(PicmanyClient().url_for("https://www.instagram.com/x/"), "https://picmany.com/x")


class CliTests(unittest.TestCase):
    def test_link(self):
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(main(["link", "https://www.instagram.com/natgeo/", "#cats"]), 0)
        self.assertEqual(out.getvalue().split(), ["https://picmany.com/natgeo", "https://picmany.com/popular/cats"])

    def test_data_command_points_to_site(self):
        err = io.StringIO()
        with mock.patch.dict(os.environ, {"PICMANY_API_KEY": ""}), redirect_stderr(err):
            self.assertEqual(main(["profile", "natgeo"]), 3)
        self.assertIn("https://picmany.com/natgeo", err.getvalue())

    def test_invalid_input(self):
        err = io.StringIO()
        with redirect_stderr(err):
            self.assertEqual(main(["link", "https://www.instagram.com/accounts/login/"]), 2)


if __name__ == "__main__":
    unittest.main()

"""Shortener response regression tests without importing the live bot runtime."""
import importlib.util
import logging
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "bot" / "helper" / "ext_utils" / "shortener_utils.py"

# Load the real utility module with lightweight package stubs. Importing bot
# normally starts the Telegram clients and optional services, which unit tests
# must not do.
PACKAGE = "shortener_test_pkg"
root_pkg = ModuleType(PACKAGE)
root_pkg.__path__ = []
root_pkg.LOGGER = logging.getLogger("shortener_test")
root_pkg.shortener_dict = {}

core_pkg = ModuleType(f"{PACKAGE}.core")
core_pkg.__path__ = []
config_module = ModuleType(f"{PACKAGE}.core.config_manager")


class FakeConfig:
    settings = {}
    PROTECTED_API = ""

    @classmethod
    def get(cls, key):
        return cls.settings.get(key, "")


config_module.Config = FakeConfig
helper_pkg = ModuleType(f"{PACKAGE}.helper")
helper_pkg.__path__ = []
ext_utils_pkg = ModuleType(f"{PACKAGE}.helper.ext_utils")
ext_utils_pkg.__path__ = []
cloudscraper_module = ModuleType("cloudscraper")
cloudscraper_module.create_scraper = lambda: None

with patch.dict(
    sys.modules,
    {
        PACKAGE: root_pkg,
        f"{PACKAGE}.core": core_pkg,
        f"{PACKAGE}.core.config_manager": config_module,
        f"{PACKAGE}.helper": helper_pkg,
        f"{PACKAGE}.helper.ext_utils": ext_utils_pkg,
        "cloudscraper": cloudscraper_module,
    },
):
    spec = importlib.util.spec_from_file_location(
        f"{PACKAGE}.helper.ext_utils.shortener_utils", MODULE_PATH
    )
    shortener = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = shortener
    spec.loader.exec_module(shortener)


class FakeResponse:
    def __init__(self, payload=None, text="", json_error=False, content_type="text/plain", status=200):
        self.payload = payload
        self.text = text
        self.json_error = json_error
        self.headers = {"Content-Type": content_type}
        self.status_code = status

    def json(self):
        if self.json_error:
            raise ValueError("provider response is not JSON")
        return self.payload


class ShortenerResponseTests(unittest.TestCase):
    def setUp(self):
        FakeConfig.settings = {
            "SHORTENER_API_URL": "https://api.example.test/shorten",
            "SHORTENER_API_KEY": "test-secret",
            "SHORTENER_API_METHOD": "GET",
            "SHORTENER_API_KEY_PARAM": "api",
            "SHORTENER_URL_PARAM": "url",
            "SHORTENER_RESPONSE_FIELD": "data.shortUrl",
        }
        FakeConfig.PROTECTED_API = ""

    def test_accepts_plain_https_url_response(self):
        response = FakeResponse(
            text="https://short.example.test/abc",
            json_error=True,
        )
        self.assertEqual(
            shortener._response_json_or_short_url(response, "test provider"),
            "https://short.example.test/abc",
        )

    def test_reads_json_response(self):
        response = FakeResponse(payload={"data": {"shortUrl": "https://short.example.test/abc"}})
        payload = shortener._response_json_or_short_url(response, "test provider")
        self.assertEqual(payload["data"]["shortUrl"], "https://short.example.test/abc")

    def test_rejects_http_short_url(self):
        response = FakeResponse(text="http://short.example.test/abc", json_error=True)
        with self.assertRaisesRegex(ValueError, "non-JSON data"):
            shortener._response_json_or_short_url(response, "test provider")

    def test_custom_provider_accepts_plain_url_body(self):
        response = FakeResponse(
            text="https://short.example.test/abc",
            json_error=True,
        )
        with patch.object(shortener, "_request", return_value=response):
            self.assertEqual(
                shortener._short_url_sync("https://example.com/original"),
                "https://short.example.test/abc",
            )

    def test_invalid_provider_body_does_not_leak_body_or_api_key(self):
        response = FakeResponse(
            text="HTML error with test-secret and private provider details",
            json_error=True,
            content_type="text/html; charset=utf-8",
            status=200,
        )
        with patch.object(shortener, "_request", return_value=response):
            with self.assertRaises(ValueError) as raised:
                shortener._short_url_sync("https://example.com/original")
        self.assertNotIn("test-secret", str(raised.exception))
        self.assertNotIn("private provider details", str(raised.exception))
        self.assertIn("text/html", str(raised.exception))


if __name__ == "__main__":
    unittest.main()

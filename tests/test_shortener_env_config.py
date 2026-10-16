"""Regression tests for private shortener callback environment configuration."""

import os
import unittest
from unittest.mock import patch

from bot.core.config_manager import Config


class ShortenerCallbackEnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.previous = Config.SHORTENER_CALLBACK_SECRET
        Config.SHORTENER_CALLBACK_SECRET = ""

    def tearDown(self):
        Config.SHORTENER_CALLBACK_SECRET = self.previous

    def test_callback_secret_loads_from_environment_but_is_not_listed(self):
        secret = "a" * 64
        with patch.dict(os.environ, {"SHORTENER_CALLBACK_SECRET": secret}, clear=True):
            Config.load_env()

        self.assertEqual(Config.SHORTENER_CALLBACK_SECRET, secret)
        self.assertNotIn("SHORTENER_CALLBACK_SECRET", Config.get_all())


if __name__ == "__main__":
    unittest.main()

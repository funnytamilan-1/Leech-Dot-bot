"""Regression tests for private shortener callback environment configuration."""

import importlib.util
import os
import unittest
from pathlib import Path
from unittest.mock import patch

# Load the manager directly so importing bot/__init__.py cannot start the bot runtime.
MODULE_PATH = Path(__file__).resolve().parents[1] / "bot" / "core" / "config_manager.py"
SPEC = importlib.util.spec_from_file_location("config_manager_shortener_test", MODULE_PATH)
config_manager = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(config_manager)
Config = config_manager.Config


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

    def test_persisted_config_cannot_override_callback_secret(self):
        secret = "c" * 64
        Config.SHORTENER_CALLBACK_SECRET = secret
        with self.assertRaisesRegex(ValueError, "BOT_TOKEN"):
            Config.load_dict({"SHORTENER_CALLBACK_SECRET": "b" * 64})
        self.assertEqual(Config.SHORTENER_CALLBACK_SECRET, secret)


if __name__ == "__main__":
    unittest.main()

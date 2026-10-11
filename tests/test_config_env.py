import importlib.util
import os
import unittest
from pathlib import Path
from unittest.mock import patch

# Load the standalone config manager without importing bot/__init__.py, which
# starts the full Telegram runtime and optional service clients.
MODULE_PATH = Path(__file__).resolve().parents[1] / "bot" / "core" / "config_manager.py"
SPEC = importlib.util.spec_from_file_location("config_manager_under_test", MODULE_PATH)
config_manager = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(config_manager)
Config = config_manager.Config


class ConfigEnvironmentTests(unittest.TestCase):
    def setUp(self):
        Config.BOT_TOKEN = ""
        Config.OWNER_ID = 0
        Config.TELEGRAM_API = 0
        Config.TELEGRAM_HASH = ""

    def test_environment_credentials_override_empty_template(self):
        environment = {
            "BOT_TOKEN": "123456:example-token",
            "OWNER_ID": "123456",
            "TELEGRAM_API": "12345",
            "TELEGRAM_HASH": "example-hash",
        }
        with patch.dict(os.environ, environment, clear=True):
            Config.load()

        self.assertEqual(Config.BOT_TOKEN, environment["BOT_TOKEN"])
        self.assertEqual(Config.OWNER_ID, 123456)
        self.assertEqual(Config.TELEGRAM_API, 12345)
        self.assertEqual(Config.TELEGRAM_HASH, environment["TELEGRAM_HASH"])

    def test_missing_required_credentials_fail_clearly(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "BOT_TOKEN"):
                Config.load()


if __name__ == "__main__":
    unittest.main()

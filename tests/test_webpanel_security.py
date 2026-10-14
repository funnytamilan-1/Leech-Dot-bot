# Web panel security and runtime configuration tests · @Code_Dots.
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


panel_auth = load_module("panel_auth_under_test", "web/panel_auth.py")
runtime_settings = load_module("runtime_settings_under_test", "web/runtime_settings.py")


class WebPanelSecurityTests(unittest.TestCase):
    def test_signed_ticket_only_accepts_allowed_admin(self):
        secret = "test-secret-value-that-is-at-least-32-characters"
        ticket = panel_auth.create_ticket(1001, secret, 120)
        self.assertEqual(panel_auth.verify_ticket(ticket, secret, {1001})["uid"], 1001)
        self.assertIsNone(panel_auth.verify_ticket(ticket, secret, {1002}))
        self.assertIsNone(panel_auth.verify_ticket(ticket, "different-secret-with-enough-length-123", {1001}))

    def test_ticket_tampering_is_rejected(self):
        secret = "test-secret-value-that-is-at-least-32-characters"
        ticket = panel_auth.create_ticket(1001, secret, 120)
        body, signature = ticket.split(".", 1)
        tampered = body[:-1] + ("A" if body[-1] != "A" else "B") + "." + signature
        self.assertIsNone(panel_auth.verify_ticket(tampered, secret, {1001}))

    def test_expired_ticket_is_rejected(self):
        secret = "test-secret-value-that-is-at-least-32-characters"
        with patch.object(panel_auth.time, "time", return_value=1000):
            ticket = panel_auth.create_ticket(1001, secret, 60)
        with patch.object(panel_auth.time, "time", return_value=1061):
            self.assertIsNone(panel_auth.verify_ticket(ticket, secret, {1001}))

    def test_shortener_settings_are_shared_and_bounded(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = str(Path(tmp) / "runtime.json")
            with patch.dict(os.environ, {"LEECH_DOT_RUNTIME_SETTINGS": target}):
                saved = runtime_settings.write_runtime_overrides({
                    "START_SHORTENER_REQUIRED": True,
                    "START_SHORTENER_LINK_TTL": 999999,
                    "START_SHORTENER_SESSION_TTL": 3600,
                })
                self.assertTrue(saved["START_SHORTENER_REQUIRED"])
                self.assertEqual(saved["START_SHORTENER_LINK_TTL"], 86400)
                self.assertEqual(runtime_settings.read_runtime_overrides(), saved)

    def test_admin_id_parser_accepts_owner_and_sudo_users(self):
        self.assertEqual(panel_auth.parse_admin_ids(1001, "1002, 1003,invalid"), {1001, 1002, 1003})

    def test_short_secret_is_rejected(self):
        with self.assertRaises(ValueError):
            panel_auth.create_ticket(1001, "short", 120)

    def test_fast_transfer_settings_are_bounded(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = str(Path(tmp) / "runtime.json")
            with patch.dict(os.environ, {"LEECH_DOT_RUNTIME_SETTINGS": target}):
                saved = runtime_settings.write_runtime_overrides({
                    "USE_HYPER": True,
                    "HYPER_THREADS": 999,
                    "HYPER_PIPELINE": 1,
                    "HYPER_CHUNK": 99999999,
                })
                self.assertTrue(saved["USE_HYPER"])
                self.assertEqual(saved["HYPER_THREADS"], 64)
                self.assertEqual(saved["HYPER_PIPELINE"], 4)
                self.assertEqual(saved["HYPER_CHUNK"], 16777216)

    def test_unknown_runtime_setting_is_rejected(self):
        with self.assertRaises(ValueError):
            runtime_settings.write_runtime_overrides({"BOT_TOKEN": "not-allowed"})


if __name__ == "__main__":
    unittest.main()

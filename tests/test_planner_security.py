"""Regression checks for the planner API's security boundaries.

These source-level checks intentionally avoid importing the live bot/web server,
which initializes external services during import.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = (ROOT / "web" / "wserver.py").read_text(encoding="utf-8")
PLANNER = (ROOT / "web" / "templates" / "planner.html").read_text(encoding="utf-8")


class PlannerSecurityRegressionTests(unittest.TestCase):
    def test_planner_api_requires_telegram_init_data(self):
        self.assertIn('request.headers.get("x-telegram-init-data", "")', SERVER)
        self.assertIn("_verify_telegram_webapp_init_data(init_data, user_id)", SERVER)
        self.assertIn("hmac.compare_digest(supplied_hash, expected_hash)", SERVER)
        self.assertIn("_require_planner_user(request, user_id)", SERVER)

    def test_session_lookup_has_no_cross_session_fallback(self):
        start = SERVER.index("def _find_planner_data(")
        end = SERVER.index('@app.get("/api/planner/data")', start)
        lookup = SERVER[start:end]
        self.assertIn('key = f"{mid}_{user_id}"', lookup)
        self.assertIn('str(data.get("user_id", "")) != user_id', lookup)
        self.assertNotIn("all_sessions", lookup)
        self.assertNotIn("len(all_sessions) == 1", lookup)

    def test_untrusted_filename_is_not_interpolated_into_html(self):
        self.assertNotIn('title="${file}">${file}', PLANNER)
        self.assertIn("filename.textContent = String(file)", PLANNER)
        self.assertIn("filename.title = String(file)", PLANNER)

    def test_mutations_validate_payloads_and_session_file_membership(self):
        self.assertIn("Submitted files do not match this planner session", SERVER)
        self.assertIn("Invalid output filename", SERVER)
        self.assertIn("Invalid JSON request", SERVER)

    def test_service_pin_derivation_uses_a_runtime_secret(self):
        start = SERVER.index("def _derive_pin(")
        end = SERVER.index("\n\ndef _pin_rate_limited", start)
        derive = SERVER[start:end]
        self.assertIn("secret = _BOT_TOKEN or _ACCESS_PASSWORD", derive)
        self.assertNotIn("hmac_new(\n        _PIN_SALT,", derive)


if __name__ == "__main__":
    unittest.main()

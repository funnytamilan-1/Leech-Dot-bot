import unittest
from unittest.mock import patch

from web.panel_auth import create_ticket, parse_admin_ids, verify_ticket


class WebPanelAuthTests(unittest.TestCase):
    def setUp(self):
        self.secret = "test-only-secret-that-is-long-enough-123456789"

    def test_valid_owner_ticket(self):
        ticket = create_ticket(1234, self.secret, 900)
        self.assertEqual(verify_ticket(ticket, self.secret, {1234})["uid"], 1234)

    def test_valid_sudo_ticket(self):
        ticket = create_ticket(5678, self.secret, 900)
        self.assertEqual(verify_ticket(ticket, self.secret, {1234, 5678})["uid"], 5678)

    def test_rejects_non_admin(self):
        ticket = create_ticket(5678, self.secret, 900)
        self.assertIsNone(verify_ticket(ticket, self.secret, {1234}))

    def test_rejects_wrong_secret_and_tampering(self):
        ticket = create_ticket(1234, self.secret, 900)
        self.assertIsNone(verify_ticket(ticket, "another-secret-that-is-long-enough-123", {1234}))
        body, signature = ticket.split(".", 1)
        changed = ("A" if body[0] != "A" else "B") + body[1:] + "." + signature
        self.assertIsNone(verify_ticket(changed, self.secret, {1234}))

    def test_rejects_expired_ticket(self):
        with patch("web.panel_auth.time.time", return_value=1000):
            ticket = create_ticket(1234, self.secret, 60)
        with patch("web.panel_auth.time.time", return_value=1061):
            self.assertIsNone(verify_ticket(ticket, self.secret, {1234}))

    def test_requires_strong_secret(self):
        with self.assertRaises(ValueError):
            create_ticket(1234, "short", 900)

    def test_parses_owner_and_sudo_ids(self):
        self.assertEqual(parse_admin_ids(1234, "5678, 9012,invalid"), {1234, 5678, 9012})


if __name__ == "__main__":
    unittest.main()

"""Regression tests for persistent shortener verification state."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from Code_dot.database import verification


class VerificationDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path_patch = patch.object(
            verification, "DB_PATH", Path(self.temp_dir.name) / "verification.sqlite3"
        )
        self.db_path_patch.start()

    def tearDown(self):
        self.db_path_patch.stop()
        self.temp_dir.cleanup()

    def test_return_token_without_provider_proof_does_not_unlock(self):
        verification.issue_token("user-token", 123, 900)
        self.assertFalse(verification.consume_token("user-token", 123))
        # A later valid provider callback can still prove this pending token.
        self.assertTrue(verification.record_completion_proof("user-token", 123, 900))
        self.assertTrue(verification.consume_token("user-token", 123))
        self.assertFalse(verification.consume_token("user-token", 123))

    def test_proof_and_token_are_bound_to_same_user(self):
        verification.issue_token("user-token", 123, 900)
        self.assertFalse(verification.record_completion_proof("user-token", 456, 900))
        self.assertFalse(verification.consume_token("user-token", 456))
        self.assertTrue(verification.record_completion_proof("user-token", 123, 900))
        self.assertFalse(verification.consume_token("user-token", 456))
        self.assertTrue(verification.consume_token("user-token", 123))

    def test_verified_status_persists_across_database_connections(self):
        verification.mark_verified(123, 900)
        self.assertTrue(verification.is_verified(123))
        self.assertTrue(verification.is_verified(123))

    def test_expired_token_cannot_be_completed(self):
        verification.issue_token("expired-token", 123, 60)
        future = verification.time.time() + 10_000
        with patch.object(verification.time, "time", return_value=future):
            self.assertFalse(verification.record_completion_proof("expired-token", 123, 900))
            self.assertFalse(verification.consume_token("expired-token", 123))


if __name__ == "__main__":
    unittest.main()

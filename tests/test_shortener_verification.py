import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / "Code_dot" / "database" / "verification.py"
SPEC = importlib.util.spec_from_file_location("verification_under_test", MODULE)
verification = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verification)


class VerificationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.patch = patch.object(verification, "DB_PATH", Path(self.tmp.name) / "verify.sqlite3")
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        self.tmp.cleanup()

    def test_redirect_without_proof_is_not_verified(self):
        verification.issue_token("token-a", 111, 900)
        self.assertFalse(verification.consume_token("token-a", 111))
        self.assertFalse(verification.is_verified(111))

    def test_wrong_user_cannot_complete(self):
        verification.issue_token("token-b", 111, 900)
        self.assertFalse(verification.record_completion_proof("token-b", 222, 900))

    def test_completion_proof_is_single_use_and_user_bound(self):
        verification.issue_token("token-c", 111, 900)
        self.assertTrue(verification.record_completion_proof("token-c", 111, 900))
        self.assertFalse(verification.consume_token("token-c", 222))
        self.assertTrue(verification.consume_token("token-c", 111))
        self.assertFalse(verification.consume_token("token-c", 111))

    def test_verified_status_persists_between_connections(self):
        verification.mark_verified(111, 86400)
        self.assertTrue(verification.is_verified(111))


if __name__ == "__main__":
    unittest.main()

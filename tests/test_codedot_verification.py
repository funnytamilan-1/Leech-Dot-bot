# Verification regression tests · @Code_Dots · partner @CodeRips.
import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "Code_dot"
    / "database"
    / "verification.py"
)
SPEC = importlib.util.spec_from_file_location("codedot_verification", MODULE_PATH)
verification = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verification)


class VerificationStoreTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        verification.DB_PATH = Path(self.tempdir.name) / "verification.sqlite3"

    def tearDown(self):
        self.tempdir.cleanup()

    def test_token_is_user_bound_and_one_time(self):
        verification.issue_token("secret-token", 1001, 900)
        self.assertFalse(verification.consume_token("secret-token", 1002))
        # Wrong-user attempts do not consume a valid token.
        self.assertTrue(verification.consume_token("secret-token", 1001))
        self.assertFalse(verification.consume_token("secret-token", 1001))

    def test_verification_expiry_is_persisted(self):
        verification.mark_verified(1001, 900)
        self.assertTrue(verification.is_verified(1001))
        self.assertFalse(verification.is_verified(1002))


if __name__ == "__main__":
    unittest.main()

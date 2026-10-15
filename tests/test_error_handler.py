# Reliability regression tests · @Code_Dots · partner @CodeRips.
import asyncio
import importlib.util
import logging
import sys
import unittest
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "bot"
    / "helper"
    / "ext_utils"
    / "error_handler.py"
)
fake_bot = ModuleType("bot")
fake_bot.LOGGER = logging.getLogger("error_handler_test")
SPEC = importlib.util.spec_from_file_location("error_handler_under_test", MODULE_PATH)
error_handler = importlib.util.module_from_spec(SPEC)
with patch.dict(sys.modules, {"bot": fake_bot}):
    SPEC.loader.exec_module(error_handler)


class CircuitBreakerTests(unittest.TestCase):
    def test_decorator_keeps_failures_between_calls(self):
        operation = "test-persistent-breaker"
        error_handler.error_monitor.circuit_breakers.pop(operation, None)

        @error_handler.circuit_breaker(
            operation, failure_threshold=2, recovery_timeout=60
        )
        async def failing_operation():
            raise ValueError("expected test failure")

        async def run():
            for _ in range(2):
                with self.assertRaises(ValueError):
                    await failing_operation()
            with self.assertRaisesRegex(Exception, "Circuit breaker open"):
                await failing_operation()

        asyncio.run(run())

    def test_half_open_state_allows_only_one_probe(self):
        breaker = error_handler.CircuitBreaker(
            failure_threshold=1, recovery_timeout=0
        )
        breaker.on_failure()

        self.assertTrue(breaker.can_execute())
        self.assertFalse(breaker.can_execute())

        breaker.on_success()
        self.assertTrue(breaker.can_execute())


if __name__ == "__main__":
    unittest.main()

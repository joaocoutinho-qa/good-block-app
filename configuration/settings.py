"""
Central configuration for paths and explicit-wait timeouts.
"""
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The signed XPI allows Firefox to register the content script reliably in CI.
EXTENSION_PATH = os.getenv(
    "EXTENSION_PATH",
    os.path.join(PROJECT_ROOT, "extensions", "good_block-1.0.3.xpi"),
)

# Simple configuration: just set the URL to test and use it directly.
TEST_URL = os.getenv("TEST_URL", "www.facebook.com")

# Timeouts in seconds used by BasePage explicit waits.
DEFAULT_TIMEOUT = 10
SHORT_TIMEOUT = 5
BLOCKED_PAGE_TIMEOUT = 20

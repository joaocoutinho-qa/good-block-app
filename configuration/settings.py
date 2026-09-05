"""
Central configuration for paths and explicit-wait timeouts.
"""
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_env_file():
    """Load default environment variables from a local .env file when present."""
    env_path = os.path.join(PROJECT_ROOT, ".env")
    if not os.path.exists(env_path):
        return

    with open(env_path, encoding="utf-8") as env_file:
        for line in env_file:
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file()

# The signed XPI allows Firefox to register the content script reliably in CI.
EXTENSION_PATH = os.getenv(
    "EXTENSION_PATH",
    os.path.join(PROJECT_ROOT, "extensions", "good_block-1.0.3.xpi"),
)

# Test data kept in env so the suite can be reused across machines and CI.
FACEBOOK_DOMAIN = os.getenv("FACEBOOK_DOMAIN", "www.facebook.com")
FACEBOOK_URL = os.getenv("FACEBOOK_URL", f"https://{FACEBOOK_DOMAIN}/")
WORK_GROUP = os.getenv("WORK_GROUP", "Work")

# Timeouts in seconds used by BasePage explicit waits.
DEFAULT_TIMEOUT = 10
SHORT_TIMEOUT = 5
BLOCKED_PAGE_TIMEOUT = 20

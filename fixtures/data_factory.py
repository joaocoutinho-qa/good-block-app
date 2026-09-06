"""Helpers for generating unique test data without external dependencies."""
import uuid


def create_unique_group_name(prefix="good-block"):
    """Return a unique group name suitable for isolated parallel runs."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"

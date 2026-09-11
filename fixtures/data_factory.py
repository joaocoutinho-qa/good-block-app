"""Helpers for generating unique test data without external dependencies."""
import uuid

from configuration import settings


class DataFactory:
    """Factory for creating Good Block test groups and related metadata."""

    @staticmethod
    def create_unique_group_name(prefix="good-block"):
        """Return a unique group name suitable for isolated parallel runs."""
        return f"{prefix}-{uuid.uuid4().hex[:8]}"

    @staticmethod
    def create_group(page, group_name=None, sites=None):
        """Create a valid group on the page and attach metadata for the test."""
        if group_name is None:
            group_name = DataFactory.create_unique_group_name()
        if sites is None:
            sites = [settings.TEST_URL]

        page.create_group(group_name, sites)
        page.verify_group_is_enabled(group_name)

        for site in sites:
            page.verify_group_has_saved_site(group_name, site)

        page.group_name = group_name
        page.sites = list(sites)
        page.set_current_page(page)
        return page


def create_unique_group_name(prefix="good-block"):
    """Backward-compatible wrapper for the unique group name generator."""
    return DataFactory.create_unique_group_name(prefix)


def create_group(page, group_name=None, sites=None):
    """Create a default Good Block group without using pytest fixtures."""
    return DataFactory.create_group(page, group_name=group_name, sites=sites)

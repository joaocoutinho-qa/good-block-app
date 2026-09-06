"""Reusable Good Block fixtures and helpers for test scenarios."""
import pytest
from configuration import settings
from pages.base_page import BasePage
from pages.good_block_page import GoodBlockPage


def _site_for_good_block(url):
    return url.removeprefix("https://").removeprefix("http://").rstrip("/")


@pytest.fixture
def create_group_data():
    """Build unique group data for each test without duplicating setup."""

    def _factory(prefix="good-block", sites=None):
        from fixtures.data_factory import create_unique_group_name

        resolved_sites = list(sites or [_site_for_good_block(settings.TEST_URL)])
        return {
            "group_name": create_unique_group_name(prefix),
            "sites": resolved_sites,
        }

    return _factory


@pytest.fixture
def open_good_block_extension(driver):
    """Open the Good Block popup extension."""
    uuid_value = BasePage.discover_extension_uuid(driver)
    return GoodBlockPage(driver, uuid_value).open()


@pytest.fixture
def create_group(open_good_block_extension):
    """Create a group in Good Block extension before each scenario."""

    def _factory(group_name, sites=None):
        resolved_sites = list(sites or [_site_for_good_block(settings.TEST_URL)])
        open_good_block_extension.create_group(group_name, resolved_sites)
        open_good_block_extension.verify_group_is_enabled(group_name)
        for site in resolved_sites:
            open_good_block_extension.verify_group_has_saved_site(group_name, site)
        return open_good_block_extension

    return _factory

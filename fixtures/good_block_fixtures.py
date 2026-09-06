"""Reusable Good Block fixtures and helpers for test scenarios."""
import pytest
from configuration import settings
from pages.base_page import BasePage
from pages.good_block_page import GoodBlockPage

@pytest.fixture
def group_data_factory():
    """Build unique group data for each test without duplicating setup."""

    def _factory(prefix="good-block", sites=None):
        from fixtures.data_factory import unique_group_name

        resolved_sites = list(sites or [settings.FACEBOOK_DOMAIN])
        return {
            "group_name": unique_group_name(prefix),
            "sites": resolved_sites,
        }
    
    return _factory

@pytest.fixture
def good_block_page(driver):
    """Open the Good Block popup for the current Firefox profile."""
    uuid_value = BasePage.discover_extension_uuid(driver)
    return GoodBlockPage(driver, uuid_value).open()

@pytest.fixture
def ready_group_page(good_block_page):
    """Create and validate a group before each scenario-specific assertion."""

    def _factory(group_name, sites=None):
        resolved_sites = list(sites or [settings.FACEBOOK_DOMAIN])
        good_block_page.create_group(group_name, resolved_sites)
        good_block_page.verify_group_is_enabled(group_name)
        for site in resolved_sites:
            good_block_page.verify_group_has_saved_site(group_name, site)
        return good_block_page

    return _factory

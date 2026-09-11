"""Reusable Good Block fixtures and helpers for test scenarios."""
import pytest
from pages.base_page import BasePage
from pages.good_block_page import GoodBlockPage


@pytest.fixture
def good_block_app(driver):
    """Open the Good Block popup extension."""
    uuid_value = BasePage.discover_extension_uuid(driver)
    return GoodBlockPage(driver, uuid_value).open()
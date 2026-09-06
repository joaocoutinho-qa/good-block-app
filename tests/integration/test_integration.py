"""Integration tests for Good Block rule and persistence behavior."""
import os

import allure
import pytest
from pages.base_page import BasePage
from pages.good_block_page import GoodBlockPage

FACEBOOK_DOMAIN = os.getenv("FACEBOOK_DOMAIN", "www.facebook.com")
FACEBOOK_URL = os.getenv("FACEBOOK_URL", f"https://{FACEBOOK_DOMAIN}/")
WORK_GROUP = os.getenv("WORK_GROUP", "Work")


@pytest.fixture
def good_block_page(driver):
    """Open the Good Block popup for the current Firefox profile."""
    uuid = BasePage.discover_extension_uuid(driver)
    return GoodBlockPage(driver, uuid).open()


@allure.parent_suite("Good Block")
@allure.suite("Integration coverage")
@allure.feature("Rule and persistence checks")
@allure.title("TC03 - Allow access for disabled category")
def test_TC03_allow_access_for_disabled_category(driver, good_block_page):
    """TC03: Allow Access for Disabled Category"""
    # Arrange
    good_block_page.create_group(WORK_GROUP, [FACEBOOK_DOMAIN])
    good_block_page.verify_group_is_enabled(WORK_GROUP)
    good_block_page.verify_group_has_saved_site(WORK_GROUP, FACEBOOK_DOMAIN)
    # Act
    good_block_page.toggle_group(WORK_GROUP).go_to(FACEBOOK_URL)
    # Assert
    good_block_page.verify_site_is_not_blocked()


@allure.parent_suite("Good Block")
@allure.suite("Integration coverage")
@allure.feature("Rule and persistence checks")
@allure.title("TC05 - Propagate URL removal to blocking rules")
def test_TC05_propagate_url_removal_to_blocking_rules(driver, good_block_page):
    """TC05: Remove URL from group and validate it is no longer blocked"""
    # Arrange
    good_block_page.create_group(WORK_GROUP, [FACEBOOK_DOMAIN])
    good_block_page.verify_group_is_enabled(WORK_GROUP)
    good_block_page.verify_group_has_saved_site(WORK_GROUP, FACEBOOK_DOMAIN)
    # Act
    good_block_page.remove_site(WORK_GROUP, FACEBOOK_DOMAIN).go_to(FACEBOOK_URL)
    # Assert
    good_block_page.verify_site_is_not_blocked()

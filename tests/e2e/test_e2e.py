"""E2E workflow validation for Good Block."""
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
@allure.suite("E2E workflow")
@allure.feature("Blocking flow")
@allure.title("TC06 - Complete blocking workflow")
def test_TC06_complete_blocking_workflow(driver, good_block_page):
    """TC06: Complete Blocking Workflow"""
    # Arrange
    good_block_page.create_group(WORK_GROUP, [FACEBOOK_DOMAIN])
    good_block_page.verify_group_is_enabled(WORK_GROUP)
    good_block_page.verify_group_has_saved_site(WORK_GROUP, FACEBOOK_DOMAIN)
    # Act
    good_block_page.go_to(FACEBOOK_URL)
    # Assert
    good_block_page.verify_site_is_blocked()
    good_block_page.verify_motivational_message_is_present()

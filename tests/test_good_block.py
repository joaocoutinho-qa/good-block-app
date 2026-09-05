"""End-to-end Good Block acceptance tests."""
import pytest

from configuration import settings
from pages.base_page import BasePage
from pages.good_block_page import GoodBlockPage

FACEBOOK_DOMAIN = settings.FACEBOOK_DOMAIN
FACEBOOK_URL = settings.FACEBOOK_URL
WORK_GROUP = settings.WORK_GROUP
@pytest.fixture
def good_block_page(driver):
    """Open the Good Block popup for the current Firefox profile."""
    uuid = BasePage.discover_extension_uuid(driver)
    return GoodBlockPage(driver, uuid).open()


def test_TC03_allow_access_for_disabled_category(driver, good_block_page):
    """TC03: Allow Access for Disabled Category"""

    # Arrange: Create a group with Facebook as the configured website.
    good_block_page.create_group(WORK_GROUP, [FACEBOOK_DOMAIN])
    good_block_page.verify_group_is_enabled(WORK_GROUP)
    good_block_page.verify_group_has_saved_site(WORK_GROUP, FACEBOOK_DOMAIN)

    # Act: Disable the group and visit Facebook.
    good_block_page.toggle_group(WORK_GROUP).go_to(FACEBOOK_URL)

    # Assert: Facebook remains accessible because its group is disabled.
    good_block_page.verify_site_is_not_blocked()


def test_TC05_propagate_url_removal_to_blocking_rules(driver, good_block_page):
    """TC05: Remove URL from group and validate it is no longer blocked"""

    # Arrange: create a group with Facebook enabled and persisted.
    good_block_page.create_group(WORK_GROUP, [FACEBOOK_DOMAIN])
    good_block_page.verify_group_is_enabled(WORK_GROUP)
    good_block_page.verify_group_has_saved_site(WORK_GROUP, FACEBOOK_DOMAIN)

    # Act: remove the URL from the extension storage and visit the site.
    good_block_page.remove_site(WORK_GROUP, FACEBOOK_DOMAIN).go_to(FACEBOOK_URL)

    # Assert: the site is no longer blocked after the URL removal.
    good_block_page.verify_site_is_not_blocked()


def test_TC06_complete_blocking_workflow(driver, good_block_page):
    """TC06: Complete Blocking Workflow"""

    # Arrange: Create an enabled group with Facebook as the configured website.
    good_block_page.create_group(WORK_GROUP, [FACEBOOK_DOMAIN])
    good_block_page.verify_group_is_enabled(WORK_GROUP)
    good_block_page.verify_group_has_saved_site(WORK_GROUP, FACEBOOK_DOMAIN)

    # Act: Visit Facebook while its configured group is enabled.
    good_block_page.go_to(FACEBOOK_URL)

    # Assert: Good Block displays its modal and motivational message.
    good_block_page.verify_site_is_blocked()
    good_block_page.verify_motivational_message_is_present()

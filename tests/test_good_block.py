"""End-to-end Good Block acceptance tests."""
import pytest

from pages.base_page import BasePage
from pages.good_block_page import GoodBlockPage

FACEBOOK_DOMAIN = "www.facebook.com"
FACEBOOK_URL = f"https://{FACEBOOK_DOMAIN}/"
WORK_GROUP = "Work"


@pytest.fixture
def good_block_page(driver):
    """Open the Good Block popup for the current Firefox profile."""
    uuid = BasePage.discover_extension_uuid(driver)
    return GoodBlockPage(driver, uuid).open()


def test_tc08_allow_access_for_disabled_category(driver, good_block_page):
    """TC08: A website remains accessible when its group is disabled."""

    # Arrange: Create a group with Facebook as the configured website.
    good_block_page.create_group(WORK_GROUP, [FACEBOOK_DOMAIN])
    assert good_block_page.is_group_enabled(WORK_GROUP)
    assert good_block_page.has_saved_site(WORK_GROUP, FACEBOOK_DOMAIN)

    # Act: Disable the group and visit Facebook.
    good_block_page.toggle_group(WORK_GROUP)
    driver.get(FACEBOOK_URL)

    # Assert: Facebook remains accessible because its group is disabled.
    assert good_block_page.is_modal_visible() is False


def test_tc11_complete_blocking_workflow(driver, good_block_page):
    """TC11: An enabled group blocks its configured website."""

    # Arrange: Create an enabled group with Facebook as the configured website.
    good_block_page.create_group(WORK_GROUP, [FACEBOOK_DOMAIN])
    assert good_block_page.is_group_enabled(WORK_GROUP)
    assert good_block_page.has_saved_site(WORK_GROUP, FACEBOOK_DOMAIN)

    # Act: Visit Facebook while its configured group is enabled.
    driver.get(FACEBOOK_URL)

    # Assert: Good Block displays its modal and motivational message.
    assert good_block_page.is_modal_visible()
    assert good_block_page.get_motivational_message() != ""


def test_tc13_disable_category_and_restore_navigation(driver, good_block_page):
    """TC13: Disabling a category restores normal browsing."""

    # Arrange: Create a group with Facebook enabled.
    good_block_page.create_group(WORK_GROUP, [FACEBOOK_DOMAIN])
    assert good_block_page.is_group_enabled(WORK_GROUP)
    assert good_block_page.has_saved_site(WORK_GROUP, FACEBOOK_DOMAIN)

    # Act: Disable the category and revisit the website.
    good_block_page.toggle_group(WORK_GROUP)
    driver.get(FACEBOOK_URL)

    # Assert: the website loads normally after the category is disabled.
    assert good_block_page.is_modal_visible() is False

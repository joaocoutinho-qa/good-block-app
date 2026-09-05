"""End-to-end Good Block acceptance tests."""
import os
import shutil
import tempfile

import pytest
from selenium import webdriver

from conftest import _build_service
from configuration import settings
from pages.base_page import BasePage
from pages.good_block_page import GoodBlockPage

FACEBOOK_DOMAIN = "www.facebook.com"
FACEBOOK_URL = f"https://{FACEBOOK_DOMAIN}/"
WORK_GROUP = "Work"


def _firefox_options(profile_dir):
    """Build a Firefox profile for the extension persistence scenario."""
    options = webdriver.FirefoxOptions()
    profile = webdriver.FirefoxProfile(profile_dir)
    profile.set_preference("xpinstall.signatures.required", False)
    profile.set_preference("extensions.autoDisableScopes", 0)
    profile.set_preference("fission.autostart", False)
    profile.set_preference("fission.autostart.session", False)
    options.profile = profile
    if os.getenv("HEADLESS") == "1":
        options.add_argument("-headless")
    return options


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


def test_tc14_persist_blocking_after_firefox_restart():
    """TC14: The blocking configuration remains active after Firefox restarts."""
    profile_dir = tempfile.mkdtemp(prefix="good-block-tc14-")

    try:
        driver = webdriver.Firefox(
            service=_build_service(),
            options=_firefox_options(profile_dir),
        )
        try:
            driver.install_addon(settings.EXTENSION_PATH, temporary=False)
            page = GoodBlockPage(driver, BasePage.discover_extension_uuid(driver)).open()

            # Arrange: create the group and keep it enabled.
            page.create_group(WORK_GROUP, [FACEBOOK_DOMAIN])
            assert page.is_group_enabled(WORK_GROUP)
            assert page.has_saved_site(WORK_GROUP, FACEBOOK_DOMAIN)
        finally:
            driver.quit()

        restarted_driver = webdriver.Firefox(
            service=_build_service(),
            options=_firefox_options(profile_dir),
        )
        try:
            restarted_page = GoodBlockPage(
                restarted_driver,
                BasePage.discover_extension_uuid(restarted_driver),
            ).open()

            # Act: reopen Firefox and navigate to the blocked site.
            restarted_driver.get(FACEBOOK_URL)

            # Assert: the saved configuration remains active after restart.
            assert restarted_page.is_group_enabled(WORK_GROUP)
            assert restarted_page.has_saved_site(WORK_GROUP, FACEBOOK_DOMAIN)
            assert restarted_page.is_modal_visible()
            assert restarted_page.get_motivational_message() != ""
        finally:
            restarted_driver.quit()
    finally:
        shutil.rmtree(profile_dir, ignore_errors=True)

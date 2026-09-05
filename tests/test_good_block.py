"""
Testes da extensão Good Block via Page Objects.
Estes testes assumem que os seletores placeholder em
pages/good_block_popup_page.py e pages/blocked_page.py já foram
ajustados para o DOM real (veja explore.py).
"""
import pytest

import config
from pages.base_page import BasePage
from pages.good_block_popup_page import GoodBlockPopupPage
from pages.blocked_page import BlockedPage

FACEBOOK_DOMAIN = "www.facebook.com"
FACEBOOK_URL = f"https://{FACEBOOK_DOMAIN}/"


@pytest.fixture
def popup_page(driver):
    uuid = BasePage.discover_extension_uuid(driver)
    return GoodBlockPopupPage(driver, uuid).open()


def test_create_group(popup_page):
    popup_page.create_group("Trabalho", ["facebook.com", "twitter.com"])
    assert popup_page.is_group_present("Trabalho")


def test_toggle_group(popup_page):
    popup_page.create_group("Trabalho", ["facebook.com"])
    popup_page.toggle_group("Trabalho")
    assert popup_page.is_group_enabled("Trabalho") is False


def test_tc11_complete_blocking_workflow(driver, popup_page):
    popup_page.create_group("Trabalho", [FACEBOOK_DOMAIN])
    assert popup_page.is_group_enabled("Trabalho")
    assert popup_page.has_saved_site("Trabalho", FACEBOOK_DOMAIN)
    popup_page.capture_screenshot("before-facebook-navigation")

    driver.get(FACEBOOK_URL)
    blocked = BlockedPage(driver)
    blocked.capture_screenshot("facebook-loaded")

    assert blocked.is_modal_visible()
    blocked.capture_screenshot("good-block-modal-visible")
    assert blocked.get_motivational_message() != ""

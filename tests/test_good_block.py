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


def test_blocked_site_shows_modal(driver, popup_page):
    popup_page.create_group("Trabalho", ["facebook.com"])

    driver.get("https://facebook.com")
    blocked = BlockedPage(driver)

    assert blocked.is_modal_visible()
    assert blocked.get_motivational_message() != ""

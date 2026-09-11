"""Integration tests for Good Block rule and persistence behavior."""
import allure
from configuration import settings
from fixtures.data_factory import DataFactory
from pages.good_block_page import GoodBlockPage

pytestmark = [
    allure.parent_suite("Good Block"),
    allure.suite("Integration Tests"),
]

@allure.title("TC03 - Allow access for disabled category")
def test_03_allow_access_for_disabled_category(good_block_app):
    group = DataFactory.create_group(good_block_app)
    GoodBlockPage.enable_group(group.group_name)
    GoodBlockPage.go_to(f"https://{settings.TEST_URL}")
    GoodBlockPage.verify_site_is_not_blocked_after_load()

@allure.title("TC05 - Check if removing a URL removes the site block.")
def test_05_check_if_removing_a_URL_removes_the_site_block(good_block_app):
    group = DataFactory.create_group(good_block_app)
    GoodBlockPage.remove_site(group.group_name, group.sites[0])
    GoodBlockPage.go_to(f"https://{settings.TEST_URL}")
    GoodBlockPage.verify_site_is_not_blocked_after_load()

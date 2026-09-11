"""E2E workflow validation for Good Block."""
import allure
from configuration import settings
from fixtures.data_factory import DataFactory
from pages.good_block_page import GoodBlockPage

pytestmark = [
    allure.parent_suite("Good Block"),
    allure.suite("End-to-End Tests"),
]

@allure.title("TC01 - Complete blocking workflow")
def test_01_complete_blocking_workflow(good_block_app):
    DataFactory.create_group(good_block_app)
    GoodBlockPage.go_to(f"https://{settings.TEST_URL}")
    GoodBlockPage.verify_site_is_blocked()
    GoodBlockPage.verify_motivational_message_is_present()
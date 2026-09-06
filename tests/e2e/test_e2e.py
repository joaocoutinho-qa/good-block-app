"""E2E workflow validation for Good Block."""
import allure
from configuration import settings

#Define report suite names
pytestmark = [
    allure.suite("End-to-End Tests"),
    allure.feature("Website blocking flow"),
]

@allure.title("TC01 - Complete blocking workflow")
def test_01_complete_blocking_workflow(create_group, create_group_data):
    group = create_group_data(prefix="tc01", sites=[settings.TEST_URL])
    page = create_group(group["group_name"], group["sites"])
    page.go_to(settings.TEST_URL)
    page.verify_site_is_blocked()
    page.verify_motivational_message_is_present()
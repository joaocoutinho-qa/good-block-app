"""E2E workflow validation for Good Block."""
import allure
from configuration import settings

@allure.parent_suite("Good Block - Functional Tests")
@allure.suite("End-to-End Tests")
@allure.feature("Website blocking flow")
@allure.title("TC01 - Complete blocking workflow")
def test_TC01_complete_blocking_workflow(ready_group_page, group_data_factory):
    group = group_data_factory(prefix="TC01", sites=[settings.FACEBOOK_DOMAIN])
    page = ready_group_page(group["group_name"], group["sites"])
    page.go_to(settings.FACEBOOK_URL)
    page.verify_site_is_blocked()
    page.verify_motivational_message_is_present()
"""Integration tests for Good Block rule and persistence behavior."""
import allure
from configuration import settings

pytestmark = [
    allure.parent_suite("Good Block"),
    allure.suite("Integration Tests"),
]

@allure.title("TC03 - Allow access for disabled category")
def test_03_allow_access_for_disabled_category(create_group, create_group_data):
    group = create_group_data(prefix="tc01")
    page = create_group(group["group_name"], group["sites"])
    page.toggle_group(group["group_name"])
    page.go_to(f"https://{settings.TEST_URL}")
    page.verify_site_is_not_blocked()

@allure.title("TC05 - Checks if removing a URL removes the site block.")
def test_05_propagate_url_removal_to_blocking_rules(create_group, create_group_data):
    group = create_group_data(prefix="tc02")
    page = create_group(group["group_name"], group["sites"])
    page.remove_site(group["group_name"], group["sites"][0])
    page.go_to(f"https://{settings.TEST_URL}")
    page.verify_site_is_not_blocked()

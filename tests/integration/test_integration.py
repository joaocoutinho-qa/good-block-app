"""Integration tests for Good Block rule and persistence behavior."""
import allure
from configuration import settings

@allure.parent_suite("Good Block - Functional Tests")
@allure.suite("Integration Tests")
@allure.feature("Rule and persistence checks")
@allure.title("TC01 - Allow access for disabled category")
def test_01_allow_access_for_disabled_category(create_group, create_group_data):
    group = create_group_data(prefix="tc01", sites=[settings.FACEBOOK_DOMAIN])
    page = create_group(group["group_name"], group["sites"])
    page.toggle_group(group["group_name"]).go_to(settings.FACEBOOK_URL)
    page.verify_site_is_not_blocked()

@allure.parent_suite("Good Block - Functional Tests")
@allure.suite("Integration Tests")
@allure.feature("Rule and persistence checks")
@allure.title("TC02 - Propagate URL removal to blocking rules")
def test_02_propagate_url_removal_to_blocking_rules(create_group, create_group_data):
    group = create_group_data(prefix="tc02", sites=[settings.FACEBOOK_DOMAIN])
    page = create_group(group["group_name"], group["sites"])
    page.remove_site(group["group_name"], settings.FACEBOOK_DOMAIN)
    page.go_to(settings.FACEBOOK_URL)
    page.verify_site_is_not_blocked()

"""Integration tests for Good Block rule and persistence behavior."""
import allure
from configuration import settings

@allure.suite("Integration Tests")
@allure.feature("Rule and persistence checks")
@allure.title("TC01 - Allow access for disabled category")
def test_TC01_allow_access_for_disabled_category(ready_group_page,group_data_factory):
    group = group_data_factory(prefix="tc03", sites=[settings.FACEBOOK_DOMAIN])
    page = ready_group_page(group["group_name"], group["sites"])
    page.toggle_group(group["group_name"]).go_to(settings.FACEBOOK_URL)
    page.verify_site_is_not_blocked()

@allure.suite("Integration Tests")
@allure.feature("Rule and persistence checks")
@allure.title("TC02 - Propagate URL removal to blocking rules")
def test_TC02_propagate_url_removal_to_blocking_rules(ready_group_page, group_data_factory):
    group = group_data_factory(prefix="TC02", sites=[settings.FACEBOOK_DOMAIN])
    page = ready_group_page(group["group_name"], group["sites"])
    page.remove_site(group["group_name"], settings.FACEBOOK_DOMAIN)
    page.go_to(settings.FACEBOOK_URL)
    page.verify_site_is_not_blocked()

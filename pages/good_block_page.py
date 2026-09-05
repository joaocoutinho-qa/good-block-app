"""
Page Object for all Good Block user interactions.

It covers the extension popup used to manage blocking groups and the modal
injected over a blocked website.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from configuration import settings
from pages.base_page import BasePage


class GoodBlockPage(BasePage):
    URL_TEMPLATE = "moz-extension://{uuid}/popup.html"

    # Good Block locators
    ADD_GROUP_BUTTON = (By.CSS_SELECTOR, "div[color='green']")
    GROUP_NAME_INPUT = (By.CSS_SELECTOR,"input[placeholder='Group name (no spaces)']")
    CREATE_GROUP_BUTTON = (By.XPATH, "//button[normalize-space()='Add Group']")
    GROUP_SELECT = (By.CSS_SELECTOR, "select")
    GROUP_OPTIONS = (By.CSS_SELECTOR, "select option")
    SITE_INPUT = (By.CSS_SELECTOR,"input[placeholder='link, example: linkname.com']")
    ADD_SITE_BUTTON = (By.XPATH, "//button[normalize-space()='Add Link']")
    GROUP_TOGGLE_SWITCH = (By.CSS_SELECTOR, "input[type='checkbox']")
    GROUP_TOGGLE_LABEL = (By.CSS_SELECTOR, "label[for='checkbox']")
    BLOCKED_MODAL = (By.CSS_SELECTOR, "#modal-root > div")
    MOTIVATIONAL_MESSAGE = (By.XPATH,"//div[@id='modal-root']//h1[contains(., \"Hey, you should't be here\")]")

    def __init__(self, driver, uuid):
        super().__init__(driver)
        self.uuid = uuid

    def open(self):
        """Open the Good Block popup for the installed extension."""
        url = self.URL_TEMPLATE.format(uuid=self.uuid)
        self.driver.get(url)
        return self

    def create_group(self, name, sites):
        """Create a blocking group and add the supplied domains."""
        self.click(self.ADD_GROUP_BUTTON)
        self.fill(self.GROUP_NAME_INPUT, name)
        self.click(self.CREATE_GROUP_BUTTON)

        self.select_group(name)
        for site in sites:
            self.fill(self.SITE_INPUT, site)
            self.click(self.ADD_SITE_BUTTON)
            self._wait_for_saved_site(name, site)
        return self

    def toggle_group(self, name):
        """Toggle the named group and wait until its state is stored."""
        self.select_group(name)
        was_active = self._get_saved_group(name).get("active")
        self.click(self.GROUP_TOGGLE_LABEL)
        self.wait().until(
            lambda _: self._get_saved_group(name).get("active") is not was_active
        )
        return self

    def is_group_enabled(self, name):
        """Return whether the named group's toggle is enabled."""
        self.select_group(name)
        return self.find(self.GROUP_TOGGLE_SWITCH).is_selected()

    def has_saved_site(self, group_name, site):
        """Return whether the domain is persisted in the extension group."""
        return self._get_saved_group(group_name).get("sitesList", []).count(site) == 1

    def select_group(self, name):
        """Select the group after it becomes available in the popup."""
        self.wait().until(
            lambda driver: any(
                name == option.text
                for option in driver.find_elements(*self.GROUP_OPTIONS)
            )
        )
        Select(self.find(self.GROUP_SELECT)).select_by_visible_text(name)
        return self

    def is_modal_visible(self, timeout=settings.BLOCKED_PAGE_TIMEOUT):
        """Return whether Good Block displays its blocked website modal."""
        return self.is_visible(self.BLOCKED_MODAL, timeout=timeout)

    def get_motivational_message(self):
        """Return the heading displayed in the blocked website modal."""
        return self.get_text(
            self.MOTIVATIONAL_MESSAGE,
            timeout=settings.BLOCKED_PAGE_TIMEOUT,
        )

    def _wait_for_saved_site(self, group_name, site):
        """Wait for the extension to persist a domain before navigating away."""
        def is_saved(_):
            group = self._get_saved_group(group_name)
            return group.get("active") and site in group.get("sitesList", [])

        self.wait().until(is_saved)

    def _get_saved_group(self, group_name):
        result = self.driver.execute_async_script(
            """
            const groupName = arguments[0];
            const done = arguments[arguments.length - 1];

            browser.storage.local.get("groups")
                .then(({groups = {}}) => done(groups[groupName] || null))
                .catch(error => done({error: error.message}));
            """,
            group_name,
        )
        if isinstance(result, dict) and "error" in result:
            raise RuntimeError(
                f"Could not read extension storage: {result['error']}"
            )
        return result or {}

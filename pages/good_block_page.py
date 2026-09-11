"""
Page Object for Good Block user interactions.

"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from configuration import settings
from pages.base_page import BasePage

class GoodBlockPage(BasePage):
    URL_TEMPLATE = "moz-extension://{uuid}/popup.html"
    CURRENT_PAGE = None

    @classmethod
    def set_current_page(cls, page):
        """Keep the active page instance for class-level operations."""
        cls.CURRENT_PAGE = page
        return page

    @classmethod
    def get_current_page(cls):
        """Return the page registered by the factory for class-level calls."""
        if cls.CURRENT_PAGE is None:
            raise RuntimeError("No current GoodBlockPage instance registered.")
        return cls.CURRENT_PAGE

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
        self.group_name = None
        self.sites = []

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

    @staticmethod
    def enable_group(name):
        """Toggle the named group and wait until its state is stored."""
        return GoodBlockPage.get_current_page().enable_group_instance(name)

    def enable_group_instance(self, name):
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

    def verify_group_is_enabled(self, name):
        """Assert the named group is enabled."""
        assert self.is_group_enabled(name)
        return self

    def verify_group_has_saved_site(self, group_name, site):
        """Assert the domain is persisted in the named group."""
        assert self.has_saved_site(group_name, site)
        return self

    @staticmethod
    def remove_site(group_name, site):
        """Remove a persisted site from the named group in extension storage."""
        return GoodBlockPage.get_current_page().remove_site_instance(group_name, site)

    def remove_site_instance(self, group_name, site):
        """Remove a persisted site from the named group in extension storage."""
        result = self.driver.execute_async_script(
            """
            const groupName = arguments[0];
            const site = arguments[1];
            const done = arguments[arguments.length - 1];

            browser.storage.local.get("groups")
                .then(({ groups = {} }) => {
                    const group = groups[groupName] || { active: true, sitesList: [] };
                    group.sitesList = (group.sitesList || []).filter(item => item !== site);
                    groups[groupName] = group;
                    return browser.storage.local.set({ groups });
                })
                .then(() => done(true))
                .catch(error => done({ error: error.message }));
            """,
            group_name,
            site,
        )
        if isinstance(result, dict) and "error" in result:
            raise RuntimeError(f"Could not remove site from storage: {result['error']}")
        return self

    @staticmethod
    def go_to(url, page_load_timeout=300):
        """Navigate the browser to a target page with a more tolerant page-load timeout."""
        return GoodBlockPage.get_current_page().go_to_instance(url, page_load_timeout)

    def go_to_instance(self, url, page_load_timeout=30):
        """Navigate the browser to a target page with a more tolerant page-load timeout."""
        self.driver.set_page_load_timeout(page_load_timeout)
        try:
            self.driver.get(url)
        except Exception:
            self.driver.execute_script("window.stop();")
            raise
        return self

    @staticmethod
    def verify_site_is_blocked():
        """Assert that the blocked website modal is visible."""
        return GoodBlockPage.get_current_page().verify_site_is_blocked_instance()

    def verify_site_is_blocked_instance(self):
        """Assert that the blocked website modal is visible."""
        assert self.is_modal_visible()
        return self

    @staticmethod
    def verify_site_is_not_blocked_after_load():
        """Wait for the target page to finish loading and assert the blocker never appeared."""
        return GoodBlockPage.get_current_page().verify_site_is_not_blocked_after_load_instance()

    def verify_site_is_not_blocked_after_load_instance(self, load_timeout=10):
        """Wait for page load and fail fast if the Good Block modal is present."""
        self.wait(load_timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        assert len(self.driver.find_elements(*self.BLOCKED_MODAL)) == 0
        return self

    @staticmethod
    def verify_motivational_message_is_present():
        """Assert the modal message exists and is not empty."""
        return GoodBlockPage.get_current_page().verify_motivational_message_is_present_instance()

    def verify_motivational_message_is_present_instance(self):
        """Assert the modal message exists and is not empty."""
        assert self.get_motivational_message() != ""
        return self

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

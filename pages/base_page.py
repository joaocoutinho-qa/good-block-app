"""
Shared Page Object utilities and extension UUID discovery.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from configuration import settings


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait(self, timeout=settings.DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout)

    def find(self, locator, timeout=settings.DEFAULT_TIMEOUT):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator, timeout=settings.DEFAULT_TIMEOUT):
        element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def fill(self, locator, text, timeout=settings.DEFAULT_TIMEOUT):
        element = self.find(locator, timeout)
        element.clear()
        element.send_keys(text)
        return element

    def is_visible(self, locator, timeout=settings.SHORT_TIMEOUT):
        try:
            self.wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def get_text(self, locator, timeout=settings.DEFAULT_TIMEOUT):
        return self.find(locator, timeout).text

    @staticmethod
    def discover_extension_uuid(
        driver,
        extension_name="Good Block",
        timeout=settings.DEFAULT_TIMEOUT,
    ):
        """Return the UUID assigned to the installed extension by Firefox."""
        extension_id = getattr(driver, "extension_id", None)
        if extension_id:
            return str(extension_id).strip("{}")

        driver.get("about:debugging#/runtime/this-firefox")

        card = WebDriverWait(driver, timeout).until(
            lambda d: next(
                (
                    c
                    for c in d.find_elements(
                        "css selector", "[data-qa-extension-list-item], .card"
                    )
                    if extension_name in c.text
                ),
                None,
            )
        )

        if card is None:
            raise RuntimeError(
                f"Could not find an extension card containing '{extension_name}' "
                "in about:debugging. Confirm the extension was installed."
            )

        manifest_link = card.find_element(
            "css selector", "a[href^='moz-extension://']"
        )
        href = manifest_link.get_attribute("href")
        uuid = href.split("moz-extension://")[1].split("/")[0]
        return uuid

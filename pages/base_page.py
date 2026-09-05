"""
BasePage: utilitários compartilhados por todos os Page Objects
(waits explícitos, clique, preenchimento, visibilidade) e um helper
para descobrir o UUID interno moz-extension:// da extensão via
about:debugging#/runtime/this-firefox.
"""
import os
import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import config


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait(self, timeout=config.DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout)

    def find(self, locator, timeout=config.DEFAULT_TIMEOUT):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator, timeout=config.DEFAULT_TIMEOUT):
        element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        element.click()
        self.capture_screenshot("click")
        return element

    def fill(self, locator, text, timeout=config.DEFAULT_TIMEOUT):
        element = self.find(locator, timeout)
        element.clear()
        element.send_keys(text)
        self.capture_screenshot("fill")
        return element

    def is_visible(self, locator, timeout=config.SHORT_TIMEOUT):
        try:
            self.wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def get_text(self, locator, timeout=config.DEFAULT_TIMEOUT):
        return self.find(locator, timeout).text

    def capture_screenshot(self, action):
        """Salva a tela após uma ação relevante para evidência do teste."""
        index = getattr(self.driver, "action_screenshot_index", 0) + 1
        self.driver.action_screenshot_index = index
        test_name = getattr(self.driver, "action_screenshot_test_name", "action")
        safe_action = re.sub(r"[^a-z0-9]+", "-", action.lower()).strip("-")
        filename = f"{test_name}_{index:02d}_{safe_action}.png"
        path = os.path.join(config.ACTION_SCREENSHOTS_DIR, filename)

        if not self.driver.save_screenshot(path):
            raise RuntimeError(f"Não foi possível salvar o screenshot: {path}")
        print(f"\n[Screenshot da ação salvo]: {path}")
        return path

    @staticmethod
    def discover_extension_uuid(driver, extension_name="Good Block", timeout=config.DEFAULT_TIMEOUT):
        """
        Abre about:debugging#/runtime/this-firefox e procura o card cujo
        nome contenha `extension_name`, retornando o UUID moz-extension://
        usado no Manifest URL exibido na página.

        Útil quando EXTENSION_ID não é conhecido de antemão (a Good Block
        não declara um ID fixo, então o Firefox gera um novo a cada
        instalação temporária).
        """
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
                f"Não encontrei um card de extensão contendo '{extension_name}' "
                "em about:debugging. Confirme se a extensão foi instalada com sucesso."
            )

        manifest_link = card.find_element(
            "css selector", "a[href^='moz-extension://']"
        )
        href = manifest_link.get_attribute("href")
        # href tem o formato: moz-extension://<uuid>/manifest.json
        uuid = href.split("moz-extension://")[1].split("/")[0]
        return uuid

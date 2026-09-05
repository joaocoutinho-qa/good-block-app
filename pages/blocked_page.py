"""
Page Object para o modal de bloqueio injetado pelo content script
(content.js) sobre a página de um site bloqueado, exibindo uma
mensagem motivacional.

"""
from selenium.webdriver.common.by import By

import config
from pages.base_page import BasePage


class BlockedPage(BasePage):
    MODAL_CONTAINER = (By.CSS_SELECTOR, "#modal-root > div")
    MOTIVATIONAL_MESSAGE = (
        By.XPATH,
        "//div[@id='modal-root']//h3[contains(., \"Hey, you should't be here\")]",
    )

    def is_modal_visible(self, timeout=config.BLOCKED_PAGE_TIMEOUT):
        return self.is_visible(self.MODAL_CONTAINER, timeout=timeout)

    def get_motivational_message(self):
        return self.get_text(
            self.MOTIVATIONAL_MESSAGE,
            timeout=config.BLOCKED_PAGE_TIMEOUT,
        )

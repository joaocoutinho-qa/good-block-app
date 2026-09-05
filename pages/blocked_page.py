"""
Page Object para o modal de bloqueio injetado pelo content script
(content.js) sobre a página de um site bloqueado, exibindo uma
mensagem motivacional.

ATENÇÃO: os seletores abaixo são PLACEHOLDERS — ajuste-os após
inspecionar o DOM real com explore.py.
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class BlockedPage(BasePage):
    # --- PLACEHOLDERS: ajustar após inspecionar o DOM real com explore.py ---
    MODAL_CONTAINER = (By.CSS_SELECTOR, "#good-block-modal, .good-block-overlay")
    MOTIVATIONAL_MESSAGE = (By.CSS_SELECTOR, ".good-block-message")
    # --------------------------------------------------------------------

    def is_modal_visible(self, timeout=None):
        kwargs = {"timeout": timeout} if timeout else {}
        return self.is_visible(self.MODAL_CONTAINER, **kwargs)

    def get_motivational_message(self):
        return self.get_text(self.MOTIVATIONAL_MESSAGE)

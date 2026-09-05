"""
Page Object para a tela de popup da extensão Good Block
(moz-extension://<uuid>/popup.html) — onde o usuário cria/gerencia
grupos de sites bloqueados e ativa/desativa cada grupo.

ATENÇÃO: os seletores abaixo são PLACEHOLDERS. O popup.js real é um
bundle Webpack minificado, então não é possível extrair os seletores
reais sem inspecionar o DOM renderizado manualmente. Use o script
explore.py (na raiz do projeto) para abrir o popup, inspecionar a
estrutura real via DevTools, e então substituir os locators abaixo.
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class GoodBlockPopupPage(BasePage):
    URL_TEMPLATE = "moz-extension://{uuid}/popup.html"

    # --- PLACEHOLDERS: ajustar após inspecionar o DOM real com explore.py ---
    ADD_GROUP_BUTTON = (By.XPATH, "//button[contains(text(), 'Add group')]")
    GROUP_NAME_INPUT = (By.CSS_SELECTOR, "input[name='groupName']")
    SITES_TEXTAREA = (By.CSS_SELECTOR, "textarea[name='sites']")
    SAVE_GROUP_BUTTON = (By.XPATH, "//button[contains(text(), 'Save')]")
    GROUP_LIST_ITEM = (By.CSS_SELECTOR, ".group-item")
    GROUP_TOGGLE_SWITCH = (By.CSS_SELECTOR, ".group-item .toggle-switch")
    GROUP_NAME_LABEL = (By.CSS_SELECTOR, ".group-item .group-name")
    # --------------------------------------------------------------------

    def __init__(self, driver, uuid):
        super().__init__(driver)
        self.uuid = uuid

    def open(self):
        url = self.URL_TEMPLATE.format(uuid=self.uuid)
        self.driver.get(url)
        return self

    def create_group(self, name, sites):
        """
        Cria um novo grupo de bloqueio.
        `sites` pode ser uma lista de domínios (ex.: ["facebook.com", "twitter.com"]).
        """
        self.click(self.ADD_GROUP_BUTTON)
        self.fill(self.GROUP_NAME_INPUT, name)
        self.fill(self.SITES_TEXTAREA, "\n".join(sites))
        self.click(self.SAVE_GROUP_BUTTON)
        return self

    def toggle_group(self, name):
        """Ativa/desativa o grupo com o nome informado."""
        group_item = self._find_group_item(name)
        toggle = group_item.find_element(*self.GROUP_TOGGLE_SWITCH)
        toggle.click()
        return self

    def is_group_present(self, name):
        return any(
            name in item.text for item in self.driver.find_elements(*self.GROUP_LIST_ITEM)
        )

    def _find_group_item(self, name):
        for item in self.driver.find_elements(*self.GROUP_LIST_ITEM):
            if name in item.text:
                return item
        raise ValueError(f"Grupo '{name}' não encontrado na lista de grupos.")

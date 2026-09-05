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
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class GoodBlockPopupPage(BasePage):
    URL_TEMPLATE = "moz-extension://{uuid}/popup.html"

    # O popup inicial exibe a criação de grupo como o controle circular "+".
    ADD_GROUP_BUTTON = (By.CSS_SELECTOR, "div[color='green']")
    GROUP_NAME_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='Group name (no spaces)']",
    )
    CREATE_GROUP_BUTTON = (By.XPATH, "//button[normalize-space()='Add Group']")
    GROUP_SELECT = (By.CSS_SELECTOR, "select")
    GROUP_OPTIONS = (By.CSS_SELECTOR, "select option")
    SITE_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='link, example: linkname.com']",
    )
    ADD_SITE_BUTTON = (By.XPATH, "//button[normalize-space()='Add Link']")
    GROUP_TOGGLE_SWITCH = (By.CSS_SELECTOR, "input[type='checkbox']")
    GROUP_TOGGLE_LABEL = (By.CSS_SELECTOR, "label[for='checkbox']")
    # --------------------------------------------------------------------

    def __init__(self, driver, uuid):
        super().__init__(driver)
        self.uuid = uuid

    def open(self):
        url = self.URL_TEMPLATE.format(uuid=self.uuid)
        self.driver.get(url)
        self.capture_screenshot("popup-opened")
        return self

    def create_group(self, name, sites):
        """
        Cria um novo grupo de bloqueio.
        Cria o grupo, seleciona-o e adiciona cada domínio informado.
        """
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
        """Ativa/desativa o grupo com o nome informado."""
        self.select_group(name)
        self.click(self.GROUP_TOGGLE_LABEL)
        return self

    def is_group_enabled(self, name):
        """Retorna o estado do toggle do grupo informado."""
        self.select_group(name)
        return self.find(self.GROUP_TOGGLE_SWITCH).is_selected()

    def has_saved_site(self, group_name, site):
        """Retorna se o link está persistido no grupo ativo da extensão."""
        return self._get_saved_group(group_name).get("sitesList", []).count(site) == 1

    def is_group_present(self, name):
        return any(
            name == option.text for option in self.driver.find_elements(*self.GROUP_OPTIONS)
        )

    def select_group(self, name):
        """Seleciona um grupo depois que ele estiver disponível no popup."""
        self.wait().until(
            lambda driver: any(
                name == option.text
                for option in driver.find_elements(*self.GROUP_OPTIONS)
            )
        )
        Select(self.find(self.GROUP_SELECT)).select_by_visible_text(name)
        self.capture_screenshot("select-group")
        return self

    def _wait_for_saved_site(self, group_name, site):
        """Espera a gravação do link no storage da extensão antes de navegar."""
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
                f"Não foi possível ler o storage da extensão: {result['error']}"
            )
        return result or {}

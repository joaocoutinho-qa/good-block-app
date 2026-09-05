"""
Fixture pytest que fornece uma instância do Firefox com a extensão
Good Block já instalada, pronta para cada teste (escopo "function":
navegador limpo a cada teste).
"""
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

import config


@pytest.fixture(scope="function")
def driver():
    options = webdriver.FirefoxOptions()
    # Extensões exigem modo headed no Firefox; headless pode se comportar
    # de forma inconsistente com WebExtensions.
    # options.add_argument("--headless")  # não usar

    service = FirefoxService(GeckoDriverManager().install())
    firefox_driver = webdriver.Firefox(service=service, options=options)

    # Instala a extensão em tempo de execução, sem popup de confirmação
    # manual. temporary=True permite instalar addons não assinados.
    extension_id = firefox_driver.install_addon(config.EXTENSION_PATH, temporary=True)
    firefox_driver.extension_id = extension_id  # guarda para uso nos testes/pages

    yield firefox_driver

    firefox_driver.quit()

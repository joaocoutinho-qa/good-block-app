"""
Fixture pytest que fornece uma instância do Firefox com a extensão
Good Block já instalada, e tira screenshots automaticamente ao final
de cada teste para visualização na pipeline de CI (GitHub Actions).
"""
import os
import shutil
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService

import config

SCREENSHOTS_DIR = os.path.join(config.BASE_DIR, "screenshots")


def _build_service():
    """
    Usa o geckodriver já instalado no PATH (ex.: instalado pela action
    browser-actions/setup-geckodriver na pipeline de CI). Se não estiver
    disponível (ambiente local), cai para o webdriver-manager, que baixa
    a versão correta automaticamente.
    """
    geckodriver_path = shutil.which("geckodriver")
    if geckodriver_path:
        return FirefoxService(geckodriver_path)

    from webdriver_manager.firefox import GeckoDriverManager
    return FirefoxService(GeckoDriverManager().install())


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook do pytest para capturar o resultado de cada fase do teste (call)."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function")
def driver(request):
    options = webdriver.FirefoxOptions()

    service = _build_service()
    firefox_driver = webdriver.Firefox(service=service, options=options)

    # Instala a extensão em tempo de execução
    extension_id = firefox_driver.install_addon(config.EXTENSION_PATH, temporary=True)
    firefox_driver.extension_id = extension_id

    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    yield firefox_driver

    # Tirar screenshot ao final do teste (tanto para sucesso quanto para falha)
    test_name = request.node.name
    rep_call = getattr(request.node, "rep_call", None)
    status = "FAILED" if (rep_call and rep_call.failed) else "PASSED"
    screenshot_path = os.path.join(SCREENSHOTS_DIR, f"{test_name}_{status}.png")

    try:
        firefox_driver.save_screenshot(screenshot_path)
        print(f"\n[Screenshot salvo]: {screenshot_path}")
    except Exception as e:
        print(f"\n[Erro ao salvar screenshot]: {e}")

    firefox_driver.quit()

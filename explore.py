"""
Script exploratório: abre o Firefox com a extensão Good Block já
instalada e navega até o popup, pausando a execução para você
inspecionar o DOM real no DevTools antes de escrever os seletores
finais nos Page Objects.

Uso:
    python explore.py
"""
from selenium import webdriver

import config
from conftest import _build_service
from pages.base_page import BasePage


def main():
    options = webdriver.FirefoxOptions()
    service = _build_service()
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.install_addon(config.EXTENSION_PATH, temporary=True)

        uuid = BasePage.discover_extension_uuid(driver)
        print(f"UUID da extensão: {uuid}")

        popup_url = f"moz-extension://{uuid}/popup.html"
        driver.get(popup_url)
        print(f"Popup aberto em: {popup_url}")
        print("Abra o DevTools (F12) e inspecione o DOM para descobrir os seletores reais.")

        input("Pressione ENTER aqui no terminal para fechar o navegador...")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

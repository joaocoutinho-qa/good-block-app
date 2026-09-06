"""
Pytest fixtures and evidence helpers for Good Block browser tests.
"""
import os
import shutil
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from configuration import settings

SCREENSHOTS_DIR = os.path.join(settings.PROJECT_ROOT, "screenshots")
DOM_DIR = os.path.join(settings.PROJECT_ROOT, "dom")
DRIVER_LOGS_DIR = os.path.join(settings.PROJECT_ROOT, "driver-logs")

def _build_service(log_output=None):
    """Use geckodriver from PATH when available; otherwise use webdriver-manager."""
    geckodriver_path = shutil.which("geckodriver")
    if geckodriver_path:
        return FirefoxService(
            executable_path=geckodriver_path,
            service_args=["--log", "trace"],
            log_output=log_output,
        )

    from webdriver_manager.firefox import GeckoDriverManager
    return FirefoxService(
        executable_path=GeckoDriverManager().install(),
        service_args=["--log", "trace"],
        log_output=log_output,
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store each pytest phase result for use during fixture teardown."""
    _ = call
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function")
def driver(request):
    options = webdriver.FirefoxOptions()
    options.set_preference("fission.autostart", False)
    options.set_preference("fission.autostart.session", False)
    if os.getenv("HEADLESS") == "1":
        options.add_argument("-headless")
    os.makedirs(DRIVER_LOGS_DIR, exist_ok=True)
    driver_log_path = os.path.join(DRIVER_LOGS_DIR, f"{request.node.name}.log")

    service = _build_service(driver_log_path)
    firefox_driver = webdriver.Firefox(service=service, options=options)

    # Permanent installation makes Firefox register the signed content script.
    firefox_driver.extension_id = firefox_driver.install_addon(
        settings.EXTENSION_PATH,
        temporary=False,
    )

    yield firefox_driver

    # Save browser evidence only when the test setup or test body fails.
    test_name = request.node.name
    rep_setup = getattr(request.node, "rep_setup", None)
    rep_call = getattr(request.node, "rep_call", None)
    if rep_setup and rep_setup.failed:
        status = "ERROR"
    elif rep_call and rep_call.failed:
        status = "FAILED"
    else:
        firefox_driver.quit()
        if os.path.exists(driver_log_path):
            os.remove(driver_log_path)
        if not os.listdir(DRIVER_LOGS_DIR):
            os.rmdir(DRIVER_LOGS_DIR)
        return

    try:
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        os.makedirs(DOM_DIR, exist_ok=True)
        screenshot_path = os.path.join(SCREENSHOTS_DIR, f"{test_name}_{status}.png")
        dom_path = os.path.join(DOM_DIR, f"{test_name}_{status}.html")
        firefox_driver.save_screenshot(screenshot_path)
        with open(dom_path, "w", encoding="utf-8") as dom_file:
            dom_file.write(firefox_driver.page_source)
        print(f"\n[Final screenshot saved]: {screenshot_path}")
        print(f"[DOM saved]: {dom_path}")
    finally:
        firefox_driver.quit()

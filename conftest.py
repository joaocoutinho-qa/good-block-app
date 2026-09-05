"""
Fixture pytest que fornece uma instância do Firefox com a extensão
Good Block já instalada, e tira screenshots automaticamente ao final
de cada teste para visualização na pipeline de CI (GitHub Actions).
"""
import os
import shutil
import subprocess
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService

import config

SCREENSHOTS_DIR = os.path.join(config.BASE_DIR, "screenshots")
DOM_DIR = os.path.join(config.BASE_DIR, "dom")
DRIVER_LOGS_DIR = os.path.join(config.BASE_DIR, "driver-logs")


def _build_service(log_output=None):
    """
    Usa o geckodriver já instalado no PATH (ex.: instalado pela action
    browser-actions/setup-geckodriver na pipeline de CI). Se não estiver
    disponível (ambiente local), cai para o webdriver-manager, que baixa
    a versão correta automaticamente.
    """
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


def _create_action_video(test_name):
    """Converte as capturas sequenciais de um teste em um vídeo MP4."""
    frames = sorted(
        Path(config.ACTION_SCREENSHOTS_DIR).glob(f"{test_name}_*.png")
    )
    if not frames:
        return

    os.makedirs(config.VIDEOS_DIR, exist_ok=True)
    concat_file = Path(config.VIDEOS_DIR, f"{test_name}.txt")
    video_path = Path(config.VIDEOS_DIR, f"{test_name}.mp4")

    with concat_file.open("w", encoding="utf-8", newline="\n") as file:
        for frame in frames:
            file.write(f"file '{frame.resolve().as_posix()}'\n")
            file.write("duration 1\n")
        file.write(f"file '{frames[-1].resolve().as_posix()}'\n")

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-vf",
                "fps=2,format=yuv420p",
                "-movflags",
                "+faststart",
                str(video_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    finally:
        concat_file.unlink(missing_ok=True)

    print(f"\n[Vídeo das ações salvo]: {video_path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook do pytest para capturar o resultado de cada fase do teste (call)."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function")
def driver(request):
    options = webdriver.FirefoxOptions()
    if os.getenv("HEADLESS") == "1":
        options.add_argument("-headless")
    os.makedirs(DRIVER_LOGS_DIR, exist_ok=True)
    driver_log_path = os.path.join(DRIVER_LOGS_DIR, f"{request.node.name}.log")

    service = _build_service(driver_log_path)
    firefox_driver = webdriver.Firefox(service=service, options=options)

    # Instala a extensão em tempo de execução
    firefox_driver.extension_id = firefox_driver.install_addon(
        config.EXTENSION_PATH,
        temporary=True,
    )

    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(config.ACTION_SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(config.VIDEOS_DIR, exist_ok=True)
    os.makedirs(DOM_DIR, exist_ok=True)
    firefox_driver.action_screenshot_index = 0
    firefox_driver.action_screenshot_test_name = request.node.name

    yield firefox_driver

    # Tirar screenshot ao final do teste (tanto para sucesso quanto para falha)
    test_name = request.node.name
    rep_setup = getattr(request.node, "rep_setup", None)
    rep_call = getattr(request.node, "rep_call", None)
    if rep_setup and rep_setup.failed:
        status = "ERROR"
    elif rep_call and rep_call.failed:
        status = "FAILED"
    else:
        status = "PASSED"
    screenshot_path = os.path.join(SCREENSHOTS_DIR, f"{test_name}_{status}.png")
    dom_path = os.path.join(DOM_DIR, f"{test_name}_{status}.html")

    try:
        firefox_driver.save_screenshot(screenshot_path)
        with open(dom_path, "w", encoding="utf-8") as dom_file:
            dom_file.write(firefox_driver.page_source)
        _create_action_video(test_name)
        print(f"\n[Screenshot salvo]: {screenshot_path}")
        print(f"[DOM salvo]: {dom_path}")
    finally:
        firefox_driver.quit()

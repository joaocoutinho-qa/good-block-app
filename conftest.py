"""
Pytest fixtures and evidence helpers for Good Block browser tests.
"""
import os
import platform
import shutil
import subprocess
import time

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService

try:
    import allure
except ImportError:  # pragma: no cover - optional dependency for local runs.
    allure = None

from configuration import settings

SCREENSHOTS_DIR = os.path.join(settings.PROJECT_ROOT, "screenshots")
DOM_DIR = os.path.join(settings.PROJECT_ROOT, "dom")
DRIVER_LOGS_DIR = os.path.join(settings.PROJECT_ROOT, "driver-logs")
VIDEOS_DIR = os.path.join(settings.PROJECT_ROOT, "videos")


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


def _start_video_recording(test_name):
    """Record a short browser session video for every test case."""
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path is None:
        return None

    os.makedirs(VIDEOS_DIR, exist_ok=True)
    video_path = os.path.join(VIDEOS_DIR, f"{test_name}.mp4")
    if os.path.exists(video_path):
        os.remove(video_path)

    system_name = platform.system().lower()
    if system_name == "windows":
        command = [
            ffmpeg_path,
            "-y",
            "-f",
            "gdigrab",
            "-framerate",
            "10",
            "-i",
            "desktop",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            video_path,
        ]
    else:
        display = os.getenv("DISPLAY") or ":99"
        command = [
            ffmpeg_path,
            "-y",
            "-f",
            "x11grab",
            "-draw_mouse",
            "0",
            "-framerate",
            "10",
            "-video_size",
            "1280x720",
            "-i",
            display,
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            video_path,
        ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1)
    return {"process": process, "path": video_path}


def _stop_video_recording(video_recording):
    """Stop the recording and return the video file path if produced."""
    if not video_recording:
        return None

    process = video_recording["process"]
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=10)

    video_path = video_recording["path"]
    return video_path if os.path.exists(video_path) else None


def _attach_video_to_allure(test_name, video_path):
    """Attach a recorded test video to the Allure report when available."""
    if allure is None or not video_path or not os.path.exists(video_path):
        return

    attachment_kind = getattr(
        allure.attachment_type,
        "VIDEO",
        getattr(allure.attachment_type, "MP4", allure.attachment_type.MP4),
    )
    allure.attach.file(
        video_path,
        name=f"{test_name}_video",
        attachment_type=attachment_kind,
        extension="mp4",
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
    video_recording = _start_video_recording(request.node.name)

    service = _build_service(driver_log_path)
    firefox_driver = webdriver.Firefox(service=service, options=options)

    # Permanent installation makes Firefox register the signed content script.
    firefox_driver.extension_id = firefox_driver.install_addon(
        settings.EXTENSION_PATH,
        temporary=False,
    )

    yield firefox_driver

    test_name = request.node.name

    # Save browser evidence for both passing and failing tests.
    rep_setup = getattr(request.node, "rep_setup", None)
    rep_call = getattr(request.node, "rep_call", None)
    if rep_setup and rep_setup.failed:
        status = "ERROR"
    elif rep_call and rep_call.failed:
        status = "FAILED"
    else:
        status = "PASSED"

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

    video_path = _stop_video_recording(video_recording)
    _attach_video_to_allure(test_name, video_path)

    if os.path.exists(driver_log_path):
        os.remove(driver_log_path)
    if not os.listdir(DRIVER_LOGS_DIR):
        os.rmdir(DRIVER_LOGS_DIR)

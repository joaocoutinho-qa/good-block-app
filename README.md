# Good Block Automation

![Tests](https://github.com/joaocoutinho-qa/good-block-app/actions/workflows/tests.yml/badge.svg)

Python + Selenium automation for the Firefox Good Block extension.

## Overview

This project covers the functional test suite for the Firefox Good Block extension using pytest and the Page Object Model.

Current autoamtion test coverage:
- TC01 — Complete blocking workflow
- TC03 — Allow access for a disabled category
- TC05 — Check if removing a URL removes the site block.

The suite is split into:
- `tests/integration` for integration-layer functional checks
- `tests/e2e` for end-to-end workflow validation

## Test scope and selection

This delivery focuses on three critical test cases, selected because a failure in any of them means the extension's core promise (blocking access reliably and configurably) is broken:

- **TC01 — Complete blocking workflow**: validates the full site-blocking flow. If this fails, the app's core purpose is lost.
- **TC03 — Allow access for disabled category**: validates that the toggle actually disables blocking for a specific group of sites. A failure here may require uninstalling the extension.
- **TC05 — Check if removing a URL removes the site block**: validates that removing a site actually disables blocking for that specific site. A failure here may require uninstalling the extension or deleting the group.

Other critical test, not implemented:
- **TC04 - Persist Blocking after Firefox Restart**:  An important scenario to make sure data persistense in the Good Block extension

The full test plan (including cases not automated in this round) and the bug report are available in the project artifacts.

## Project structure

```text
good-block-automation/
├── .github/
│   └── workflows/
│       └── tests.yml
├── configuration/
│   └── settings.py
├── extensions/
│   └── good_block-1.0.3.xpi
├── fixtures/
│   ├── data_factory.py
│   └── good_block_fixtures.py
├── pages/
│   ├── base_page.py
│   └── good_block_page.py
├── tests/
│   ├── conftest.py
│   ├── e2e/
│   │   └── test_e2e.py
│   └── integration/
│       └── test_integration.py
├── .gitignore
├── conftest.py
├── pytest.ini
├── README.md
├── requirements.txt
```

## Requirements

Before running the automation locally, make sure the machine has the following prerequisites:

- Python 3.12+
- Firefox ESR installed. The local setup was validated with Firefox ESR 153.2.0.
- The signed extension file present at:

```text
extensions/good_block-1.0.3.xpi
```

- A clean Firefox installation, without managed or restricted profiles that may block WebDriver sessions.
- geckodriver is optional: the fixture uses a driver from `PATH` when available and otherwise downloads one with `webdriver-manager`.
- Xvfb and ffmpeg are only required for the Linux CI workflow and video/evidence capture.

## Setup (Windows PowerShell)

1. Confirm that Firefox ESR is installed. The package name must be `Mozilla.Firefox.ESR`:

```powershell
winget list --id Mozilla.Firefox.ESR -e
```

If it is not installed, install it with:

```powershell
winget install --id Mozilla.Firefox.ESR -e
```

Confirm the executable version:

```powershell
(Get-Item "C:\Program Files\Mozilla Firefox\firefox.exe").VersionInfo | Select-Object ProductVersion,ProductName
```

The package list should identify `Mozilla Firefox ESR`. A normal Firefox installation may cause recent Firefox versions to block WebDriver access to extension pages.

2. Create and activate the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, allow it only for the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

3. Install the project dependencies inside the activated environment:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. Set the target site. Use only the host name, without `https://`:

```powershell
$env:TEST_URL = "wesper.co"
```

5. Confirm that the signed extension is present:

```text
extensions/good_block-1.0.3.xpi
```

If the `.xpi` was downloaded from the internet and Firefox reports `ERROR_FILE_ACCESS`, unblock the file once:

```powershell
Unblock-File .\extensions\good_block-1.0.3.xpi
```

Do not install the extension manually in your personal Firefox profile. The fixture installs the `.xpi` automatically in an isolated WebDriver profile. The geckodriver service also uses `--allow-system-access`, required by Firefox 153+ to access `about:debugging` and `moz-extension://` pages during automation.

## Run locally

Run the complete suite with the Firefox interface visible:

```powershell
$env:TEST_URL = "wesper.co"
Remove-Item Env:HEADLESS -ErrorAction SilentlyContinue
python -m pytest -vv -s tests/integration tests/e2e
```

Run only the E2E test with the Firefox interface visible:

```powershell
$env:TEST_URL = "wesper.co"
Remove-Item Env:HEADLESS -ErrorAction SilentlyContinue
python -m pytest -vv -s tests/e2e/test_e2e.py
```

Run all tests in headless mode:

```powershell
$env:TEST_URL = "wesper.co"
$env:HEADLESS = "1"
python -m pytest -q tests/integration tests/e2e
```

Run a specific suite:

```powershell
python -m pytest -q tests/integration
python -m pytest -q tests/e2e
```

The first run may download geckodriver through `webdriver-manager` if no `geckodriver` executable is available on `PATH`. The test opens a separate Firefox WebDriver profile, installs `extensions/good_block-1.0.3.xpi` in that profile, and closes the profile after the test.

### Exact Windows sequence

Run these commands in order from the project root:

```powershell
winget list --id Mozilla.Firefox.ESR -e
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
$env:TEST_URL = "wesper.co"
Unblock-File .\extensions\good_block-1.0.3.xpi
Remove-Item Env:HEADLESS -ErrorAction SilentlyContinue
python -m pytest -vv -s tests/integration tests/e2e
```

The last command runs all three tests with the Firefox window visible. To run without the interface, replace the last two commands with:

```powershell
$env:HEADLESS = "1"
python -m pytest -q tests/integration tests/e2e
```

## CI flow

The pipeline is organized in three stages:

1. Setup environment
2. Run `tests/integration` and `tests/e2e` in parallel
3. Merge Allure results and publish the final HTML report

The final artifact is:
- `good-block-report.html`

This is a single-file HTML report that can be opened directly in a browser.

## Failure evidence

When a test fails, the driver fixture saves:
- screenshot
- DOM dump
- geckodriver log

These artifacts are uploaded by the GitHub Actions workflow for debugging.

## Notes

- The root [`conftest.py`](./conftest.py) keeps the Firefox driver setup and evidence handling.
- The shared page and data fixtures live in [`fixtures/`](./fixtures) and are loaded by [`tests/conftest.py`](./tests/conftest.py).
- The report is generated from the merged Allure results and exported as a single HTML file for direct opening.

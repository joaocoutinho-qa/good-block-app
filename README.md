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

Before running the automation locally, make sure the machine has the following prerequisites configured correctly:

- Python 3.12+
- Firefox installed and available on the local system
- geckodriver available on `PATH`
- A clean Firefox installation, without managed or restricted profiles that may block extension installation
- The signed extension file present at:

```text
extensions/good_block-1.0.3.xpi
```

- Optional: Xvfb for headless/browser CI execution

## Setup

1. Create and activate the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Set the target site you want to test:

```powershell
$env:TEST_URL = "wesper.co"
```

4. Ensure the signed extension exists:

```text
extensions/good_block-1.0.3.xpi
```

## Run locally

Run all functional checks:

```powershell
pytest -q tests/integration tests/e2e
```

Run a specific suite:

```powershell
pytest -q tests/integration
pytest -q tests/e2e
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

# Good Block Automation

Python + Selenium automation for the Firefox Good Block extension.

## Overview

This project covers the functional test suite for the Firefox Good Block extension using pytest and the Page Object Model.

Current tests coverage:
- TC03 — allow access for a disabled category
- TC05 — Checks if removing a URL removes the site block.
- TC01 — complete blocking workflow

The suite is split into:
- `tests/integration` for integration-layer functional checks
- `tests/e2e` for end-to-end workflow validation

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
│   ├── __init__.py
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
└── .env.example
```

## Requirements

- Python 3.12+
- Firefox
- geckodriver available on `PATH`
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
$env:TEST_URL = "www.example.com"
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

# Good Block Automation

End-to-end automation for the Firefox **Good Block** extension using Selenium,
geckodriver, pytest, and the Page Object Model.

## Requirements

- Python 3.12 or later
- Firefox
- geckodriver available on `PATH`, or an internet connection so
  `webdriver-manager` can download it

## Setup

1. Create and activate a virtual environment.

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the dependencies.

   ```powershell
   pip install -r requirements.txt
   ```

The signed extension package at
[`extensions/good_block-1.0.3.xpi`](./extensions/good_block-1.0.3.xpi) is
installed into a clean Firefox profile for every test.

## Project structure

```text
configuration/  Test settings and paths
extensions/     Signed Firefox extension package
pages/          Shared browser helpers and the Good Block Page Object
tests/          Acceptance tests
```

## Run the tests

```powershell
pytest -v
```

Each test uses a new Firefox instance through the `driver` fixture in
[`conftest.py`](./conftest.py). The suite covers:

- **TC08:** Facebook stays accessible when the `Work` group is disabled.
- **TC11:** Facebook displays the Good Block modal when the `Work` group is enabled.

## Failure evidence

When a test fails, teardown saves a final screenshot, page DOM, and geckodriver
log. Successful tests do not create evidence files. GitHub Actions uploads
failure evidence as the `test-evidence` artifact.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| `install_addon` reports a signature error | The XPI is missing or corrupt | Restore `extensions/good_block-1.0.3.xpi` and rerun the tests. |
| The popup remains blank | Firefox has not registered the extension | Confirm the XPI installation completed and retry. |
| geckodriver is missing | geckodriver is not on `PATH` | Let `webdriver-manager` download it, or install geckodriver locally. |
| CI is slow or unstable | Firefox needs a display server | The GitHub Actions workflow runs Firefox through Xvfb. |

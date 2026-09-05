# Prompt: Configure Selenium for Firefox Extension Automation (Good Block)

Copy and paste the prompt below into any AI assistant (Claude, ChatGPT, etc.)
to generate a complete Selenium automation project for the Good Block
Firefox extension.

---

## PROMPT

```
I need you to build a complete Selenium WebDriver automation project in
Python to interact with a specific Firefox extension. Follow the
specifications below exactly.

EXTENSION CONTEXT
- Extension name: Good Block
- Mozilla Add-ons (AMO) page: https://addons.mozilla.org/firefox/addon/good-block/
- What it does: blocks websites for the user. Allows creating groups
  with a list of websites, and turning each group on/off independently.
  When a blocked website is visited, a modal appears over the page
  content with a motivational message.
- Main functionality I need to test/automate: creating a group of
  blocked sites, toggling a group on/off, and verifying that visiting
  a blocked site shows the blocking modal with a motivational message.
- Does the extension expose a popup/options page reachable via HTML
  (moz-extension://<id>/somepage.html)? Yes — it has a popup screen
  for managing groups and a content-script-injected modal for blocked
  pages. I don't know the exact HTML structure yet.

TECHNICAL REQUIREMENTS
1. Use Selenium WebDriver with geckodriver (not Playwright, not
   Puppeteer), because I need the install_addon() method to install
   the extension at runtime without manual confirmation popups.
2. Manage geckodriver automatically via webdriver-manager (I don't
   want to download the binary manually).
3. Install the extension with driver.install_addon(xpi_path, temporary=True)
   inside a pytest fixture, scoped to "function" (a clean browser per test).
4. Structure the project using the Page Object Model (POM) pattern:
   - A BasePage with shared utilities (explicit waits via
     WebDriverWait, click, fill, is_visible)
   - One Page Object per relevant screen/feature of the extension
     (at minimum: the popup UI for managing groups, and the blocked-site
     modal)
   - Tests written in pytest that only interact through the Page
     Objects, never calling driver.find_element directly
5. Include a method to discover the extension's internal UUID/ID via
   about:debugging#/runtime/this-firefox, in case I don't know the
   exact ID (search specifically for a card containing "Good Block").
6. Include a separate exploratory script (explore.py) that launches
   Firefox with the extension already installed and pauses execution
   with input(), so I can inspect the extension's real HTML in
   DevTools before writing final selectors.
7. Leave all CSS/XPath selectors as clearly commented placeholders,
   since you don't have access to the real HTML — I will adjust them
   myself after manual inspection.

EXPECTED FILE STRUCTURE
project/
├── requirements.txt
├── config.py              # paths, EXTENSION_ID, timeouts
├── conftest.py            # driver fixture with extension installed
├── explore.py             # manual popup inspection script
├── extensions/            # folder where I place the .xpi
├── pages/
│   ├── base_page.py
│   ├── good_block_popup_page.py
│   └── blocked_page.py
└── tests/
    └── test_good_block.py

DELIVERABLES
1. All project files, complete and commented in English.
2. A README.md with:
   - Step-by-step installation instructions (venv, pip install,
     downloading the .xpi from the AMO link above)
   - How to find the real extension ID from the manifest.json inside
     the .xpi (it's a zip file)
   - How to run the exploratory script to fine-tune the selectors
   - How to run the tests with pytest
   - A troubleshooting table covering the most common issues
     (install_addon failing, blank moz-extension:// page, element not
     found, etc.)
3. Do not invent selectors that look "real" — clearly mark them as
   placeholders to be adjusted, both in code comments and in the README.

CONSTRAINTS
- Do not use browser localStorage/sessionStorage to persist test state.
- Good Block was last updated in 2020 and is Manifest V2 — do not add
  unnecessary Manifest V3 content-script-permission workarounds.
- Run in headed mode (headless=False) by default, since extensions can
  behave inconsistently in Firefox headless mode.
```

---

## Notes

- This prompt is pre-filled for **Good Block** specifically, based on its
  public AMO listing (website blocking with on/off groups).
- The AI generating the project still won't know Good Block's actual
  popup HTML — it will produce placeholder selectors and an
  `explore.py` script for you to inspect the real DOM and finalize them
  yourself, exactly like the project delivered earlier in this
  conversation.
- If you want to reuse this prompt for a *different* extension later,
  swap out the "EXTENSION CONTEXT" section only — the rest applies to
  any Firefox extension automated via Selenium.

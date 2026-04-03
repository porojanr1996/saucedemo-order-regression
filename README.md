# Sauce Demo — order placement regression (Playwright + pytest)

Automated regression tests for the [Sauce Demo](https://www.saucedemo.com/) shopping flow: login, cart, checkout, and order confirmation.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Run

```bash
pytest tests/ -v
```

Optional: run only regression-marked tests:

```bash
pytest tests/ -v -m regression
```

Tests use headless Chromium against the live demo site (`base_url` in `pytest.ini`).

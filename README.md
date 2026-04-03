# Sauce Demo — order placement automation

Regression and E2E tests for [Sauce Demo](https://www.saucedemo.com/): authentication, cart, checkout (step one), overview totals, order confirmation.

## Structure

- `pages/` — Page Object Model, `data-test` selectors
- `flows/order_flow.py` — reusable checkout sequence
- `config/test_data.py` — users, products, expected strings
- Pytest markers: `smoke`, `regression`, `auth`
- Failed tests: PNG under `artifacts/screenshots/` (ignored in git)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

## Run

```bash
pytest tests/ -v
pytest tests/ -v -m smoke
pytest tests/ -v -m "regression and not smoke"
```

Headed (visible browser):

```bash
HEADED=1 pytest tests/test_order_e2e.py::test_smoke_single_item_happy_path -v
```

Video recording:

```bash
PW_VIDEO_DIR=artifacts/videos pytest tests/ -v
```

Base URL: `pytest.ini` → `base_url`.

## Paths

| Path | Purpose |
|------|---------|
| `config/settings.py` | Timeouts |
| `config/test_data.py` | Users, `CustomerInfo`, catalog keys, literals |
| `pages/` | Screen-level page objects |
| `flows/` | Journey helpers |
| `tests/` | Test modules |

## CI

Install browsers in the job, e.g. `playwright install chromium --with-deps` on Linux. `pythonpath = .` in `pytest.ini` resolves `config` and `pages` without a package install.

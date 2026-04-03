# Sauce Demo — order placement automation

End-to-end and regression checks for [Sauce Demo](https://www.saucedemo.com/): login, cart, checkout step one, overview totals, and confirmation.

## What you get

- **Page Object Model** (`pages/`) — UI changes land in one place per screen, not scattered through tests.
- **Thin flows** (`flows/order_flow.py`) — composes pages for the “happy path” without hiding assertions.
- **Central test data** (`config/test_data.py`) — users, product slugs, and expected copy.
- **Pytest markers** — `smoke` vs `regression`, plus `auth` for access-control cases.
- **Failure screenshots** — on assertion failure, a PNG is written under `artifacts/screenshots/` (gitignored).

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

**Headed debugging** (watch the browser):

```bash
HEADED=1 pytest tests/test_order_e2e.py::test_smoke_single_item_happy_path -v
```

**Optional video** (per run):

```bash
PW_VIDEO_DIR=artifacts/videos pytest tests/ -v
```

The target URL is `base_url` in `pytest.ini` (overridable with pytest-base-url’s usual mechanisms if you add them).

## Layout

| Path | Role |
|------|------|
| `config/settings.py` | Timeouts |
| `config/test_data.py` | Users, `CustomerInfo`, catalog keys, message literals |
| `pages/` | One class per major UI state |
| `flows/` | Short user-journey helpers |
| `tests/` | Specs only — no selectors here |

## CI note

Install browsers in the job (`playwright install chromium --with-deps` on Linux). Keep `pythonpath = .` in `pytest.ini` so `config` and `pages` resolve without installing a package.

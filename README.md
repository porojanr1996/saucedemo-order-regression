# Sauce Demo — order placement tests

Playwright + pytest for https://www.saucedemo.com/

## Run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
pytest tests/ -v
```

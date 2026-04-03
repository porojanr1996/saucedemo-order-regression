"""Timeouts and defaults. Tune here instead of scattering magic numbers in tests."""

# Playwright default navigation/action timeout (ms)
NAVIGATION_TIMEOUT_MS = 30_000

# Expect assertions (ms) — slightly above typical SaaS TTFB for flaky-prone checks
EXPECT_TIMEOUT_MS = 15_000

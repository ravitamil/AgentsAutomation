---
applyTo: "tests/e2e/**"
description: "Rules applied strictly when editing or generating end-to-end test spec files."
---

# Path-Specific Instructions: E2E Playwright Tests

When generating or editing files under `tests/e2e/`:
1. Every test file MUST import and instantiate existing Page Objects from `../pages/`.
2. Every test title MUST begin with the Test Case ID (e.g. `test('TC-ORHM-1-01: ...', async () => ...)`).
3. Do not include raw CSS or XPath selectors directly in `tests/e2e/*.spec.ts`. All selectors belong in `tests/pages/`.
4. Ensure all assertions use Playwright's web-first assertions: `await expect(...).toBeVisible()`.

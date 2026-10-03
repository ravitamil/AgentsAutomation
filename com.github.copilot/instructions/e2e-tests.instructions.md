---
applyTo: "src/test/java/com/orangehrm/tests/**"
description: "Rules applied strictly when editing or generating Java Playwright test classes."
---

# Path-Specific Instructions: Java Playwright Tests

When generating or editing files under `src/test/java/com/orangehrm/tests/`:
1. Every test class MUST extend `com.orangehrm.base.BaseTest` to leverage automated Playwright Tracing, console logging, and screenshot capture.
2. Every test class MUST import and instantiate existing Page Objects from `com.orangehrm.pages.*`.
3. Every test method MUST use `@Test` and `@DisplayName("TC-ORHM-X-01: ...")` starting with the Test Case ID.
4. Do not include raw CSS or XPath selectors directly in test classes. All selectors belong encapsulated inside Page Objects.
5. Ensure all assertions use AssertJ (`org.assertj.core.api.Assertions.assertThat`) or Playwright web-first assertions (`com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat`).

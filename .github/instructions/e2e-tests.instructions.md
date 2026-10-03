---
applyTo: "src/test/java/com/orangehrm/tests/**"
description: "Rules applied strictly when editing, authoring, or refactoring Java Playwright test classes."
---

# Java Playwright Test Class Instructions

These rules apply whenever authoring, updating, or reviewing test classes under `src/test/java/com/orangehrm/tests/`.

## 1. Class Structure & BaseTest Inheritance
- Every test class **MUST** extend `com.orangehrm.base.BaseTest`.
- `BaseTest` manages:
  - Playwright browser lifecycle (`Browser`, `BrowserContext`, `Page`).
  - Automated Playwright Tracing (`target/traces/<TestName>-trace.zip`).
  - Browser console logs listener (`target/logs/<TestName>-console.log`).
  - Automated failure screenshots (`target/screenshots/<TestName>-failed.png`).

```java
package com.orangehrm.tests;

import com.orangehrm.base.BaseTest;
import com.orangehrm.pages.LoginPage;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

public class CustomTest extends BaseTest {

    @Test
    @DisplayName("TC-ORHM-1-01: Successful login with valid credentials")
    public void testValidLogin() {
        LoginPage loginPage = new LoginPage(page);
        loginPage.navigate();
        loginPage.login("Admin", "admin123");
        assertThat(loginPage.isDashboardVisible())
                .as("Dashboard should be displayed after login")
                .isTrue();
    }
}
```

## 2. Naming Conventions & Display Names
- Class names must follow the feature or story: `<FeatureName>Test.java` (e.g. `LoginTest.java`, `LeaveTest.java`).
- Every test method must include a descriptive `@DisplayName` prefixed with the formal Test Case ID:
  ```java
  @Test
  @DisplayName("TC-ORHM-4-01: Apply leave with valid balance and future date")
  ```

## 3. Test Isolation & Independent State
- Tests **MUST NEVER** depend on the execution order or side-effects of another test.
- Every test starts with a fresh `BrowserContext` and `Page` instance created in `@BeforeEach`.
- Do not store state in `static` fields across test methods.

## 4. Failure Artifact Recording
- When wrapping assertions or catching exceptions, ensure `markTestFailed()` is called so `BaseTest` archives the trace, console logs, and failure screenshot:
  ```java
  try {
      // test actions & assertions
  } catch (Throwable t) {
      markTestFailed();
      throw t;
  }
  ```

## 5. Assertion Standards
- Use **AssertJ** (`org.assertj.core.api.Assertions.assertThat`) with clear `.as("...")` descriptions:
  ```java
  assertThat(page.title()).as("Page title must match OrangeHRM").isEqualTo("OrangeHRM");
  ```
- Alternatively, use Playwright web assertions (`PlaywrightAssertions.assertThat(locator)...`) for auto-retrying assertions:
  ```java
  PlaywrightAssertions.assertThat(page.getByText("Welcome")).isVisible();
  ```

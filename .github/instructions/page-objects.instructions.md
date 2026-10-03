---
applyTo: "src/main/java/com/orangehrm/pages/**"
description: "Strict architecture and coding rules for authoring Java Playwright Page Object Model (POM) classes."
---

# Java Playwright Page Object Model (POM) Instructions

These rules apply whenever viewing, authoring, or refactoring Page Object classes under `src/main/java/com/orangehrm/pages/`.

## 1. Class Structure & Inheritance
- Every Page Object **MUST** extend `com.orangehrm.pages.BasePage`.
- The constructor **MUST** accept `com.microsoft.playwright.Page` and invoke `super(page);`.
- Initialize all locators in the constructor or declare them as `private final Locator`.

```java
package com.orangehrm.pages;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.options.AriaRole;

public class CustomPage extends BasePage {
    private final Locator submitBtn;
    private final Locator usernameInput;

    public CustomPage(Page page) {
        super(page);
        this.submitBtn = page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Save"));
        this.usernameInput = page.getByPlaceholder("Username");
    }
}
```

## 2. Locator Strategy (Priority Order)
Always prioritize user-facing, accessible locators over brittle DOM selectors:
1. `page.getByRole(AriaRole.<ROLE>, new Page.GetByRoleOptions().setName("..."))`
2. `page.getByPlaceholder("...")`
3. `page.getByLabel("...")`
4. `page.getByText("...", new Page.GetByTextOptions().setExact(true))`
5. Scoped contextual locators: `container.locator(".oxd-select-wrapper")`

### 🚫 STRICTLY FORBIDDEN:
- **Absolute XPaths**: e.g. `/html/body/div[1]/div[1]/div/form/div[2]/button`
- **Volatile Auto-Generated Class Hashes**: e.g. `div._3f89_x`
- **Hardcoded Thread Sleep**: Never use `Thread.sleep()`. Rely on Playwright's auto-waiting locators or explicit `locator.waitFor()`.

## 3. Separation of Concerns (Zero Assertions in Page Objects)
- **DO NOT** place JUnit (`org.junit.jupiter.api.Assertions`) or AssertJ (`org.assertj.core.api.Assertions`) assertions inside Page Objects.
- Page Objects model user workflows and provide state query methods:
  - **Action methods**: `login(user, pass)`, `submitForm()`, `selectDropdownOption(name)`
  - **State query methods**: `boolean isSuccessToastVisible()`, `String getErrorMessageText()`, `int getValidationErrorsCount()`

## 4. Handling Asynchronous UI & Spinners
- OrangeHRM uses AJAX loading spinners (`.oxd-form-loader`, `.oxd-loading-spinner`).
- When navigating or submitting forms, wait for loading overlays to detach before interacting with subsequent inputs:
  ```java
  page.locator(".oxd-form-loader").waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.DETACHED));
  ```

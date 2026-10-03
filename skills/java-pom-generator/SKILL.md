---
name: "java-pom-generator"
description: "Guidelines and templates for designing clean, resilient Page Object Models for Playwright in Java 17+ with JUnit 5."
---

# Java Page Object Model (POM) Generator Skill

Use this skill whenever generating, auditing, or refactoring Page Object classes for Java Playwright test automation.

## Core Design Principles
1. **Single Responsibility**: Each Page Object represents a single page or distinct reusable UI component (e.g., `NavbarComponent`, `LeavePage`, `LoginPage`).
2. **Encapsulation**:
   - Locators (`Locator`) are private or protected fields initialized in constructor using `page.getByRole(...)`, `page.getByLabel(...)`, or `page.getByPlaceholder(...)`.
   - Never expose raw Playwright locators directly to tests; expose intent-based action methods (e.g., `login(username, password)`, `applyLeave(...)`).
3. **Inheritance**:
   - All Page Objects extend `BasePage` (`com.orangehrm.pages.BasePage`).
4. **State Queries vs Assertions**:
   - Page Objects must **NEVER** contain JUnit/AssertJ assertions.
   - Return booleans, element text, or counts (e.g., `isUserLoggedIn()`, `getErrorMessageText()`, `getRequiredErrorsCount()`) and let the test class assert against them.

---

## Standard Java Playwright POM Template

```java
package com.orangehrm.pages;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.options.AriaRole;

/**
 * Page Object representing OrangeHRM Feature Page.
 */
public class FeaturePage extends BasePage {

    // Locators
    private final Locator pageHeading;
    private final Locator inputField;
    private final Locator submitButton;
    private final Locator successToast;
    private final Locator errorMessage;

    public FeaturePage(Page page) {
        super(page);
        this.pageHeading = page.getByRole(AriaRole.HEADING, new Page.GetByRoleOptions().setLevel(6));
        this.inputField = page.getByPlaceholder("Enter value");
        this.submitButton = page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Save"));
        this.successToast = page.locator(".oxd-toast--success");
        this.errorMessage = page.locator(".oxd-input-field-error-message");
    }

    public void navigate() {
        page.navigate("/web/index.php/feature/view");
    }

    public void enterValueAndSubmit(String value) {
        inputField.fill(value);
        submitButton.click();
    }

    public boolean isSuccessToastVisible() {
        return successToast.isVisible();
    }

    public String getErrorMessageText() {
        return errorMessage.innerText();
    }
}
```

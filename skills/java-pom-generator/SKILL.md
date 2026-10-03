---
name: "pom-generator"
description: "Guidelines and templates for designing clean, resilient Page Object Models for Playwright in TypeScript."
---

# Page Object Model Generator Skill

Use this skill whenever generating or refactoring Page Objects for web test automation.

## Design Rules
1. **Single Responsibility**: Each Page Object should represent one page or a well-defined reusable component (e.g. Navigation Bar, Modal, Table).
2. **Encapsulation**:
   - Internal locators should be private or exposed via descriptive getters.
   - Action methods should model user intents (`applyForLeave(data)`), not low-level clicks (`clickApplyButton()`).
3. **Resilience**:
   - Always prefer Playwright built-in locators (`getByRole`, `getByLabel`, `getByPlaceholder`).
   - For custom dropdowns (like OrangeHRM's custom dropdown divs), use combined locator patterns rather than raw XPath.

## Template:
```typescript
import { Page, Locator } from '@playwright/test';

export class FeaturePage {
  readonly page: Page;
  readonly mainHeading: Locator;
  readonly submitButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.mainHeading = page.getByRole('heading', { level: 6 });
    this.submitButton = page.getByRole('button', { name: 'Save' });
  }

  async navigate(): Promise<void> {
    await this.page.goto('/web/index.php/feature/view');
  }

  async performAction(value: string): Promise<void> {
    // Fill and submit
    await this.submitButton.click();
  }
}
```

---
name: "test-scripts-automation"
description: "Converts Confluence test cases into executable Java Playwright POM test classes extending BaseTest with JUnit 5 and AssertJ, validating compilation with Maven."
---

# Java Playwright Test Scripts Automation Skill

Use this skill to implement automated end-to-end test suites using Java 17+, Microsoft Playwright for Java, JUnit 5, and the Page Object Model (POM) architecture.

## Objectives
1. Read approved test cases from Confluence or Jira.
2. Inspect existing Page Objects under `src/main/java/com/orangehrm/pages/`.
3. Design or extend Page Objects with resilient locators (`getByRole`, `getByLabel`, `getByPlaceholder`).
4. **Enforce Gate 4: Architecture & Locator Review** before writing or modifying code.
5. Create test classes under `src/test/java/com/orangehrm/tests/` extending `com.orangehrm.base.BaseTest`.
6. Compile and execute tests with Apache Maven: `mvn test -Dtest=<TestClass>`.

---

## 🛑 Gate 4: Human-in-the-Loop Protocol (Architecture & Locator Sign-Off)

> [!IMPORTANT]
> The agent must present the proposed Page Object methods and locators to the human engineer before writing or updating any Java files.

### Confirmation Card Template:
```markdown
### 🛑 HUMAN-IN-THE-LOOP CHECKPOINT: Gate 4 (Architecture & Locator Sign-Off)
I have prepared the Java Playwright POM design for Jira Story **${jiraKey}**:

#### 🏛️ Architecture Plan:
1. **Target Page Object**: `src/main/java/com/orangehrm/pages/${PageName}.java` (Extends `BasePage`)
   - **Proposed Methods**:
     - `public void enterCredentials(String user, String pass)`
     - `public void submitForm()`
     - `public boolean isErrorMessageVisible(String expectedText)`
   - **Proposed Locators**:
     - `submitBtn = page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Save"))`
     - `userInput = page.getByPlaceholder("Username")`
2. **Target Test Class**: `src/test/java/com/orangehrm/tests/${StoryName}Test.java` (Extends `BaseTest`)
   - `@Test @DisplayName("TC_${jiraKey}_01 - Happy path")`
   - `@Test @DisplayName("TC_${jiraKey}_02 - Mandatory field validation")`

#### ✋ Human Action Required:
Do you approve this Page Object structure and locator strategy?
- **[Approve]**: Proceed with generating Java classes and running Maven.
- **[Modify]**: Adjust locators, method names, or assertion strategy.
```

---

## Technical Standards
1. **Inheritance**:
   - Page Objects extend `BasePage` (`src/main/java/com/orangehrm/pages/BasePage.java`).
   - Test classes extend `BaseTest` (`src/test/java/com/orangehrm/base/BaseTest.java`).
2. **Playwright Artifacts**:
   - `BaseTest` automatically configures console logging (`target/logs/<TestName>-console.log`), Playwright Traces (`target/traces/<TestName>-trace.zip`), and failure screenshots (`target/screenshots/<TestName>-failed.png`).
3. **Assertions**:
   - Use AssertJ (`assertThat(...)`) or Playwright assertions (`PlaywrightAssertions.assertThat(locator)...`).
4. **Maven Execution**:
   ```bash
   mvn test -Dtest=<ClassName>Test
   ```

# Enterprise QA Automation Guidelines for GitHub Copilot in VS Code (Java Edition)

## Project Stack & Standards
- **Language**: Java 17+ (Maven)
- **Framework**: Microsoft Playwright for Java (`com.microsoft.playwright:playwright`)
- **Test Runner**: JUnit 5 (`org.junit.jupiter`) + AssertJ (`org.assertj.core`)
- **Target Application**: OrangeHRM Open Source Demo (https://opensource-demo.orangehrmlive.com/)
- **Architecture Pattern**: Strict Page Object Model (POM) under `src/main/java/com/orangehrm/pages/`
- **Tests Location**: `src/test/java/com/orangehrm/tests/`

---

## 1. Page Object Model (POM) Rules
- Every Page Object extends `BasePage` and accepts a `com.microsoft.playwright.Page` instance in its constructor.
- Never write raw assertions inside Page Object methods; encapsulate user workflows (e.g., `login(username, password)`, `submitAssignment()`).
- Expose state queries returning boolean or counts (e.g., `isUserLoggedIn()`, `getRequiredErrorsCount()`).
- Encapsulate locators as private or protected fields; prioritize `page.getByRole(...)`, `page.getByPlaceholder(...)`, `page.getByText(...)`.
- **FORBIDDEN**: Absolute XPaths (`/html/body/...`) and volatile auto-generated CSS hashes.

---

## 2. Playwright Tracing & Failure Artifacts
- All tests extend `BaseTest`.
- Every test execution records:
  - **Console Logs**: Captured via `page.onConsoleMessage` and saved to `target/logs/<TestName>-console.log`.
  - **Playwright Trace**: Started in `@BeforeEach` with screenshots, snapshots, and sources. On failure, saved to `target/traces/<TestName>-trace.zip`.
  - **Screenshots**: Saved to `target/screenshots/<TestName>-failed.png`.
- Trace Viewer command:
  ```bash
  mvn exec:java -e -Dexec.mainClass=com.microsoft.playwright.CLI -Dexec.args="show-trace target/traces/<TestName>-trace.zip"
  ```

---

## 3. Human-in-the-Loop Governance (STRICT)
**Copilot MUST NEVER make autonomous decisions on key testing activities:**
1. **NO Autonomous Code Overwrites**: When diagnosing a test failure, Copilot must inspect the artifacts (Surefire trace, console log, trace file), determine the root cause, and display a proposed diff. Copilot **MUST ASK FOR EXPLICIT HUMAN APPROVAL** before modifying any Page Object or Test file.
2. **NO Autonomous Bug Filing**: Copilot must propose defect details (summary, steps to reproduce, actual vs expected) and wait for the QA Engineer's confirmation before creating a Jira issue via MCP.
3. **Disambiguation**: If failure could be either an application regression or a brittle locator, present both interpretations to the human engineer.

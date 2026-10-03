---
name: "jira-to-test-pipeline"
description: "End-to-end QA pipeline skill that takes a Jira Story Key, audits requirements, generates test cases, scripts Java Playwright tests, and runs Maven validation."
---

# Jira-to-Test Automation Pipeline Skill

Use this skill to run the complete lifecycle from Jira User Story to executable Java Playwright test automation with JUnit 5.

## Pipeline Lifecycle

```mermaid
flowchart LR
    A["Jira Story"] --> B["Audit Specs (Gate 1)"]
    B --> C["Estimate Effort (Gate 2)"]
    C --> D["Design Test Matrix (Gate 3)"]
    D --> E["Generate Java POM (Gate 4)"]
    E --> F["Maven Validation ('mvn test')"]
    F -->|Failure| G["Self-Healing (Gate 5)"]
```

## Step-by-Step Execution:
1. **Fetch Jira Story**:
   - Query `${input:jiraKey}` via Atlassian MCP tool.
   - Extract description, acceptance criteria, and linked Confluence PRDs.
2. **Audit & Gate 1**:
   - Verify Gherkin scenarios. If ambiguous, pause and prompt user.
3. **Estimate & Gate 2**:
   - Compute story points and effort distribution. Confirm with user.
4. **Design Test Matrix & Gate 3**:
   - Create test matrix. Confirm before publishing to Confluence Space `SD`.
5. **Java POM & Gate 4**:
   - Formulate Page Objects under `src/main/java/com/orangehrm/pages/`.
   - Confirm locators with user.
6. **Script & Maven Execution**:
   - Create test class under `src/test/java/com/orangehrm/tests/` extending `BaseTest`.
   - Run `mvn test -Dtest=<TestName>`.
7. **Failure Diagnosis (if any) & Gate 5**:
   - Ingest `target/traces/*.zip` and `target/logs/*.log`. Present diagnostic diff for human decision.

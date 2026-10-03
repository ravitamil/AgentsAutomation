---
applyTo: ["**/*.md", "**/scripts/**"]
description: "Rules for authoring Jira issues, bug reports, and Confluence test documentation via Atlassian MCP."
---

# Atlassian Jira & Confluence Standards

These rules apply whenever authoring Jira issues, logging defects, or publishing test specifications to Confluence Cloud.

## 1. Jira Project `ORHM` Standards

### User Story Format:
Every Jira story must include:
1. **User Narrative**:
   > *As an* [Employee / Admin / Supervisor],  
   > *I want to* [perform action],  
   > *So that* [business value achieved].
2. **Acceptance Criteria (Gherkin Format)**:
   ```gherkin
   Scenario: Successful action
     Given the user is logged into OrangeHRM
     When they perform [action]
     Then the system should [expected state change]
   ```
3. **Traceability**: Link to the relevant Confluence PRD page.

### Defect (Bug) Report Format:
Every defect must include:
- **Environment**: OS, Browser (Chromium / Firefox / WebKit), Resolution, Build version.
- **Steps to Reproduce**: Numbered, deterministic steps from the login screen.
- **Expected Result**: What should have occurred per acceptance criteria.
- **Actual Result**: What actually occurred (quote exact error toasts or HTTP status codes).
- **Evidence**: Stack trace snippets and the Playwright Trace location (`target/traces/*.zip`).

---

## 2. Confluence Space `SD` (Space ID: `196612`) Standards

### Page Title Convention:
`Test Plan & Test Cases - <JiraKey>: <StoryTitle>`

### Page Header & Metadata:
Always include a structured summary header:
- **Linked Jira Issue**: Direct hyperlink to `https://travitamil.atlassian.net/browse/<JiraKey>`.
- **Target Application**: OrangeHRM Open Source Demo.
- **Author**: GitHub Copilot QA Automation Guild.

### Test Matrix Table Columns:
- `Test Case ID` (e.g. `TC-ORHM-4-01`)
- `Category` (Positive / Negative / Boundary / Security)
- `Test Objective`
- `Preconditions`
- `Execution Steps`
- `Expected Result`
- `Automation Candidate` (`Yes` / `No`)

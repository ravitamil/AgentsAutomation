---
name: "test-cases-creation"
description: "Generates comprehensive test case matrices (functional, negative, boundary, security) and publishes them to Confluence Cloud via Atlassian MCP or bundled Python script, enforcing Gate 3 approval."
---

# Test Cases Creation & Confluence Publishing Skill

Use this skill to convert Jira User Stories and Acceptance Criteria into formal, audit-ready Test Case matrices and publish them to Confluence Cloud under Space `SD` (ID: `196612`).

## Objectives
1. Design comprehensive test suites utilizing Black-Box test design techniques:
   - **Equivalence Partitioning**: Valid vs Invalid input classes.
   - **Boundary Value Analysis (BVA)**: Min, Max, Min-1, Max+1 boundaries.
   - **State Transition Testing**: Workflow progression and invalid shortcuts.
   - **Error Guessing**: Blank fields, special characters, whitespace trimming, double clicks.
2. Structure test cases with Test ID, Category, Objective, Preconditions, Test Steps, Expected Result, and Automation Candidate (`Yes`/`No`).
3. **Enforce Gate 3: Confluence Documentation Sign-Off** before writing or publishing any page.
4. Publish the approved matrix to Confluence Cloud via Atlassian Rovo MCP or the bundled script `scripts/publish_confluence_testcases.py`.

---

## 🛑 Gate 3: Human-in-the-Loop Protocol (Confluence Sign-Off)

> [!IMPORTANT]
> The agent must display the test matrix summary and obtain explicit human approval before calling Confluence MCP or the publishing script.

### Approval Card Template:
```markdown
### 🛑 HUMAN-IN-THE-LOOP CHECKPOINT: Gate 3 (Confluence Publish Sign-Off)
I have generated the test matrix for Jira Story **${jiraKey}** (${title}):

#### 📋 Proposed Test Case Summary:
- **Total Test Cases**: `X`
  - **Positive / Happy Path**: `A` cases
  - **Negative / Validation**: `B` cases
  - **Boundary Value**: `C` cases
  - **Security / Permissions**: `D` cases
- **Target Confluence Space**: `SD` (Software Development, ID: `196612`)
- **Page Title**: `Test Plan & Test Cases - ${jiraKey}: ${title}`

#### 📝 Sample Test Case Preview:
| Test ID | Category | Objective | Steps | Expected Result | Auto? |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `TC_${jiraKey}_01` | Positive | Successful workflow completion | 1. Navigate...<br/>2. Enter...<br/>3. Click Save | Record saved, success toast displayed | Yes |
| `TC_${jiraKey}_02` | Negative | Blank required fields validation | 1. Leave field empty...<br/>2. Click Save | "Required" error text highlighted in red | Yes |

#### ✋ Human Action Required:
Do you approve publishing this test matrix directly to Confluence Cloud?
- **[Yes]**: Proceed with Confluence publishing via Atlassian MCP / Python script.
- **[Modify]**: Adjust scenarios, add missing edge cases, or modify coverage before publishing.
```

---

## Confluence Publishing Methods

### Option A: Via Atlassian MCP Server (Recommended)
Invoke the Atlassian MCP tool:
```json
{
  "server": "com.atlassian/atlassian-mcp-server",
  "tool": "createConfluencePage",
  "arguments": {
    "spaceId": "196612",
    "title": "Test Plan & Test Cases - ${jiraKey}: ${title}",
    "body": "<table class='wrapped'>...</table>"
  }
}
```

### Option B: Via Bundled Python Script
```bash
python scripts/publish_confluence_testcases.py <JIRA_KEY> "<TITLE>" <HTML_FILE_PATH>
```

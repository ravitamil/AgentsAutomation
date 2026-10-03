---
name: "qa-estimation"
description: "Calculates story points and testing effort breakdown (test design, manual execution, Java Playwright POM automation, defect buffer) and enforces Gate 2 human approval."
---

# QA Estimation & Sizing Skill

Use this skill to determine test complexity, calculate story points, and provide an effort breakdown for testing a user story or epic.

## Objectives
1. Assess the complexity of the feature across UI interactions, API dependencies, data setup, and non-functional requirements.
2. Calculate Story Points using a modified Fibonacci scale (1, 2, 3, 5, 8, 13).
3. Generate an effort distribution breakdown across:
   - **Test Design**: Writing test cases and equivalence partitioning.
   - **Manual Execution & Verification**: Exploratory and exploratory boundary testing.
   - **Java Playwright POM Automation**: Authoring Page Objects, locators, and assertions in JUnit 5.
   - **Defect Retesting & Buffer**: Standard 20% safety margin.
4. **Enforce Gate 2: Agile Estimation Approval** by presenting the estimate to the QA Lead for consensus before finalizing.

---

## Sizing Matrix

| Story Points | Complexity Level | Criteria | Typical Scope |
| :---: | :---: | :--- | :--- |
| **1 SP** | Trivial | Simple static UI text change, single input validation, no state change. | 1-2 Test Cases, 0-1 POM method. |
| **2 SP** | Simple | Standard CRUD form, single user role, predictable validation errors. | 3-5 Test Cases, 1 POM class modification. |
| **3 SP** | Moderate | Multi-step form, date/calendar calculations, file uploads, role differences (Admin vs ESS). | 6-10 Test Cases, 1-2 POM classes, automated suite. |
| **5 SP** | Complex | Multi-page workflow, state transitions (Leave Apply -> Approve -> Balance recalculation), multiple API integrations. | 10-18 Test Cases, full E2E POM suite with Traces. |
| **8 SP** | Very High | Cross-module dependencies, reporting exports, bulk data processing, external webhooks. | 20+ Test Cases, split into multiple sub-tasks. |

---

## 🛑 Gate 2: Human-in-the-Loop Protocol (Estimation Sign-Off)

> [!IMPORTANT]
> The agent must present the estimation breakdown to the user and obtain explicit consensus before recording or updating any ticket.

### Confirmation Card Template:
```markdown
### 🛑 HUMAN-IN-THE-LOOP CHECKPOINT: Gate 2 (Estimation Sign-Off)
I have calculated the QA testing effort for Jira Story **${jiraKey}**:

#### 📊 Proposed Effort Breakdown:
- **Test Design & Test Cases (Confluence)**: `X.X hours`
- **Manual Verification & Boundary Checks**: `X.X hours`
- **Java Playwright Automation (POM + BaseTest)**: `X.X hours`
- **Defect Retesting Buffer (20%)**: `X.X hours`
- **Total QA Effort**: `X.X hours`
- **Recommended Story Points**: **${storyPoints} SP** (${complexityTier})

#### 💡 Complexity Justification:
<Brief 2-3 bullet explanation of what drives the sizing (e.g., custom dropdowns, date picker logic, role switching)>

#### ✋ Human Action Required:
Do you agree with this sizing (**${storyPoints} SP**), or would you like to adjust the estimate based on team velocity?
```

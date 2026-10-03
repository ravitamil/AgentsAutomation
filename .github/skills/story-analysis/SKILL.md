---
name: "story-analysis"
description: "Audits Jira user stories and Confluence PRDs for testability, missing edge cases, and Acceptance Criteria ambiguity, strictly enforcing Gate 1 human alignment."
---

# QA Story Analysis & Requirements Audit Skill

Use this skill whenever analyzing a Jira user story, Confluence Product Requirements Document (PRD), or feature specification before test design or test implementation begins.

## Objectives
1. Retrieve Jira issue details and linked Confluence PRDs using the Atlassian MCP server (`com.atlassian/atlassian-mcp-server`).
2. Audit the requirements against industry QA standards (Gherkin syntax, completeness, testability).
3. Identify ambiguous language, missing boundary conditions, unstated error messages, and unhandled edge cases.
4. **Enforce Gate 1: Requirements & AC Alignment** by pausing for human confirmation whenever any doubt exists.

---

## 🛑 Gate 1: Human-in-the-Loop Protocol (Zero-Presumption Policy)

> [!IMPORTANT]
> **Zero-Presumption Rule**: You must **NEVER** guess or invent business logic. If any Acceptance Criterion is vague, contradictory, or lacks edge cases, pause immediately and request human clarification.

### Ambiguity Trigger Words:
Flag requirements containing words like:
- *"System should handle gracefully"*
- *"Appropriate error message"*
- *"Reasonable time / fast response"*
- *"Valid format"* (without explicit regex or examples)

### Human Clarification Card Template:
When doubts or missing criteria are identified, output this exact card and pause:

```markdown
### 🛑 HUMAN-IN-THE-LOOP CHECKPOINT: Gate 1 (Requirements Clarification)
I have audited Jira Story **${jiraKey}** against Confluence PRD specs. Before proceeding to estimation or test design, I require human alignment on the following doubts:

#### ❓ Clarifying Questions for Product Owner / QA Lead:
1. **[Doubt 1: Field / Behavior]**: <Specific question with context>
   - *Assumed Behavior*: <What standard behavior would be>
   - *Risk*: <Why guessing this could introduce bugs or invalid tests>
2. **[Doubt 2: Boundary / Error Handling]**: <Specific question with context>
   - *Assumed Behavior*: <What standard behavior would be>
   - *Risk*: <Why guessing this could introduce bugs or invalid tests>

#### ✋ Human Action Required:
Please reply with your answers or confirm if the assumed behavior is correct. I will **NOT** proceed with test case generation until you confirm.
```

---

## Audit Checklist
- [ ] **Gherkin Structure**: Are scenarios formatted in clear `Given [context] When [event] Then [outcome]`?
- [ ] **Data Boundaries**: Are field length limits, numerical ranges, and accepted file extensions explicitly defined?
- [ ] **Negative Paths**: Are exact validation error messages quoted?
- [ ] **Access Control**: Are User Roles (e.g. Admin vs ESS in OrangeHRM) and unauthorized redirect behaviors specified?
- [ ] **State Transitions**: Are lifecycle transitions (e.g., Pending Approval -> Scheduled -> Taken / Cancelled) fully documented?

---

## Output Format (Upon Human Confirmation)
Once all doubts are clarified and approved by the user:
```markdown
## ✅ Gate 1 Passed: Story Analysis Report
- **Jira Key**: ${jiraKey}
- **Summary**: <Title>
- **Testability Status**: READY FOR TEST DESIGN
- **Approved Acceptance Criteria**:
  1. Scenario 1: Given ... When ... Then ...
  2. Scenario 2: Given ... When ... Then ...
- **Next Recommended Step**: Proceed to `@qa-estimator` for sizing or `@test-cases-creator` for matrix design.
```

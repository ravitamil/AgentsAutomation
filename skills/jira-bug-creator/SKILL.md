---
name: "jira-bug-creator"
description: "Constructs professional, audit-ready Jira bug tickets with reproduction steps, environment details, console logs, and Playwright trace attachments via Atlassian MCP."
---

# Jira Bug Creator Skill

Use this skill whenever filing a software defect or bug in Jira Cloud (Project: `ORHM`) resulting from test execution failures or exploratory testing.

## Objectives
1. Extract failure evidence from Playwright Traces (`target/traces/*.zip`), console logs (`target/logs/*.log`), and Surefire reports.
2. Structure the defect following standard enterprise QA bug report standards:
   - **Summary**: Concise `[Module] Description of issue when [trigger]`
   - **Issue Type**: `Bug`
   - **Priority**: `Highest`, `High`, `Medium`, or `Low`
   - **Environment**: OS, Browser (Chromium / Firefox / WebKit), Resolution, Build version.
   - **Steps to Reproduce**: Numbered, deterministic steps.
   - **Expected Result**: What should have occurred.
   - **Actual Result**: What actually occurred (including exact error messages).
   - **Evidence & Logs**: Truncated stack traces and console errors.
3. Submit the defect to Jira Cloud via Atlassian MCP (`com.atlassian/atlassian-mcp-server`).

---

## Standard Bug Description Template

```markdown
*Target Application:* OrangeHRM Open Source Demo (https://opensource-demo.orangehrmlive.com)
*Environment:* Chromium Headless / Java 17 / Playwright Java 1.47.0
*Linked Story:* ${jiraStoryKey}

h3. Description
${conciseDescription}

h3. Steps to Reproduce
1. Navigate to OrangeHRM login page.
2. Log in with standard credentials.
3. Navigate to '${modulePath}'.
4. ${triggerAction}

h3. Expected Result
${expectedBehavior}

h3. Actual Result
${actualBehavior}

h3. Failure Evidence & Logs
{code:java}
${stackTraceSnippet}
{code}

*Playwright Trace Location:* `target/traces/${testName}-trace.zip`
```

---
applyTo: "target/**"
description: "Rules for triaging test execution failure artifacts (Surefire logs, Playwright traces, console logs) and self-healing under Gate 5."
---

# Test Failure Triage & Self-Healing Instructions

These rules apply whenever inspecting build outputs, test logs, or Playwright failure artifacts under `target/`.

## 1. Artifact Ingestion Hierarchy
When a test fails, triage evidence in the following sequential order:
1. **Surefire Report**: `target/surefire-reports/<TestClass>.txt` (extract line of code and assertion failure).
2. **Browser Console Logs**: `target/logs/<TestName>-console.log` (detect uncaught JS errors, 404/500 API responses).
3. **Playwright Trace Archive**: `target/traces/<TestName>-trace.zip` (contains DOM snapshots, network waterfall, action timeline).
4. **Failure Screenshot**: `target/screenshots/<TestName>-failed.png` (visual confirmation of state at failure moment).

## 2. Failure Root-Cause Classification
Classify every failure into one of 3 distinct categories:

| Category | Diagnostic Indicators | Recommended Action |
| :--- | :--- | :--- |
| **Timing / Overlay** | `TimeoutError`, element intercepted by `.oxd-form-loader` or `.oxd-loading-spinner`. | Add explicit wait for loader detachment in Page Object. |
| **Selector Drift** | `waiting for locator(...) to be visible`, changed aria role or label. | Update Page Object locator to match new accessible attribute. |
| **Product Defect** | Console log has 500 status, assertion value mismatches business logic. | Propose logging a Jira Bug in project `ORHM`. |

## 3. Strict Gate 5 Human Approval Policy
- **NEVER** autonomously overwrite Page Objects or test files.
- Present the root cause analysis, artifact links, and proposed diff to the human engineer.
- Request user choice:
  1. Apply code diff to Page Object or Test.
  2. File Jira bug in `ORHM` via Atlassian MCP.
  3. Launch local Playwright Trace Viewer (`mvn exec:java -e ...`).

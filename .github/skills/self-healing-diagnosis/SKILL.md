---
name: "self-healing-diagnosis"
description: "Parses failed Maven test runs, Surefire stack traces, console logs (target/logs/*.log), and Playwright Traces (target/traces/*.zip) to diagnose root causes and propose fixes under Gate 5 approval."
---

# Self-Healing & Trace Diagnostic Skill

Use this skill whenever a Java Playwright test fails during local execution or CI/CD runs.

## Objectives
1. Automatically ingest test execution failure artifacts:
   - **Surefire Reports**: `target/surefire-reports/*.txt`
   - **Browser Console Logs**: `target/logs/<TestName>-console.log`
   - **Playwright Trace ZIP**: `target/traces/<TestName>-trace.zip`
   - **Failure Screenshots**: `target/screenshots/<TestName>-failed.png`
2. Classify the root cause:
   - **Timing / Asynchronous Overlay**: Pointer interception by AJAX loaders (e.g. `.oxd-form-loader`).
   - **DOM Drift / Selector Failure**: Label, placeholder, or aria role change.
   - **Application Defect**: Uncaught JavaScript 500/400 exception or broken business logic.
3. Formulate the precise code diff for resolution.
4. **Enforce Gate 5: Self-Healing & Defect Remediation Sign-Off** - never modify code without explicit human consent.

---

## 🛑 Gate 5: Human-in-the-Loop Protocol (Remediation Sign-Off)

> [!IMPORTANT]
> The agent must **NEVER** autonomously overwrite files, modify locators, or file Jira defects without the user selecting one of the remediation options.

### Diagnostic Card Template:
```markdown
### 🛑 HUMAN-IN-THE-LOOP CHECKPOINT: Gate 5 (Self-Healing Diagnosis)
I have diagnosed the failure in test: **${testClass}#${testMethod}**

#### 🔍 Root Cause Analysis:
- **Failure Classification**: `[Timing / Selector Drift / Application Defect]`
- **Root Cause**: <Concise explanation of what broke>
- **Artifact Evidence**:
  - *Failing Assertion*: `<File.java:Line>` - `<AssertionError details>`
  - *Console Logs*: `target/logs/${testName}-console.log`
  - *Trace File*: `target/traces/${testName}-trace.zip`

#### 💡 Proposed Resolution (Diff):
```diff
--- a/src/main/java/com/orangehrm/pages/${PageName}.java
+++ b/src/main/java/com/orangehrm/pages/${PageName}.java
@@ -25,3 +25,3 @@
-    this.submitBtn = page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Old"));
+    this.submitBtn = page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Save"));
```

#### ✋ Human Action Required:
Please select how to proceed:
- **[1] Approve & Apply Fix**: Overwrite the Page Object / Test file with the proposed diff and re-run Maven.
- **[2] File Jira Defect**: If this represents a genuine application bug, invoke Atlassian MCP to log a defect in project `ORHM`.
- **[3] Inspect Trace Visually**: Launch Playwright Trace Viewer locally:
  `mvn exec:java -e -Dexec.mainClass=com.microsoft.playwright.CLI -Dexec.args="show-trace target/traces/${testName}-trace.zip"`
```

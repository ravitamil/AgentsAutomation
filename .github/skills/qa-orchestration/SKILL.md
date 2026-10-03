---
name: "qa-orchestration"
description: "Coordinates multi-agent workflows across story analysis, estimation, test matrix design, Java Playwright scripting, and self-healing diagnostics while enforcing all 5 HITL gates."
---

# QA Master Orchestration Skill

Use this skill to orchestrate end-to-end quality engineering workflows across multiple specialist agents, maintaining strict Human-in-the-Loop verification gates.

## Specialist Agent Topology

| Specialist Agent | Core Responsibility | Verification Gate |
| :--- | :--- | :--- |
| `@story-analyst` | Audits Jira Stories and Confluence PRDs for ambiguity and completeness. | **Gate 1**: Requirements & AC Alignment |
| `@qa-estimator` | Calculates complexity points and test effort breakdown. | **Gate 2**: Sizing & Estimation Sign-off |
| `@test-cases-creator` | Generates comprehensive test matrices and publishes to Confluence. | **Gate 3**: Confluence Publishing Sign-off |
| `@test-scripts-creator` | Implements Java Playwright POM test classes and runs Maven. | **Gate 4**: Test Architecture & Locators Sign-off |
| `@self-healing-analyzer` | Ingests Playwright Traces and console logs on failure to diagnose root causes. | **Gate 5**: Remediation & Fix Sign-off |

---

## The 5-Gate Conductor Protocol
1. **Never Skip Gates**: Even if the user issues a broad prompt like "automate everything for ORHM-4", execute stage-by-stage and halt at each gate for explicit confirmation.
2. **Context Passing**: Forward approved outputs from earlier stages (e.g. refined Gherkin ACs from Gate 1 to Gate 2 and Gate 3) so subsequent agents build on verified knowledge.
3. **Artifact Verification**: Validate that Playwright Traces (`target/traces/*.zip`), logs (`target/logs/*.log`), and Surefire reports exist before triggering `@self-healing-analyzer`.

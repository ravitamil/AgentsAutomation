import sys
import json
import base64
import urllib.request
import urllib.error

DOMAIN = "https://travitamil.atlassian.net"
EMAIL = "travitamil@gmail.com"
TOKEN = "ATATT3xFfGF0en2wYoMbHltzWbWIkb3H4r_rG68kUGVM8HoTyL8lTGvXTvf5FrTrJRjAnSXKHtCNVXf9bqM6s1I2mJDLVhe_BxNnDw8lgBdX4Pb54-2bFbCiTJA70JGDChCfKVS6VRTLR05nVJa9GQS2pf69Aadi7senVfRab9Hep8rhiqSFr_A=4302ADC7"

raw_auth = f"{EMAIL}:{TOKEN}".encode('utf-8')
AUTH_HEADER = base64.b64encode(raw_auth).decode('utf-8')

def req(url, method='GET', data=None):
    request = urllib.request.Request(url, method=method)
    request.add_header('Authorization', f'Basic {AUTH_HEADER}')
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json')
    body = json.dumps(data).encode('utf-8') if data is not None else None
    try:
        with urllib.request.urlopen(request, data=body) as response:
            res_body = response.read().decode('utf-8')
            return (json.loads(res_body) if res_body else {}), response.status
    except urllib.error.HTTPError as e:
        err = e.read().decode('utf-8')
        return {"error": err, "status": e.code}, e.code
    except Exception as e:
        return {"error": str(e), "status": 500}, 500

def create_jira_issue(project_key, summary, description_doc, issue_type="Story"):
    url = f"{DOMAIN}/rest/api/3/issue"
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "issuetype": {"name": issue_type},
            "description": description_doc
        }
    }
    res, status = req(url, method='POST', data=payload)
    if status in (200, 201):
        key = res.get('key')
        print(f"[JIRA] Created {issue_type} {key}: {DOMAIN}/browse/{key}")
        return key
    else:
        print(f"[JIRA Error] status={status}: {res}")
        return None

def create_confluence_page(space_id, title, markdown_body):
    url = f"{DOMAIN}/wiki/api/v2/pages"
    # Using standard storage format (HTML-compatible)
    payload = {
        "spaceId": str(space_id),
        "status": "current",
        "title": title,
        "body": {
            "representation": "storage",
            "value": markdown_body
        }
    }
    res, status = req(url, method='POST', data=payload)
    if status in (200, 201):
        page_id = res.get('id')
        web_link = res.get('_links', {}).get('webui', '')
        print(f"[CONFLUENCE] Created Page '{title}' (ID: {page_id}): {DOMAIN}/wiki{web_link}")
        return page_id
    else:
        print(f"[CONFLUENCE Error] status={status}: {res}")
        return None

def main():
    print("=== SEEDING JIRA STORIES IN ORHM ===")

    # Story 1: Leave Application
    story1_desc = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Target URL: ", "marks": [{"type": "strong"}]},
                    {"type": "text", "text": "https://opensource-demo.orangehrmlive.com/web/index.php/leave/applyLeave"}
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "As an ", "marks": [{"type": "strong"}]},
                    {"type": "text", "text": "authenticated OrangeHRM employee,\n"},
                    {"type": "text", "text": "I want to ", "marks": [{"type": "strong"}]},
                    {"type": "text", "text": "submit a leave application with leave type, date range, and comments,\n"},
                    {"type": "text", "text": "So that ", "marks": [{"type": "strong"}]},
                    {"type": "text", "text": "my supervisor can review and approve my requested time off."}
                ]
            },
            {
                "type": "heading",
                "attrs": {"level": 3},
                "content": [{"type": "text", "text": "Acceptance Criteria (Gherkin)"}]
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Scenario 1: Happy Path - Apply for Medical Leave\n", "marks": [{"type": "strong"}]},
                    {"type": "text", "text": "Given the user is logged into OrangeHRM with username 'Admin' and password 'admin123'\n"},
                    {"type": "text", "text": "And the user navigates to the 'Leave' -> 'Apply' tab\n"},
                    {"type": "text", "text": "When the user selects Leave Type 'CAN - FMLA'\n"},
                    {"type": "text", "text": "And enters From Date '2026-11-10' and To Date '2026-11-12'\n"},
                    {"type": "text", "text": "And enters Comment 'Attending scheduled medical procedure'\n"},
                    {"type": "text", "text": "And clicks the 'Apply' button\n"},
                    {"type": "text", "text": "Then a success notification toast 'Success: Successfully Saved' should appear\n\n"},
                    {"type": "text", "text": "Scenario 2: Negative Validation - Missing Required Fields\n", "marks": [{"type": "strong"}]},
                    {"type": "text", "text": "Given the user is on the 'Apply Leave' page\n"},
                    {"type": "text", "text": "When the user clicks the 'Apply' button without filling any fields\n"},
                    {"type": "text", "text": "Then validation error messages 'Required' must appear beneath the Leave Type and Date fields."}
                ]
            }
        ]
    }
    s1_key = create_jira_issue("ORHM", "ORHM-1: Employee Leave Application Workflow (OrangeHRM)", story1_desc, "Story")

    # Story 2: PIM Search
    story2_desc = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Target URL: ", "marks": [{"type": "strong"}]},
                    {"type": "text", "text": "https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList"}
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "As an ", "marks": [{"type": "strong"}]},
                    {"type": "text", "text": "HR administrator,\n"},
                    {"type": "text", "text": "I want to ", "marks": [{"type": "strong"}]},
                    {"type": "text", "text": "search employees by Employment Status or Employee Name,\n"},
                    {"type": "text", "text": "So that ", "marks": [{"type": "strong"}]},
                    {"type": "text", "text": "I can quickly audit staff employment records."}
                ]
            },
            {
                "type": "heading",
                "attrs": {"level": 3},
                "content": [{"type": "text", "text": "Acceptance Criteria"}]
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "1. Filter by 'Full-Time Permanent' and click 'Search' displays only matching records.\n"},
                    {"type": "text", "text": "2. Searching for a non-existent name displays 'No Records Found' toast or table empty state.\n"},
                    {"type": "text", "text": "3. Clicking 'Reset' clears all search inputs."}
                ]
            }
        ]
    }
    s2_key = create_jira_issue("ORHM", "ORHM-2: PIM Employee Search and Filtering", story2_desc, "Story")

    # Seed Confluence PRD
    print("\n=== SEEDING CONFLUENCE PRD SPECIFICATION ===")
    sd_space_id = "196612"  # 'Software Development' space
    conf_html = """
    <h2>OrangeHRM Product Requirement Document: Leave &amp; Attendance Management</h2>
    <p><strong>Version:</strong> 2.4 | <strong>Status:</strong> Approved | <strong>Author:</strong> QA &amp; Product Engineering</p>
    
    <hr/>
    
    <h3>1. Executive Summary</h3>
    <p>This document specifies the end-to-end business requirements for the <strong>Leave Application &amp; Entitlement Engine</strong> in OrangeHRM. It establishes the acceptance criteria used by the QA Automation team to author Playwright test suites.</p>
    
    <h3>2. Target Application Environment</h3>
    <ul>
      <li><strong>Demo Instance:</strong> <a href="https://opensource-demo.orangehrmlive.com">OrangeHRM Open Source Demo</a></li>
      <li><strong>Default Admin Credentials:</strong> <code>Admin / admin123</code></li>
      <li><strong>Direct Apply URL:</strong> <code>/web/index.php/leave/applyLeave</code></li>
    </ul>

    <h3>3. Business Rules &amp; Constraints</h3>
    <table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%;">
      <thead>
        <tr style="background-color:#f4f5f7;">
          <th>Rule ID</th>
          <th>Requirement</th>
          <th>Behavior</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>BR-LEAVE-01</strong></td>
          <td>Leave Type Selection</td>
          <td>Mandatory dropdown. Options include CAN - FMLA, CAN - Bereavement, US - Vacation.</td>
        </tr>
        <tr>
          <td><strong>BR-LEAVE-02</strong></td>
          <td>Date Range Validation</td>
          <td>From Date cannot be later than To Date. Date format must adhere to YYYY-MM-DD.</td>
        </tr>
        <tr>
          <td><strong>BR-LEAVE-03</strong></td>
          <td>Balance Calculation</td>
          <td>If an employee has 0 days balance, an informational balance alert should be displayed, but application can proceed if unpaid leave is enabled.</td>
        </tr>
        <tr>
          <td><strong>BR-LEAVE-04</strong></td>
          <td>Success Feedback</td>
          <td>Upon valid submission, a temporary toast notification with text <code>Successfully Saved</code> must be visible within 5 seconds.</td>
        </tr>
      </tbody>
    </table>

    <h3>4. Linked Jira Epics &amp; Stories</h3>
    <ul>
      <li><strong>ORHM-1:</strong> Employee Leave Application Workflow (OrangeHRM)</li>
      <li><strong>ORHM-2:</strong> PIM Employee Search and Filtering</li>
    </ul>

    <h3>5. Automation Guidelines</h3>
    <p>Automation scripts must use Playwright in TypeScript with Page Object Model (POM). Locators must rely on accessible roles and labels (<code>getByRole('button', { name: 'Apply' })</code>). Avoid brittle XPaths.</p>
    """

    create_confluence_page(sd_space_id, "PRD - OrangeHRM Leave Entitlement and Application Module", conf_html)

if __name__ == '__main__':
    main()

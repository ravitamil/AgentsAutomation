"""
Expanded Seeder for OrangeHRM Jira Stories, Bugs, and Confluence PRDs.
Covers PIM, Recruitment, and Admin User Management.
"""

import sys
import json
import base64
import urllib.request
import urllib.error

DOMAIN = "https://travitamil.atlassian.net"
EMAIL = "travitamil@gmail.com"
TOKEN = "ATATT3xFfGF0en2wYoMbHltzWbWIkb3H4r_rG68kUGVM8HoTyL8lTGvXTvf5FrTrJRjAnSXKHtCNVXf9bqM6s1I2mJDLVhe_BxNnDw8lgBdX4Pb54-2bFbCiTJA70JGDChCfKVS6VRTLR05nVJa9GQS2pf69Aadi7senVfRab9Hep8rhiqSFr_A=4302ADC7"
SPACE_ID = "196612"  # 'SD' Software Development space

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

def create_jira_issue(project_key, summary, description_text, issue_type="Story", priority_name="Medium"):
    url = f"{DOMAIN}/rest/api/3/issue"
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "issuetype": {"name": issue_type},
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": description_text}]
                    }
                ]
            }
        }
    }
    res, status = req(url, method='POST', data=payload)
    if status in (200, 201):
        key = res.get('key')
        print(f"[OK] [JIRA] Created {issue_type} {key}: {DOMAIN}/browse/{key} - {summary}")
        return key
    else:
        print(f"[ERROR] [JIRA Error] status={status}: {res}")
        return None

def create_confluence_page(space_id, title, html_body):
    url = f"{DOMAIN}/wiki/api/v2/pages"
    payload = {
        "spaceId": str(space_id),
        "status": "current",
        "title": title,
        "body": {
            "representation": "storage",
            "value": html_body
        }
    }
    res, status = req(url, method='POST', data=payload)
    if status in (200, 201):
        pid = res.get('id')
        webui = res.get('_links', {}).get('webui', '')
        print(f"[OK] [CONFLUENCE] Created Page '{title}' (ID: {pid}): {DOMAIN}/wiki{webui}")
        return pid
    else:
        print(f"[ERROR] [CONFLUENCE Error] status={status}: {res}")
        return None

def main():
    print("==================================================")
    print("  SEEDING EXPANDED JIRA TICKETS IN ORHM           ")
    print("==================================================")

    # 1. PIM Add Employee Story
    s3_desc = (
        "As an HR Administrator\n"
        "I want to add a new employee record with optional login credentials creation\n"
        "So that the new hire is registered in the corporate directory and can log in.\n\n"
        "Target URL: https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee\n\n"
        "Acceptance Criteria (Gherkin):\n"
        "Scenario: Successfully Add Employee without Login Credentials\n"
        "  Given the HR Admin navigates to PIM > Add Employee\n"
        "  When the Admin fills First Name 'Sarah', Last Name 'Connor'\n"
        "  And clicks 'Save'\n"
        "  Then the system displays 'Successfully Saved' toast\n"
        "  And redirects to Personal Details page.\n\n"
        "Scenario: Mandatory First and Last Name Validation\n"
        "  Given the HR Admin is on the Add Employee page\n"
        "  When the Admin clicks 'Save' with empty names\n"
        "  Then inline 'Required' error messages appear beneath First Name and Last Name fields."
    )
    create_jira_issue("ORHM", "ORHM-3: PIM - Add New Employee with Validation", s3_desc, "Story")

    # 2. Recruitment Candidate Story
    s4_desc = (
        "As a Talent Acquisition Specialist\n"
        "I want to register a candidate for an open job vacancy and upload their resume\n"
        "So that our recruitment team can track them through the hiring pipeline.\n\n"
        "Target URL: https://opensource-demo.orangehrmlive.com/web/index.php/recruitment/addCandidate\n\n"
        "Acceptance Criteria:\n"
        "1. Full Name (First, Last) and Email are mandatory fields.\n"
        "2. Vacancy dropdown allows associating candidate to open positions (e.g. Senior QA Lead, Sales Representative).\n"
        "3. Resume upload accepts PDF and DOCX files up to 5MB.\n"
        "4. Invalid email format triggers inline error 'Expected format: admin@example.com'."
    )
    create_jira_issue("ORHM", "ORHM-4: Recruitment - Candidate Registration and Resume Upload", s4_desc, "Story")

    # 3. Admin User Management Story
    s5_desc = (
        "As a Super Administrator\n"
        "I want to manage system user accounts, roles, and status in the Admin module\n"
        "So that staff can be granted appropriate Admin or ESS system privileges.\n\n"
        "Target URL: https://opensource-demo.orangehrmlive.com/web/index.php/admin/saveSystemUser\n\n"
        "Acceptance Criteria:\n"
        "1. User Role dropdown supports 'Admin' and 'ESS'.\n"
        "2. Employee Name field uses asynchronous autocomplete typing hints.\n"
        "3. Status dropdown supports 'Enabled' and 'Disabled'.\n"
        "4. Password must contain at least 8 characters with alphanumeric and special characters."
    )
    create_jira_issue("ORHM", "ORHM-5: Admin - System User Management & Role Provisioning", s5_desc, "Story")

    # 4. Realistic Defect: PIM Duplicate Employee ID
    b6_desc = (
        "Issue Type: Bug\n"
        "Severity: High\n"
        "Component: PIM Module / Employee Creation\n\n"
        "Description:\n"
        "When creating a new employee in PIM > Add Employee, if a user manually specifies an Employee ID "
        "that already belongs to an existing staff member, the system displays an unhandled 500 error instead "
        "of a user-friendly validation warning 'Employee Id already exists'.\n\n"
        "Steps to Reproduce:\n"
        "1. Login as Admin to OrangeHRM Demo.\n"
        "2. Navigate to PIM > Add Employee.\n"
        "3. Enter First Name: 'Alex', Last Name: 'Murphy'.\n"
        "4. In 'Employee Id', enter an existing ID: '0024'.\n"
        "5. Click 'Save'.\n\n"
        "Expected Result:\n"
        "Inline validation error appears beneath Employee Id: 'Employee Id already exists'.\n\n"
        "Actual Result:\n"
        "Page freezes with 'System Error: Duplicate key constraint violated' and form is not cleared."
    )
    create_jira_issue("ORHM", "[Defect][PIM] System throws unhandled exception on duplicate Employee ID", b6_desc, "Bug")

    # 5. Realistic Defect: Recruitment Resume File Upload
    b7_desc = (
        "Issue Type: Bug\n"
        "Severity: Medium\n"
        "Component: Recruitment Module / Candidate Upload\n\n"
        "Description:\n"
        "When attaching a valid resume in .docx format under 1MB during candidate registration, the file "
        "attachment spinner loops indefinitely and prevents form submission.\n\n"
        "Steps to Reproduce:\n"
        "1. Navigate to Recruitment > Candidates > Add.\n"
        "2. Enter valid candidate details.\n"
        "3. Upload a sample .docx resume (e.g. resume_qa_lead.docx, size 450KB).\n"
        "4. Click 'Save'.\n\n"
        "Expected Result:\n"
        "File attaches successfully and candidate record is created.\n\n"
        "Actual Result:\n"
        "UI remains stuck on 'Uploading...' and 'Save' button is disabled."
    )
    create_jira_issue("ORHM", "[Defect][Recruitment] Resume file upload hangs indefinitely for .docx files", b7_desc, "Bug")

    print("\n==================================================")
    print("  SEEDING EXPANDED CONFLUENCE PRD SPECIFICATIONS  ")
    print("==================================================")

    # Confluence Page 1: PIM PRD
    pim_html = """
    <h2>OrangeHRM PRD: Personnel Information Management (PIM) Module</h2>
    <p><strong>Module:</strong> PIM | <strong>Version:</strong> 3.1 | <strong>Status:</strong> Approved</p>
    
    <hr/>
    <h3>1. Module Overview</h3>
    <p>The Personnel Information Management (PIM) module is the foundational HR record system in OrangeHRM. It maintains staff profiles, job assignments, personal identification, and login credential binding.</p>

    <h3>2. Business Rules &amp; Validations</h3>
    <table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%;">
      <thead>
        <tr style="background-color:#0052cc; color:#ffffff;">
          <th>Rule ID</th>
          <th>Requirement</th>
          <th>Validation / Constraint</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>BR-PIM-01</strong></td>
          <td>Employee Name</td>
          <td>First Name and Last Name are mandatory. Max length: 30 characters each.</td>
        </tr>
        <tr>
          <td><strong>BR-PIM-02</strong></td>
          <td>Employee ID</td>
          <td>Unique alphanumeric identifier. Auto-generated by default, but editable by Admin. Duplicate IDs must be rejected.</td>
        </tr>
        <tr>
          <td><strong>BR-PIM-03</strong></td>
          <td>Login Credentials</td>
          <td>Optional toggle during creation. If enabled, Username must be unique across all system users and Password must meet complexity policy.</td>
        </tr>
        <tr>
          <td><strong>BR-PIM-04</strong></td>
          <td>Search &amp; Filter</td>
          <td>Supports search by Employee Name, ID, Employment Status, Job Title, and Sub Unit.</td>
        </tr>
      </tbody>
    </table>

    <h3>3. Traceability to Jira Stories</h3>
    <ul>
      <li><a href="https://travitamil.atlassian.net/browse/ORHM-2">ORHM-2: PIM Employee Search and Filtering</a></li>
      <li><a href="https://travitamil.atlassian.net/browse/ORHM-3">ORHM-3: PIM - Add New Employee with Validation</a></li>
    </ul>
    """
    create_confluence_page(SPACE_ID, "PRD - OrangeHRM Personnel Information Management (PIM) Module", pim_html)

    # Confluence Page 2: Recruitment PRD
    recruitment_html = """
    <h2>OrangeHRM PRD: Recruitment &amp; Talent Acquisition Module</h2>
    <p><strong>Module:</strong> Recruitment | <strong>Version:</strong> 2.0 | <strong>Status:</strong> Approved</p>
    
    <hr/>
    <h3>1. Feature Scope</h3>
    <p>The Recruitment module streamlines candidate application tracking across job vacancies. It covers Candidate Registration, Resume Ingestion, Interview Scheduling, and Pipeline Progression (Shortlisted -> Interview -> Offered -> Hired).</p>

    <h3>2. Form &amp; Data Specifications</h3>
    <table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%;">
      <thead>
        <tr style="background-color:#0052cc; color:#ffffff;">
          <th>Field Name</th>
          <th>Mandatory</th>
          <th>Rules &amp; Constraints</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Full Name</strong></td>
          <td>Yes</td>
          <td>First and Last Name required.</td>
        </tr>
        <tr>
          <td><strong>Vacancy</strong></td>
          <td>No</td>
          <td>Dropdown linking candidate to published job vacancy.</td>
        </tr>
        <tr>
          <td><strong>Email</strong></td>
          <td>Yes</td>
          <td>Valid RFC 5322 email regex pattern required.</td>
        </tr>
        <tr>
          <td><strong>Resume File</strong></td>
          <td>No</td>
          <td>Allowed extensions: <code>.pdf, .doc, .docx, .odt</code>. Max file size: 5MB.</td>
        </tr>
      </tbody>
    </table>

    <h3>3. Traceability to Jira Stories</h3>
    <ul>
      <li><a href="https://travitamil.atlassian.net/browse/ORHM-4">ORHM-4: Recruitment - Candidate Registration and Resume Upload</a></li>
      <li><a href="https://travitamil.atlassian.net/browse/ORHM-5">ORHM-5: Admin - System User Management &amp; Role Provisioning</a></li>
    </ul>
    """
    create_confluence_page(SPACE_ID, "PRD - OrangeHRM Recruitment & Candidate Onboarding Specification", recruitment_html)

    # Confluence Page 3: Master Test Strategy
    strategy_html = """
    <h2>OrangeHRM Enterprise QA Master Test Strategy &amp; Traceability Matrix</h2>
    <p><strong>Prepared By:</strong> Lead QA Automation Engineer | <strong>Framework:</strong> Playwright for Java (POM)</p>
    
    <hr/>
    <h3>1. Test Automation Architecture</h3>
    <ul>
      <li><strong>Language &amp; Runner:</strong> Java 17+, JUnit 5, AssertJ, Maven.</li>
      <li><strong>Design Pattern:</strong> Strict Page Object Model (POM) under <code>src/main/java/com/orangehrm/pages/</code>.</li>
      <li><strong>Diagnostics:</strong> Automatic Playwright Trace recording (<code>target/traces/</code>), browser console logs (<code>target/logs/</code>), and full-page screenshots on failure.</li>
      <li><strong>AI Integration:</strong> GitHub Copilot Agent Mode with Model Context Protocol (MCP) connecting Jira Cloud and Confluence.</li>
    </ul>

    <h3>2. Module Test Coverage Matrix</h3>
    <table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%;">
      <thead>
        <tr style="background-color:#f4f5f7;">
          <th>Module</th>
          <th>Jira Epics / Stories</th>
          <th>Confluence PRD Reference</th>
          <th>Automated Test Class</th>
          <th>Coverage Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Auth &amp; Login</strong></td>
          <td>SYS-AUTH</td>
          <td>Security Architecture Spec</td>
          <td><code>LoginTest.java</code></td>
          <td><span style="color:#00875a; font-weight:bold;">100% Automated</span></td>
        </tr>
        <tr>
          <td><strong>Leave Management</strong></td>
          <td>ORHM-1</td>
          <td>Leave Entitlement PRD</td>
          <td><code>LeaveTest.java</code></td>
          <td><span style="color:#00875a; font-weight:bold;">100% Automated</span></td>
        </tr>
        <tr>
          <td><strong>PIM Employees</strong></td>
          <td>ORHM-2, ORHM-3</td>
          <td>PIM Specification PRD</td>
          <td><code>EmployeeTest.java</code></td>
          <td><span style="color:#ffab00; font-weight:bold;">In Progress</span></td>
        </tr>
        <tr>
          <td><strong>Recruitment</strong></td>
          <td>ORHM-4, ORHM-5</td>
          <td>Recruitment PRD</td>
          <td><code>RecruitmentTest.java</code></td>
          <td><span style="color:#ffab00; font-weight:bold;">Planned</span></td>
        </tr>
      </tbody>
    </table>
    """
    create_confluence_page(SPACE_ID, "QA Master Test Strategy & Traceability Matrix - OrangeHRM", strategy_html)

    print("\n[SUCCESS] Seeding of Expanded Tickets and Confluence Pages Complete!")

if __name__ == '__main__':
    main()

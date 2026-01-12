#!/usr/bin/env python3
"""Test with the actual full response from test_agent.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import FileWriter

# Actual full response from your test output
full_response = """Here's the structured analysis for the given requirement, formatted as requested:

---

**File: `analysis/requirements.md`**
```markdown
# Requirement Analysis: REST API Endpoint for "Hello World"

## 1. Detailed Requirements Breakdown
### Functional Requirements:
- **Endpoint Specification**:
  - Method: `GET` 
  - Path: `/api/hello` (or similar, to be confirmed)
  - Response: `Hello World` (plain text or JSON format, e.g., `{"message": "Hello World"}`)
- **HTTP Status Codes**:
  - Success: `200 OK` 
  - Errors: `404 Not Found` (if path is invalid), `500 Internal Server Error` (if backend fails)

### Non-Functional Requirements:
- **Performance**: Response time < 100ms (for initial implementation).
- **Scalability**: Endpoint should handle at least 100 requests/second (scalable via load balancing if needed).
- **Security**: No authentication required for this endpoint (public access).
- **Documentation**: Swagger/OpenAPI specs for the endpoint.

### Assumptions:
- The API will be hosted on a cloud service (e.g., AWS, Azure) or internal server.
- Initial implementation uses a lightweight framework (e.g., Flask, Express.js, or Spring Boot).

### Open Questions:
1. Should the response be plain text or JSON?
2. Are there any logging or monitoring requirements?
3. Is this endpoint part of a larger API, or is it standalone?

---

## 2. User Stories with Acceptance Criteria
### User Story 1: As a developer, I want to create a REST API endpoint that returns "Hello World" so that I can test basic API functionality.
**Acceptance Criteria**:
- The endpoint `/api/hello` returns "Hello World" when accessed via `GET`.
- Response status code is `200 OK`.
- Response format is plain text (or JSON, if specified).
- Endpoint is accessible without authentication.

### User Story 2: As a QA engineer, I want to validate the API response so that I can ensure correctness.
**Acceptance Criteria**:
- Automated test (e.g., Postman or unit test) confirms the response matches "Hello World".
- Test covers error cases (e.g., invalid path returns `404`).

---

## 3. Business Value Assessment
- **High Priority**: This is a foundational requirement for API development, enabling future endpoints.
- **Stakeholder Impact**:
  - Developers: Quick validation of API setup.
  - Product Owners: Milestone for API development.
- **Risk Mitigation**: Low-risk task; serves as a proof of concept for larger API projects.

---

## 4. Dependencies and Risks
### Dependencies:
- Availability of development environment (e.g., IDE, server).
- Framework/library selection (e.g., Flask, Express.js).

### Risks:
- **Technical Risk**: Framework compatibility issues (mitigated by using well-documented tools).
- **Scope Creep**: Additional features (e.g., authentication) may be requested later (mitigated by clear scope definition).

---

## 5. Jira Ticket Structure Recommendations
### Ticket 1: [API] Create "Hello World" Endpoint
- **Type**: Task
- **Priority**: High
- **Story Points**: 2
- **Assignee**: Backend Developer
- **Labels**: `api`, `rest`, `hello-world` 
- **Acceptance Criteria** (as above):
  - Endpoint returns "Hello World" with `200 OK`.
  - Tests pass for success and error cases.

### Sub-tasks:
1. Set up development environment.
2. Implement endpoint in chosen framework.
3. Write unit tests.
4. Deploy to staging for validation.

---
```

**File: `analysis/user_stories.md`**
```markdown
# User Stories for "Hello World" REST API

## Story 1: Basic Endpoint Implementation
**Title**: Create `/api/hello` endpoint returning "Hello World"
**Description**: As a developer, I want a simple API endpoint to return "Hello World" so that I can verify API functionality.
**Acceptance Criteria**:
- Endpoint `/api/hello` returns "Hello World" via `GET`.
- Response status: `200 OK`.
- No authentication required.

## Story 2: Testing and Validation
**Title**: Validate API response with automated tests
**Description**: As a QA engineer, I want to test the endpoint to ensure it meets requirements.
**Acceptance Criteria**:
- Postman collection includes test for `/api/hello`.
- Unit test confirms correct response.
- Error cases (e.g., `404`) are tested.
```

---

### Notes:
- The analysis assumes a minimal scope; adjust if additional requirements (e.g., logging, metrics) are needed.
- For Jira, use **Epic** if this is part of a larger API project.
"""

def main():
    print("="*80)
    print("Testing Full Response Extraction")
    print("="*80)
    
    writer = FileWriter("/tmp/test_full")
    
    # Extract files
    files = writer.extract_file_structure(full_response)
    
    print(f"\nExtracted {len(files)} files:\n")
    
    for filename, content in files.items():
        print("="*80)
        print(f"File: {filename}")
        print(f"Content length: {len(content)} characters")
        print(f"Content lines: {len(content.splitlines())} lines")
        print("-"*80)
        print("FULL CONTENT:")
        print(content)
        print("="*80)
        print()
    
    # Check if content is complete
    expected_in_requirements = [
        "Detailed Requirements Breakdown",
        "User Stories with Acceptance Criteria",
        "Business Value Assessment",
        "Dependencies and Risks",
        "Jira Ticket Structure"
    ]
    
    if 'analysis/requirements.md' in files:
        req_content = files['analysis/requirements.md']
        print("\nChecking requirements.md completeness:")
        for expected in expected_in_requirements:
            if expected in req_content:
                print(f"  ✓ Contains: {expected}")
            else:
                print(f"  ✗ Missing: {expected}")
    
    if 'analysis/user_stories.md' in files:
        stories_content = files['analysis/user_stories.md']
        print("\nChecking user_stories.md completeness:")
        expected_in_stories = ["Story 1", "Story 2", "Testing and Validation"]
        for expected in expected_in_stories:
            if expected in stories_content:
                print(f"  ✓ Contains: {expected}")
            else:
                print(f"  ✗ Missing: {expected}")

if __name__ == "__main__":
    main()

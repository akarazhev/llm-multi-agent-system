# External Integrations

## Overview

This document describes the integration with external systems: Jira, Confluence, and GitLab.

---

## Jira Integration

### Purpose
Create and manage project tickets, epics, stories, and tasks automatically based on requirements analysis.

### API Client
- **Library**: `jira` (Python)
- **Authentication**: API Token or OAuth 2.0
- **Base URL**: Configurable (Jira Cloud or Server)

### Key Functionality

#### 1. Project Management
```python
def create_project(name: str, key: str, project_type: str) -> Project
def get_project(project_key: str) -> Project
def list_projects() -> List[Project]
```

#### 2. Epic Management
```python
def create_epic(project_key: str, summary: str, description: str) -> Issue
def link_epic_to_story(epic_key: str, story_key: str) -> bool
def get_epic_stories(epic_key: str) -> List[Issue]
```

#### 3. Story/Task Creation
```python
def create_story(
    project_key: str,
    summary: str,
    description: str,
    acceptance_criteria: List[str],
    epic_key: str = None
) -> Issue

def create_task(
    project_key: str,
    summary: str,
    description: str,
    parent_key: str = None
) -> Issue
```

#### 4. Issue Management
```python
def update_issue_status(issue_key: str, status: str) -> bool
def add_comment(issue_key: str, comment: str) -> bool
def link_issues(issue_key_1: str, issue_key_2: str, link_type: str) -> bool
def assign_issue(issue_key: str, assignee: str) -> bool
```

### Integration Points

**Business Analyst Agent** uses Jira to:
- Create epics from high-level requirements
- Generate user stories with acceptance criteria
- Create tasks from task breakdown

**Developer Agent** uses Jira to:
- Update story status during development
- Link code commits to issues
- Add technical comments

**QA Agent** uses Jira to:
- Create test-related tasks
- Link test results to stories
- Report defects as bugs

### Configuration

```yaml
jira:
  url: "https://your-domain.atlassian.net"
  username: "your-email@example.com"
  api_token: "${JIRA_API_TOKEN}"
  project_key: "PROJ"
  default_issue_type: "Story"
```

### Error Handling

- **Rate Limiting**: Implement exponential backoff
- **Authentication Errors**: Retry with token refresh
- **Validation Errors**: Log and return to agent for correction

---

## Confluence Integration

### Purpose
Automatically create and maintain project documentation in Confluence spaces.

### API Client
- **Library**: `atlassian-python-api`
- **Authentication**: API Token or OAuth 2.0
- **Base URL**: Configurable (Confluence Cloud or Server)

### Key Functionality

#### 1. Space Management
```python
def create_space(key: str, name: str, description: str) -> Space
def get_space(space_key: str) -> Space
def list_spaces() -> List[Space]
```

#### 2. Page Management
```python
def create_page(
    space_key: str,
    title: str,
    content: str,
    parent_id: str = None
) -> Page

def update_page(
    page_id: str,
    title: str,
    content: str,
    version: int
) -> Page

def get_page(page_id: str) -> Page
def delete_page(page_id: str) -> bool
```

#### 3. Content Structure
```python
def create_page_hierarchy(
    space_key: str,
    structure: Dict[str, Any]
) -> List[Page]

def add_attachment(
    page_id: str,
    file_path: str,
    filename: str
) -> bool
```

### Integration Points

**Technical Writer Agent** uses Confluence to:
- Create documentation spaces
- Generate API documentation pages
- Create user guides and tutorials
- Document architecture decisions

**Business Analyst Agent** uses Confluence to:
- Document requirements
- Create business analysis pages
- Document user stories

**Developer Agent** uses Confluence to:
- Document architecture
- Create technical specifications
- Document design decisions

### Content Format

Confluence uses Storage Format (similar to HTML) or Markdown (with conversion).

Example page structure:
```markdown
# Project Documentation

## Overview
[Generated content]

## Architecture
[Architecture diagrams and descriptions]

## API Documentation
[API endpoints and examples]
```

### Configuration

```yaml
confluence:
  url: "https://your-domain.atlassian.net"
  username: "your-email@example.com"
  api_token: "${CONFLUENCE_API_TOKEN}"
  default_space_key: "PROJ"
  content_format: "storage"  # or "wiki"
```

### Error Handling

- **Rate Limiting**: Implement exponential backoff
- **Content Size**: Split large pages into multiple pages
- **Version Conflicts**: Handle with merge or version increment

---

## GitLab Integration

### Purpose
Manage source code repositories, commits, branches, and merge requests automatically.

### API Client
- **Library**: `python-gitlab`
- **Authentication**: Personal Access Token or OAuth
- **Base URL**: Configurable (GitLab.com or self-hosted)

### Key Functionality

#### 1. Repository Management
```python
def create_repository(
    name: str,
    description: str,
    visibility: str = "private"
) -> Project

def get_repository(project_id: int) -> Project
def list_repositories() -> List[Project]
```

#### 2. Branch Management
```python
def create_branch(
    project_id: int,
    branch_name: str,
    ref: str = "main"
) -> Branch

def get_branch(project_id: int, branch_name: str) -> Branch
def list_branches(project_id: int) -> List[Branch]
```

#### 3. Commit Management
```python
def create_commit(
    project_id: int,
    branch: str,
    commit_message: str,
    actions: List[Dict[str, Any]]
) -> Commit

def get_commit(project_id: int, sha: str) -> Commit
def list_commits(project_id: int, branch: str) -> List[Commit]
```

#### 4. Merge Request Management
```python
def create_merge_request(
    project_id: int,
    source_branch: str,
    target_branch: str,
    title: str,
    description: str
) -> MergeRequest

def update_merge_request(
    project_id: int,
    mr_id: int,
    **kwargs
) -> MergeRequest

def get_merge_request(project_id: int, mr_id: int) -> MergeRequest
```

#### 5. CI/CD Pipeline
```python
def trigger_pipeline(
    project_id: int,
    ref: str,
    variables: Dict[str, str] = None
) -> Pipeline

def get_pipeline(project_id: int, pipeline_id: int) -> Pipeline
def list_pipelines(project_id: int) -> List[Pipeline]
```

### Integration Points

**Developer Agent** uses GitLab to:
- Create repositories for new projects
- Commit generated code
- Create feature branches
- Create merge requests

**DevOps Agent** uses GitLab to:
- Configure CI/CD pipelines
- Set up repository structure
- Manage deployment configurations

**QA Agent** uses GitLab to:
- Link test results to commits
- Create test-related branches
- Document test coverage

### Commit Strategy

1. **Initial Commit**: Project structure and configuration
2. **Feature Commits**: Logical feature units
3. **Documentation Commits**: Separate commits for docs
4. **Test Commits**: Test files with related code

### Configuration

```yaml
gitlab:
  url: "https://gitlab.com"  # or self-hosted URL
  private_token: "${GITLAB_PRIVATE_TOKEN}"
  default_branch: "main"
  default_visibility: "private"
  group_id: 123  # Optional: default group
```

### Error Handling

- **Rate Limiting**: Implement exponential backoff
- **Merge Conflicts**: Detect and notify for manual resolution
- **Large Files**: Use Git LFS for large files
- **Authentication**: Token refresh mechanism

---

## Integration Architecture

### Integration Layer

```
┌─────────────────────────────────────┐
│      Agent Layer                    │
│  (Business, Developer, QA, etc.)    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Integration Service Layer         │
│  ┌──────────┐ ┌──────────┐ ┌──────┐│
│  │  Jira    │ │Confluence│ │GitLab││
│  │  Client  │ │  Client  │ │Client││
│  └──────────┘ └──────────┘ └──────┘│
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      External APIs                  │
│  (Jira, Confluence, GitLab)         │
└─────────────────────────────────────┘
```

### Common Patterns

#### 1. Retry Logic
All integrations implement retry with exponential backoff:
```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def api_call():
    # API call implementation
```

#### 2. Error Handling
```python
try:
    result = api_call()
except RateLimitError:
    # Wait and retry
except AuthenticationError:
    # Refresh token and retry
except ValidationError:
    # Log and return error to agent
```

#### 3. Caching
Cache frequently accessed data:
- Project/space information
- Repository metadata
- User information

### Testing

#### Mock Services
- Use mock servers for testing
- Testcontainers for integration testing
- Fixtures for unit testing

#### Test Scenarios
1. **Happy Path**: Successful API calls
2. **Error Handling**: Rate limits, auth errors
3. **Edge Cases**: Large payloads, missing data
4. **Concurrency**: Multiple simultaneous requests

---

## Security Considerations

### API Keys
- Store in environment variables
- Use secrets management (Vault) in production
- Rotate keys regularly
- Never commit keys to repository

### Authentication
- Use OAuth 2.0 where possible
- Implement token refresh
- Secure token storage

### Network Security
- Use HTTPS for all API calls
- Validate SSL certificates
- Implement request signing if required

---

## Monitoring

### Metrics
- API call success rate
- API response times
- Rate limit hits
- Error rates by type

### Logging
- Log all API calls (without sensitive data)
- Log errors with context
- Track integration usage per agent

### Alerts
- High error rates
- Rate limit approaching
- Authentication failures
- Service unavailability

---

## Future Enhancements

1. **Additional Integrations**
   - Slack/Teams for notifications
   - GitHub as alternative to GitLab
   - Azure DevOps integration
   - Linear for issue tracking

2. **Advanced Features**
   - Webhook support for real-time updates
   - Batch operations for efficiency
   - GraphQL APIs where available
   - Real-time synchronization

3. **Optimization**
   - Parallel API calls
   - Request batching
   - Smart caching strategies
   - Connection pooling

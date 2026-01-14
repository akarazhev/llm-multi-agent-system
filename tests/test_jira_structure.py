"""Test parsing of Jira structure markdown with nested code blocks"""
from src.utils.file_writer import FileWriter
import tempfile

def test_jira_structure_parsing():
    """Test parsing the actual Jira structure response that was truncated"""
    
    # This is the EXACT format from the agent response
    text = """### File: `analysis/jira_structure.md`
```markdown
# Jira Ticket Structure Recommendations

## Epic Structure
```
API Foundation
├── Hello World Endpoint (Current Focus)
│   ├── [DEV-1] Create Hello World endpoint
│   ├── [DEV-2] Add API documentation
│   ├── [DEV-3] Implement performance monitoring
│   └── [DEV-4] Setup CI/CD pipeline for endpoint
└── Future API Development
    ├── [DEV-5] Authentication Service
    └── [DEV-6] Data Access Layer
```

## Ticket Templates

### Template 1: Feature Ticket (Hello World Endpoint)
```json
{
  "fields": {
    "project": {"key": "API"},
    "summary": "Create GET /api/hello endpoint returning 'Hello World'",
    "description": "As a developer integrating with the API,\\nI want a simple endpoint that returns 'Hello World',\\nSo that I can verify the API is working correctly.",
    "issuetype": {"name": "Task"},
    "priority": {"name": "High"},
    "labels": ["api", "hello-world", "foundation"],
    "customfield_10016": 2,
    "components": [{"name": "Backend API"}]
  }
}
```

### Template 2: Documentation Ticket
```json
{
  "fields": {
    "project": {"key": "API"},
    "summary": "Document /api/hello endpoint in Swagger",
    "description": "Add comprehensive Swagger documentation for the Hello World endpoint",
    "issuetype": {"name": "Task"},
    "priority": {"name": "Medium"}
  }
}
```

## Workflow States
1. **To Do** → Initial state
2. **In Progress** → Development started
3. **Code Review** → PR submitted
4. **Testing** → QA validation
5. **Done** → Deployed to production

## Acceptance Criteria Template
- [ ] Endpoint returns 'Hello World' with status 200
- [ ] Response time < 100ms
- [ ] Swagger documentation complete
- [ ] Unit tests pass
- [ ] Integration tests pass
```

This is the complete structure.
"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        writer = FileWriter(tmpdir)
        files = writer.extract_file_structure(text)
        
        print(f"\nFound {len(files)} files:")
        for filename, content in files.items():
            print(f"  - {filename} ({len(content)} chars)")
            print(f"    First 100 chars: {content[:100]}")
            print(f"    Last 100 chars: ...{content[-100:]}")
        
        # Check file was extracted
        assert 'analysis/jira_structure.md' in files, f"jira_structure.md not found. Files: {list(files.keys())}"
        
        content = files['analysis/jira_structure.md']
        
        # Check all sections are present
        assert '# Jira Ticket Structure Recommendations' in content
        assert '## Epic Structure' in content
        assert 'API Foundation' in content
        assert '[DEV-1] Create Hello World endpoint' in content
        
        # Check the nested code blocks are preserved
        assert '## Ticket Templates' in content
        assert '### Template 1: Feature Ticket' in content
        assert '```json' in content or '"fields"' in content  # JSON block should be there
        
        # Check Template 2 is present
        assert '### Template 2: Documentation Ticket' in content
        
        # Check workflow section
        assert '## Workflow States' in content
        assert '**To Do**' in content
        assert '**Done**' in content
        
        # Check acceptance criteria
        assert '## Acceptance Criteria Template' in content
        assert 'Endpoint returns' in content
        
        print(f"\n✅ Test passed!")
        print(f"\nFull content length: {len(content)} chars")
        print(f"\nFull content:\n{content}")


if __name__ == '__main__':
    test_jira_structure_parsing()

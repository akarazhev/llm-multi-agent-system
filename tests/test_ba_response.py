"""Test parsing of Business Analyst response with multiple markdown files"""
from src.utils.file_writer import FileWriter
import tempfile

def test_ba_multi_markdown_response():
    """Test parsing BA response with multiple markdown documentation files"""
    
    # This is the actual format from the BA agent
    text = """Here's the complete analysis formatted as requested:

```markdown:analysis/requirements.md
# REST API "Hello World" Endpoint - Requirements Analysis

## Executive Summary
This document provides analysis.

## Business Context
Problem statement and goals.
```

```markdown:analysis/user_stories.md
# User Stories for "Hello World" API Endpoint

## User Story 1: Basic Endpoint Implementation
**Title**: As a developer, I want endpoint.

**User Story**:
```
As a developer,
I want to access endpoint,
So that I can verify it works.
```

**Acceptance Criteria**:
- Given the API server is running
- When a GET request is made
- Then response should be 200
```

This analysis provides a complete foundation.
"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        writer = FileWriter(tmpdir)
        files = writer.extract_file_structure(text)
        
        print(f"\nFound {len(files)} files:")
        for filename in files.keys():
            print(f"  - {filename} ({len(files[filename])} chars)")
        
        # Check both files were extracted
        assert 'analysis/requirements.md' in files, f"requirements.md not found. Files: {list(files.keys())}"
        assert 'analysis/user_stories.md' in files, f"user_stories.md not found. Files: {list(files.keys())}"
        
        # Check requirements.md content
        req_content = files['analysis/requirements.md']
        assert '# REST API "Hello World" Endpoint' in req_content
        assert '## Executive Summary' in req_content
        assert '## Business Context' in req_content
        
        # Check user_stories.md content
        story_content = files['analysis/user_stories.md']
        assert '# User Stories' in story_content
        assert '## User Story 1' in story_content
        assert 'As a developer' in story_content
        assert '**Acceptance Criteria**:' in story_content
        
        # The critical check - nested code block should be preserved
        assert 'As a developer,' in story_content
        assert 'I want to access endpoint,' in story_content
        
        print(f"\n✅ Test passed!")
        print(f"requirements.md: {len(req_content)} chars")
        print(f"user_stories.md: {len(story_content)} chars")
        print(f"\nuser_stories.md content:\n{story_content}")


if __name__ == '__main__':
    test_ba_multi_markdown_response()

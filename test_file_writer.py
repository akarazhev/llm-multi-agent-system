#!/usr/bin/env python3
"""Test the FileWriter's ability to parse LLM responses"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils import FileWriter

# Sample LLM response in the format we're seeing
sample_response = """Here's the structured analysis in markdown format:

File: `analysis/requirements_breakdown.md` 
```markdown
# REST API Endpoint - Hello World

## 1. Requirements Breakdown
**Functional Requirements:**
- Create a new REST API endpoint
- Endpoint must respond to HTTP GET requests
```

File: `analysis/user_stories.md` 
```markdown
# User Stories

## Story 1: Basic Endpoint Implementation
**As a** developer
**I want** a simple REST endpoint
```

File: `analysis/business_value.md` 
```markdown
# Business Value Assessment

**Value:**
- Low business value (proof of concept)
```
"""

def test_file_extraction():
    """Test that FileWriter can extract files from LLM response"""
    writer = FileWriter("/tmp/test_workspace")
    
    # Test extract_file_structure
    files = writer.extract_file_structure(sample_response)
    
    print("="*80)
    print("File Extraction Test")
    print("="*80)
    print(f"\nFound {len(files)} files:\n")
    
    for filename, content in files.items():
        print(f"File: {filename}")
        print(f"Content length: {len(content)} chars")
        print(f"First 100 chars: {content[:100]}...")
        print("-"*80)
    
    # Verify we got the expected files
    expected_files = [
        'analysis/requirements_breakdown.md',
        'analysis/user_stories.md',
        'analysis/business_value.md'
    ]
    
    for expected in expected_files:
        if expected in files:
            print(f"✓ Found: {expected}")
        else:
            print(f"✗ Missing: {expected}")
            return False
    
    print("\n" + "="*80)
    print("✓ All tests passed!")
    print("="*80)
    return True

if __name__ == "__main__":
    success = test_file_extraction()
    sys.exit(0 if success else 1)

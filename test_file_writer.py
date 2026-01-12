#!/usr/bin/env python3
"""Test the FileWriter's ability to parse LLM responses"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils import FileWriter

# Sample LLM response in the format we're seeing (with bold)
sample_response_bold = """Here's the structured analysis:

**File: `analysis/requirements.md`**
```markdown
# Requirement Analysis

## 1. Detailed Requirements Breakdown
- Endpoint Specification
- HTTP Status Codes
```

**File: `analysis/user_stories.md`**
```markdown
# User Stories

## Story 1: Basic Endpoint
**As a** developer
```
"""

# Sample LLM response without bold
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
    
    all_passed = True
    
    # Test 1: Bold format
    print("="*80)
    print("Test 1: Bold Format (**File: `filename`**)")
    print("="*80)
    files_bold = writer.extract_file_structure(sample_response_bold)
    print(f"\nFound {len(files_bold)} files:\n")
    
    for filename, content in files_bold.items():
        print(f"File: {filename}")
        print(f"Content length: {len(content)} chars")
        print(f"First 80 chars: {content[:80]}...")
        print("-"*80)
    
    expected_bold = ['analysis/requirements.md', 'analysis/user_stories.md']
    for expected in expected_bold:
        if expected in files_bold:
            print(f"✓ Found: {expected}")
        else:
            print(f"✗ Missing: {expected}")
            all_passed = False
    
    # Test 2: Regular format
    print("\n" + "="*80)
    print("Test 2: Regular Format (File: `filename`)")
    print("="*80)
    files = writer.extract_file_structure(sample_response)
    print(f"\nFound {len(files)} files:\n")
    
    for filename, content in files.items():
        print(f"File: {filename}")
        print(f"Content length: {len(content)} chars")
        print(f"First 80 chars: {content[:80]}...")
        print("-"*80)
    
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
            all_passed = False
    
    print("\n" + "="*80)
    if all_passed:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed!")
    print("="*80)
    return all_passed

if __name__ == "__main__":
    success = test_file_extraction()
    sys.exit(0 if success else 1)

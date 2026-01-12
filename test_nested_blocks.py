#!/usr/bin/env python3
"""Test handling of nested code blocks in markdown files"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.utils import FileWriter

# Sample with nested code blocks (like README with usage examples)
nested_blocks_response = """Here's a complete implementation:

File: `factorial.py` 
```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

File: `README.md` 
```markdown
# Factorial Calculator

## Usage

```python
from factorial import factorial
result = factorial(5)
```

## Features
- Simple implementation
- Recursive approach
```

File: `test.py`
```python
import unittest
from factorial import factorial

class TestFactorial(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(factorial(5), 120)
```
"""

def test_nested_blocks():
    """Test that nested code blocks are handled correctly"""
    writer = FileWriter("/tmp/test_nested")
    
    files = writer.extract_file_structure(nested_blocks_response)
    
    print("="*80)
    print("Nested Code Blocks Test")
    print("="*80)
    print(f"\nExtracted {len(files)} files:\n")
    
    for filename, content in files.items():
        lines = content.count('\n') + 1
        has_nested = '```' in content
        print(f"File: {filename}")
        print(f"  Lines: {lines}")
        print(f"  Has nested blocks: {has_nested}")
        print(f"  Content preview (first 100 chars): {content[:100]}...")
        print("-"*80)
    
    # Validate README.md has the nested code block
    if 'README.md' in files:
        readme_content = files['README.md']
        if '```python' in readme_content and 'from factorial import factorial' in readme_content:
            print("\n✓ README.md contains nested code block correctly!")
        else:
            print("\n✗ README.md missing nested code block!")
            print(f"README content:\n{readme_content}")
            return False
    else:
        print("\n✗ README.md not found!")
        return False
    
    # Check all expected files
    expected = ['factorial.py', 'README.md', 'test.py']
    for exp in expected:
        if exp in files:
            print(f"✓ Found: {exp}")
        else:
            print(f"✗ Missing: {exp}")
            return False
    
    print("\n" + "="*80)
    print("✓ All tests passed!")
    print("="*80)
    return True

if __name__ == "__main__":
    success = test_nested_blocks()
    sys.exit(0 if success else 1)

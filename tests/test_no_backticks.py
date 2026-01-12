#!/usr/bin/env python3
"""Test File: path/to/file.py format without backticks"""
import sys
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.utils import FileWriter

# Sample with File: path (no backticks)
no_backticks_response = """Here's a complete implementation:

File: factorial/factorial.py
```python
def factorial(n):
    if n < 0:
        raise ValueError("Negative not allowed")
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

File: tests/test_factorial.py
```python
import unittest
from factorial.factorial import factorial

class TestFactorial(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(factorial(5), 120)
```

File: README.md
```markdown
# Factorial

Simple factorial implementation.

## Usage

```python
from factorial import factorial
result = factorial(5)
```
```
"""

def test_no_backticks():
    """Test that File: path format works without creating garbage files"""
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        writer = FileWriter(temp_dir)
        
        # Extract files
        files = writer.extract_file_structure(no_backticks_response)
        
        print("="*80)
        print("File: path/to/file.py Format Test (No Backticks)")
        print("="*80)
        print(f"\nExtracted {len(files)} files:\n")
        
        for filename, content in files.items():
            lines = content.count('\n') + 1
            print(f"File: {filename}")
            print(f"  Lines: {lines}")
            print(f"  First 80 chars: {content[:80]}...")
            print("-"*80)
        
        # Write files
        created_files = writer.write_code_blocks(
            no_backticks_response,
            task_id="test_no_backticks",
            agent_role="developer"
        )
        
        print(f"\nCreated {len(created_files)} files on disk")
        
        # Check directory for garbage files
        gen_dir = Path(temp_dir) / "generated" / "test_no_backticks" / "developer"
        if gen_dir.exists():
            all_files = list(gen_dir.rglob("*"))
            actual_files = [f for f in all_files if f.is_file()]
            
            print(f"\nActual files in directory: {len(actual_files)}")
            
            # List all files
            for f in actual_files:
                rel_path = f.relative_to(gen_dir)
                print(f"  - {rel_path}")
            
            # Check for garbage
            expected = ['factorial/factorial.py', 'tests/test_factorial.py', 'README.md']
            garbage_files = []
            
            for f in actual_files:
                rel_path = str(f.relative_to(gen_dir))
                # Check if it's not one of the expected files
                if not any(exp in rel_path for exp in ['factorial.py', 'test_factorial.py', 'README.md']):
                    garbage_files.append(rel_path)
            
            if garbage_files:
                print(f"\n✗ FAIL: Found {len(garbage_files)} garbage files:")
                for g in garbage_files:
                    print(f"  - {g}")
                return False
            else:
                print("\n✓ PASS: No garbage files found!")
            
            # Verify expected files
            print("\nExpected files:")
            for exp in expected:
                found = any(exp in str(f) for f in actual_files)
                status = "✓" if found else "✗"
                print(f"  {status} {exp}")
                if not found:
                    return False
        
        print("\n" + "="*80)
        print("✓ All tests passed!")
        print("="*80)
        return True
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    success = test_no_backticks()
    sys.exit(0 if success else 1)

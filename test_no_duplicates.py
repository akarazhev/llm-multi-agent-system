#!/usr/bin/env python3
"""Test that no duplicate files are created"""
import sys
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.utils import FileWriter

# Sample response with File: `filename` format
sample_response = """Here's a complete implementation following best practices:

File: `factorial.py` 
```python
import logging

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Negative numbers not allowed")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
```

File: `test_factorial.py` 
```python
import unittest
from factorial import factorial

class TestFactorial(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(factorial(5), 120)
```

File: `README.md` 
```markdown
# Factorial Calculator
A simple factorial implementation.
```
"""

def test_no_duplicates():
    """Test that write_code_blocks creates only the expected files"""
    
    # Create temporary workspace
    temp_dir = tempfile.mkdtemp()
    
    try:
        writer = FileWriter(temp_dir)
        
        # Write files using write_code_blocks
        created_files = writer.write_code_blocks(
            sample_response,
            task_id="test_task",
            agent_role="developer"
        )
        
        print("="*80)
        print("File Creation Test - No Duplicates")
        print("="*80)
        print(f"\nCreated {len(created_files)} files:\n")
        
        for file_path in created_files:
            rel_path = Path(file_path).relative_to(temp_dir)
            file_size = Path(file_path).stat().st_size
            print(f"  ✓ {rel_path} ({file_size} bytes)")
        
        # Check that only expected files were created
        expected_files = ['factorial.py', 'test_factorial.py', 'README.md']
        
        print("\n" + "-"*80)
        print("Validation:")
        print("-"*80)
        
        # Get all files in the generated directory
        gen_dir = Path(temp_dir) / "generated" / "test_task" / "developer"
        if gen_dir.exists():
            all_files = list(gen_dir.rglob("*"))
            actual_files = [f for f in all_files if f.is_file()]
            
            print(f"\nTotal files in directory: {len(actual_files)}")
            
            # Check for unwanted files
            unwanted_patterns = ['code_*.md', 'code_*.txt', '*.md.md']
            unwanted_found = []
            
            for file in actual_files:
                filename = file.name
                # Check if it's an unwanted file
                if (filename.startswith('code_') and 
                    (filename.endswith('.md') or filename.endswith('.txt'))):
                    unwanted_found.append(filename)
            
            if unwanted_found:
                print(f"\n✗ FAIL: Found {len(unwanted_found)} unwanted duplicate files:")
                for f in unwanted_found:
                    print(f"  - {f}")
                return False
            else:
                print("\n✓ PASS: No duplicate files found!")
                
            # Verify expected files exist
            print("\nExpected files:")
            for expected in expected_files:
                found = any(expected in str(f) for f in actual_files)
                status = "✓" if found else "✗"
                print(f"  {status} {expected}")
                if not found:
                    return False
        
        print("\n" + "="*80)
        print("✓ All tests passed - No duplicates created!")
        print("="*80)
        return True
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    success = test_no_duplicates()
    sys.exit(0 if success else 1)

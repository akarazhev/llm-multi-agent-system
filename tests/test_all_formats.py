#!/usr/bin/env python3
"""Comprehensive test for all supported file formats"""
import sys
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.utils import FileWriter

def test_all_formats():
    """Test all supported LLM output formats"""
    
    formats = {
        "Colon format (```language:filename)": """
```python:src/main.py
def main():
    print("Hello")
```
""",
        "File with backticks (File: `filename`)": """
File: `src/utils.py`
```python
def helper():
    return True
```
""",
        "File without backticks (File: filename)": """
File: src/config.py
```python
CONFIG = {"debug": True}
```
""",
        "Bold file with backticks (**File: `filename`**)": """
**File: `src/models.py`**
```python
class Model:
    pass
```
""",
        "Nested code blocks": """
File: `README.md`
```markdown
# Project

## Usage
```python
import main
main.run()
```
```
"""
    }
    
    temp_dir = tempfile.mkdtemp()
    all_passed = True
    
    try:
        writer = FileWriter(temp_dir)
        
        print("="*80)
        print("Comprehensive Format Test")
        print("="*80)
        
        for format_name, sample in formats.items():
            print(f"\n{format_name}:")
            print("-"*80)
            
            files = writer.extract_file_structure(sample)
            
            if files:
                for filename, content in files.items():
                    print(f"  ✓ Extracted: {filename} ({len(content)} chars)")
            else:
                print(f"  ✗ FAILED: No files extracted")
                all_passed = False
        
        print("\n" + "="*80)
        if all_passed:
            print("✓ All formats work correctly!")
        else:
            print("✗ Some formats failed!")
        print("="*80)
        
        return all_passed
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    success = test_all_formats()
    sys.exit(0 if success else 1)

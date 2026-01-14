"""Test markdown files with nested code blocks"""
from src.utils.file_writer import FileWriter
import tempfile

def test_markdown_with_nested_code_blocks():
    """Test that markdown files with nested code blocks are extracted correctly"""
    
    text = """File: README.md
```markdown
# Factorial Calculator

A simple Python implementation of a factorial calculator with proper error handling and logging.

## Features
- Calculates factorial of non-negative integers
- Input validation and error handling
- Comprehensive logging
- Unit tests with pytest

## Usage

```python
from factorial import factorial

result = factorial(5)  # Returns 120
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

```bash
pytest test_factorial.py -v
```
```
"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        writer = FileWriter(tmpdir)
        files = writer.extract_file_structure(text)
        
        assert 'README.md' in files, f"README.md not found. Files: {list(files.keys())}"
        
        content = files['README.md']
        
        # Check that all sections are present
        assert '# Factorial Calculator' in content
        assert '## Features' in content
        assert '## Usage' in content
        assert '## Installation' in content
        assert '## Running Tests' in content
        
        # Check that nested code blocks are preserved
        assert 'from factorial import factorial' in content
        assert 'pip install -r requirements.txt' in content
        assert 'pytest test_factorial.py -v' in content
        
        # Check length - should be complete, not truncated
        assert len(content) > 500, f"Content too short ({len(content)} chars), likely truncated"
        
        print(f"✅ Test passed! README.md extracted with {len(content)} characters")
        print(f"Contains all sections: Installation={('## Installation' in content)}, Running Tests={('## Running Tests' in content)}")


if __name__ == '__main__':
    test_markdown_with_nested_code_blocks()

"""
Comprehensive tests for file parser and writer functionality.
Tests all supported formats and edge cases.
"""
import pytest
from pathlib import Path
import tempfile
import shutil
from src.utils.file_writer import FileWriter


class TestFileWriter:
    """Test FileWriter parsing and writing functionality"""
    
    @pytest.fixture
    def temp_workspace(self):
        """Create a temporary workspace for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def file_writer(self, temp_workspace):
        """Create FileWriter instance"""
        return FileWriter(temp_workspace)
    
    def test_format_1_colon_syntax(self, file_writer):
        """Test ```language:filename format"""
        text = """
Here's the implementation:

```python:factorial.py
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
```

```python:test_factorial.py
def test_factorial():
    assert factorial(5) == 120
```
"""
        blocks = file_writer.parse_code_blocks(text)
        
        assert len(blocks) == 2
        assert blocks[0]['filename'] == 'factorial.py'
        assert 'def factorial(n):' in blocks[0]['content']
        assert blocks[1]['filename'] == 'test_factorial.py'
        assert 'def test_factorial():' in blocks[1]['content']
    
    def test_format_2_file_with_backticks(self, file_writer):
        """Test File: `filename` format"""
        text = """
File: `requirements.txt`
```
pytest>=7.0.0
coverage>=6.0.0
```

File: `setup.py`
```python
from setuptools import setup
setup(name='test')
```
"""
        files = file_writer.extract_file_structure(text)
        
        assert len(files) == 2
        assert 'requirements.txt' in files
        assert 'pytest>=7.0.0' in files['requirements.txt']
        assert 'coverage>=6.0.0' in files['requirements.txt']
        assert 'setup.py' in files
        assert 'from setuptools import setup' in files['setup.py']
    
    def test_format_3_file_without_backticks(self, file_writer):
        """Test File: filename format (no backticks)"""
        text = """
File: config.yaml
```yaml
database:
  host: localhost
  port: 5432
```

File: README.md
```markdown
# Project Title
This is a test project.
```
"""
        files = file_writer.extract_file_structure(text)
        
        assert len(files) == 2
        assert 'config.yaml' in files
        assert 'database:' in files['config.yaml']
        assert 'localhost' in files['config.yaml']
        assert 'README.md' in files
        assert '# Project Title' in files['README.md']
    
    def test_format_4_bold_file_marker(self, file_writer):
        """Test **File: `filename`** format"""
        text = """
**File: `app.py`**
```python
print("Hello, World!")
```

**File: `test.py`**
```python
def test_hello():
    pass
```
"""
        files = file_writer.extract_file_structure(text)
        
        assert len(files) == 2
        assert 'app.py' in files
        assert 'print("Hello, World!")' in files['app.py']
        assert 'test.py' in files
        assert 'def test_hello():' in files['test.py']
    
    def test_requirements_txt_bug(self, file_writer):
        """Test the specific bug case: requirements.txt with pytest>=7.0.0"""
        text = """
File: `requirements.txt`
```
pytest>=7.0.0
```
"""
        files = file_writer.extract_file_structure(text)
        
        assert len(files) == 1
        assert 'requirements.txt' in files
        # This is the critical test - should contain full line
        assert files['requirements.txt'] == 'pytest>=7.0.0'
        assert not files['requirements.txt'].startswith('>=')
    
    def test_multiline_content(self, file_writer):
        """Test files with multiple lines of content"""
        text = """
File: `app.py`
```python
import os
import sys

def main():
    print("Hello")
    print("World")
    return 0

if __name__ == "__main__":
    main()
```
"""
        files = file_writer.extract_file_structure(text)
        
        assert len(files) == 1
        assert 'app.py' in files
        content = files['app.py']
        assert 'import os' in content
        assert 'import sys' in content
        assert 'def main():' in content
        assert 'print("Hello")' in content
        assert 'print("World")' in content
        assert 'if __name__ == "__main__":' in content
    
    def test_nested_code_blocks_in_markdown(self, file_writer):
        """Test markdown files containing code blocks"""
        text = """
File: `README.md`
```markdown
# My Project

Here's how to use it:

\`\`\`python
import myproject
myproject.run()
\`\`\`

That's all!
```
"""
        files = file_writer.extract_file_structure(text)
        
        assert len(files) == 1
        assert 'README.md' in files
        content = files['README.md']
        assert '# My Project' in content
        assert 'import myproject' in content
        assert 'myproject.run()' in content
    
    def test_empty_lines_preserved(self, file_writer):
        """Test that empty lines are preserved in content"""
        text = """
File: `test.py`
```python
def func1():
    pass


def func2():
    pass
```
"""
        files = file_writer.extract_file_structure(text)
        
        assert len(files) == 1
        assert 'test.py' in files
        content = files['test.py']
        # Should have empty lines between functions
        assert '\n\n' in content
    
    def test_trailing_whitespace_handling(self, file_writer):
        """Test handling of trailing whitespace"""
        text = """
File: `app.py`
```python
print("test")   
```
"""
        files = file_writer.extract_file_structure(text)
        
        assert len(files) == 1
        assert 'app.py' in files
        # Content should be stripped but preserve internal whitespace
        content = files['app.py']
        assert content.strip() == 'print("test")'
    
    def test_multiple_files_in_sequence(self, file_writer):
        """Test parsing multiple files in sequence"""
        text = """
File: `file1.py`
```python
content1
```

File: `file2.py`
```python
content2
```

File: `file3.py`
```python
content3
```
"""
        files = file_writer.extract_file_structure(text)
        
        assert len(files) == 3
        assert files['file1.py'] == 'content1'
        assert files['file2.py'] == 'content2'
        assert files['file3.py'] == 'content3'
    
    def test_write_code_blocks(self, file_writer, temp_workspace):
        """Test writing code blocks to disk"""
        text = """
File: `app.py`
```python
print("Hello")
```

File: `requirements.txt`
```
pytest>=7.0.0
requests>=2.28.0
```
"""
        created_files = file_writer.write_code_blocks(text, "test_task", "test_agent")
        
        assert len(created_files) == 2
        
        # Check files were created
        for file_path in created_files:
            assert Path(file_path).exists()
        
        # Check content is correct
        app_file = [f for f in created_files if 'app.py' in f][0]
        req_file = [f for f in created_files if 'requirements.txt' in f][0]
        
        with open(app_file, 'r') as f:
            assert 'print("Hello")' in f.read()
        
        with open(req_file, 'r') as f:
            content = f.read()
            assert 'pytest>=7.0.0' in content
            assert 'requests>=2.28.0' in content
            # Critical: Should not have truncated content
            assert not content.startswith('>=')
    
    def test_special_characters_in_filename(self, file_writer):
        """Test handling of special characters in filenames"""
        text = """
File: `my-app.py`
```python
content
```

File: `test_file.py`
```python
content
```
"""
        files = file_writer.extract_file_structure(text)
        
        assert len(files) == 2
        assert 'my-app.py' in files
        assert 'test_file.py' in files
    
    def test_path_with_directories(self, file_writer):
        """Test files with directory paths"""
        text = """
File: `src/utils/helper.py`
```python
def helper():
    pass
```

File: `tests/test_helper.py`
```python
def test_helper():
    pass
```
"""
        files = file_writer.extract_file_structure(text)
        
        assert len(files) == 2
        assert 'src/utils/helper.py' in files
        assert 'tests/test_helper.py' in files
    
    def test_language_identifiers(self, file_writer):
        """Test various language identifiers"""
        text = """
```python:app.py
python_code
```

```javascript:script.js
js_code
```

```yaml:config.yml
yaml_code
```

```dockerfile:Dockerfile
docker_code
```
"""
        blocks = file_writer.parse_code_blocks(text)
        
        assert len(blocks) == 4
        assert blocks[0]['language'] == 'python'
        assert blocks[1]['language'] == 'javascript'
        assert blocks[2]['language'] == 'yaml'
        assert blocks[3]['language'] == 'dockerfile'
    
    def test_edge_case_empty_code_block(self, file_writer):
        """Test handling of empty code blocks"""
        text = """
File: `empty.py`
```python
```

File: `nonempty.py`
```python
content
```
"""
        files = file_writer.extract_file_structure(text)
        
        # Empty blocks should be skipped or handled gracefully
        assert 'nonempty.py' in files
        assert files['nonempty.py'] == 'content'
    
    def test_complex_real_world_example(self, file_writer):
        """Test a complex real-world example like the factorial output"""
        text = """
Here's a complete implementation following best practices:

File: `factorial.py`
```python
import logging
from typing import Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def factorial(n: int) -> Union[int, float]:
    \"\"\"Calculate factorial\"\"\"
    if n < 0:
        raise ValueError("Negative numbers not allowed")
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

File: `test_factorial.py`
```python
import pytest
from factorial import factorial

def test_factorial_basic():
    assert factorial(0) == 1
    assert factorial(5) == 120
```

File: `requirements.txt`
```
pytest>=7.0.0
```

File: `README.md`
```markdown
# Factorial Calculator

## Installation

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Usage

\`\`\`python
from factorial import factorial
result = factorial(5)
\`\`\`
```

## Key Features Implemented:

1. **Error Handling**: Validates input
2. **Testing**: Comprehensive test suite
"""
        files = file_writer.extract_file_structure(text)
        
        # Should extract all 4 files
        assert len(files) == 4
        
        # Check factorial.py
        assert 'factorial.py' in files
        assert 'def factorial(n: int)' in files['factorial.py']
        assert 'import logging' in files['factorial.py']
        
        # Check test_factorial.py
        assert 'test_factorial.py' in files
        assert 'def test_factorial_basic():' in files['test_factorial.py']
        
        # Check requirements.txt (THE CRITICAL TEST)
        assert 'requirements.txt' in files
        assert files['requirements.txt'] == 'pytest>=7.0.0'
        # Should NOT be truncated
        assert not files['requirements.txt'].startswith('>=')
        
        # Check README.md
        assert 'README.md' in files
        assert '# Factorial Calculator' in files['README.md']
        assert 'pip install -r requirements.txt' in files['README.md']


def test_file_writer_integration(tmp_path):
    """Integration test: parse and write files"""
    workspace = str(tmp_path)
    writer = FileWriter(workspace)
    
    text = """
File: `app.py`
```python
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
```

File: `requirements.txt`
```
pytest>=7.0.0
black>=23.0.0
mypy>=1.0.0
```

File: `tests/test_app.py`
```python
from app import main

def test_main():
    main()
```
"""
    
    created_files = writer.write_code_blocks(text, "integration_test", "test_agent")
    
    # Verify all files were created
    assert len(created_files) == 3
    
    # Verify content is correct
    for file_path in created_files:
        assert Path(file_path).exists()
        
        if 'requirements.txt' in file_path:
            with open(file_path, 'r') as f:
                content = f.read()
                # THE CRITICAL CHECK
                assert 'pytest>=7.0.0' in content
                assert 'black>=23.0.0' in content
                assert 'mypy>=1.0.0' in content
                # Should not be truncated
                lines = content.strip().split('\n')
                assert any('pytest' in line for line in lines)
                assert not any(line.startswith('>=') for line in lines)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class FileWriter:
    """Utility class to parse LLM responses and write files to disk"""
    
    def __init__(self, workspace_root: str, output_dir: str = "generated"):
        self.workspace_root = Path(workspace_root)
        self.output_dir = self.workspace_root / output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def parse_code_blocks(self, text: str) -> List[Dict[str, str]]:
        """
        Parse code blocks from markdown-formatted text.
        Returns list of dicts with 'language', 'filename', and 'content'.
        """
        code_blocks = []
        
        # Pattern to match fenced code blocks with optional filename
        # Supports: ```python, ```python:filename.py, ```filename.py
        pattern = r'```(?:(\w+)(?::([^\n]+))?)?\n(.*?)```'
        
        matches = re.finditer(pattern, text, re.DOTALL)
        
        for match in matches:
            language = match.group(1) or 'text'
            filename = match.group(2)
            content = match.group(3).strip()
            
            # Try to infer filename from content if not specified
            if not filename:
                filename = self._infer_filename(content, language)
            
            code_blocks.append({
                'language': language,
                'filename': filename,
                'content': content
            })
        
        return code_blocks
    
    def _infer_filename(self, content: str, language: str) -> str:
        """Infer filename from content or language"""
        # Try to find class or function names
        class_match = re.search(r'class\s+(\w+)', content)
        if class_match:
            name = class_match.group(1)
            return self._to_snake_case(name) + self._get_extension(language)
        
        func_match = re.search(r'def\s+(\w+)', content)
        if func_match:
            name = func_match.group(1)
            return name + self._get_extension(language)
        
        # Default naming
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f'code_{timestamp}{self._get_extension(language)}'
    
    def _to_snake_case(self, name: str) -> str:
        """Convert CamelCase to snake_case"""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    def _get_extension(self, language: str) -> str:
        """Get file extension for language"""
        extensions = {
            'python': '.py',
            'javascript': '.js',
            'typescript': '.ts',
            'tsx': '.tsx',
            'jsx': '.jsx',
            'java': '.java',
            'cpp': '.cpp',
            'c': '.c',
            'go': '.go',
            'rust': '.rs',
            'ruby': '.rb',
            'php': '.php',
            'html': '.html',
            'css': '.css',
            'scss': '.scss',
            'sql': '.sql',
            'yaml': '.yaml',
            'yml': '.yml',
            'json': '.json',
            'xml': '.xml',
            'markdown': '.md',
            'md': '.md',
            'bash': '.sh',
            'shell': '.sh',
            'dockerfile': 'Dockerfile',
            'docker': 'Dockerfile',
        }
        return extensions.get(language.lower(), '.txt')
    
    def write_code_blocks(
        self, 
        text: str, 
        task_id: str, 
        agent_role: str,
        base_path: Optional[str] = None
    ) -> List[str]:
        """
        Parse code blocks from text and write them to files.
        Returns list of created file paths.
        """
        code_blocks = self.parse_code_blocks(text)
        created_files = []
        
        if not code_blocks:
            logger.warning(f"No code blocks found in response for task {task_id}")
            return created_files
        
        # Determine output directory
        if base_path:
            output_path = self.workspace_root / base_path
        else:
            output_path = self.output_dir / task_id / agent_role
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        for idx, block in enumerate(code_blocks):
            filename = block['filename']
            content = block['content']
            
            # Handle special cases for filenames
            if filename.startswith('/') or filename.startswith('./'):
                # Absolute or relative path specified
                file_path = self.workspace_root / filename.lstrip('./')
            else:
                file_path = output_path / filename
            
            # Create parent directories
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                created_files.append(str(file_path))
                logger.info(f"Created file: {file_path}")
            except Exception as e:
                logger.error(f"Failed to write file {file_path}: {e}")
        
        return created_files
    
    def write_file(
        self, 
        filename: str, 
        content: str, 
        task_id: str,
        agent_role: str,
        base_path: Optional[str] = None
    ) -> str:
        """Write a single file with specified content"""
        if base_path:
            output_path = self.workspace_root / base_path
        else:
            output_path = self.output_dir / task_id / agent_role
        
        output_path.mkdir(parents=True, exist_ok=True)
        file_path = output_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Created file: {file_path}")
            return str(file_path)
        except Exception as e:
            logger.error(f"Failed to write file {file_path}: {e}")
            raise
    
    def write_json(
        self, 
        filename: str, 
        data: Dict[str, Any], 
        task_id: str,
        agent_role: str,
        base_path: Optional[str] = None
    ) -> str:
        """Write JSON data to file"""
        if base_path:
            output_path = self.workspace_root / base_path
        else:
            output_path = self.output_dir / task_id / agent_role
        
        output_path.mkdir(parents=True, exist_ok=True)
        file_path = output_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            logger.info(f"Created JSON file: {file_path}")
            return str(file_path)
        except Exception as e:
            logger.error(f"Failed to write JSON file {file_path}: {e}")
            raise
    
    def extract_file_structure(self, text: str) -> Dict[str, str]:
        """
        Extract file structure from text that describes multiple files.
        Looks for patterns like:
        - File: `path/to/file.py`
        - File: path/to/file.py
        - path/to/file.py:
        - ## path/to/file.py
        """
        files = {}
        
        # Pattern 1: File: `filename` followed by ```language code block
        # This handles formats:
        # - File: `analysis/file.md` \n```markdown\n content \n```
        # - **File: `analysis/file.md`** \n```markdown\n content \n```
        # Use non-greedy match but ensure we capture until the closing ```
        
        # Try with bold first
        pattern1 = r'\*\*File:\s*`([^`]+)`\*\*\s*\n```(?:\w+)?\n(.*?)\n```'
        matches = re.finditer(pattern1, text, re.DOTALL)
        for match in matches:
            filename = match.group(1).strip()
            content = match.group(2).strip()
            files[filename] = content
        
        # If no matches with bold, try without bold
        if not files:
            pattern1_no_bold = r'File:\s*`([^`]+)`\s*\n```(?:\w+)?\n(.*?)\n```'
            matches = re.finditer(pattern1_no_bold, text, re.DOTALL)
            for match in matches:
                filename = match.group(1).strip()
                content = match.group(2).strip()
                files[filename] = content
        
        # If pattern 1 found files, return them
        if files:
            return files
        
        # Pattern 2: Traditional line-by-line parsing for other formats
        current_file = None
        current_content = []
        in_code_block = False
        
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            # Check for file markers
            file_marker = None
            
            # Pattern: File: `path/to/file.py` or File: path/to/file.py
            if line.strip().startswith('File:'):
                file_part = line.split('File:', 1)[1].strip()
                # Remove backticks if present
                file_marker = file_part.strip('`').strip()
                
                # Save previous file
                if current_file:
                    files[current_file] = '\n'.join(current_content).strip()
                
                current_file = file_marker
                current_content = []
                in_code_block = False
                
                # Skip the next line if it's a code block start
                if i + 1 < len(lines) and lines[i + 1].strip().startswith('```'):
                    in_code_block = True
                continue
            
            # Pattern: ## path/to/file.py
            elif line.strip().startswith('##') and ('/' in line or '.' in line):
                file_marker = line.strip('#').strip()
                
                if current_file:
                    files[current_file] = '\n'.join(current_content).strip()
                
                current_file = file_marker
                current_content = []
                in_code_block = False
                continue
            
            # Pattern: path/to/file.py:
            elif line.strip().endswith(':') and ('/' in line or line.count('.') >= 1):
                potential_marker = line.rstrip(':').strip()
                # Check if it looks like a file path
                if '.' in potential_marker or '/' in potential_marker:
                    file_marker = potential_marker
                    
                    if current_file:
                        files[current_file] = '\n'.join(current_content).strip()
                    
                    current_file = file_marker
                    current_content = []
                    in_code_block = False
                    continue
            
            # Handle code block markers
            if line.strip().startswith('```'):
                if in_code_block:
                    # End of code block
                    in_code_block = False
                else:
                    # Start of code block
                    in_code_block = True
                continue
            
            # Add content to current file
            if current_file:
                current_content.append(line)
        
        # Save last file
        if current_file:
            files[current_file] = '\n'.join(current_content).strip()
        
        return files
    
    def write_file_structure(
        self,
        text: str,
        task_id: str,
        agent_role: str,
        base_path: Optional[str] = None
    ) -> List[str]:
        """
        Parse file structure from text and write all files.
        Returns list of created file paths.
        """
        files = self.extract_file_structure(text)
        created_files = []
        
        if not files:
            # Fallback to code blocks if no file structure found
            return self.write_code_blocks(text, task_id, agent_role, base_path)
        
        for filepath, content in files.items():
            try:
                created_file = self.write_file(
                    filepath, 
                    content, 
                    task_id, 
                    agent_role, 
                    base_path
                )
                created_files.append(created_file)
            except Exception as e:
                logger.error(f"Failed to write file {filepath}: {e}")
        
        return created_files
    
    def save_task_result(
        self,
        task_id: str,
        agent_role: str,
        result: Dict[str, Any],
        output_subdir: str = "results"
    ) -> str:
        """Save task result as JSON file"""
        output_path = self.output_dir / output_subdir
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        filename = f"{task_id}_{agent_role}_{timestamp}.json"
        file_path = output_path / filename
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dumps(result, f, indent=2, default=str)
            
            logger.info(f"Saved task result: {file_path}")
            return str(file_path)
        except Exception as e:
            logger.error(f"Failed to save task result: {e}")
            raise

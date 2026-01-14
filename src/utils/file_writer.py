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
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename by removing markdown formatting characters.
        Removes backticks, asterisks, and other special characters that might
        be captured from malformed LLM output.
        """
        # Remove backticks and asterisks from beginning and end
        filename = filename.strip()
        # Remove leading/trailing backticks and asterisks
        filename = filename.strip('`*')
        # Remove any remaining backticks in the path (but keep directory separators)
        # Only strip them from individual path components
        parts = filename.split('/')
        cleaned_parts = [part.strip('`*') for part in parts]
        return '/'.join(cleaned_parts)
        
    def parse_code_blocks(self, text: str) -> List[Dict[str, str]]:
        """
        Parse code blocks from markdown-formatted text.
        Returns list of dicts with 'language', 'filename', and 'content'.
        
        Supports multiple formats:
        - File: `filename` followed by code block
        - **File: `filename`** followed by code block
        - ```python:filename.py
        - ```python
        """
        code_blocks = []
        
        if not text or not text.strip():
            logger.debug("parse_code_blocks: Empty or whitespace-only text provided")
            return code_blocks
        
        # First, try to extract File: `filename` format (same as extract_file_structure)
        # This prevents creating duplicate files
        files_dict = self.extract_file_structure(text)
        if files_dict:
            logger.debug(f"parse_code_blocks: Found {len(files_dict)} files using extract_file_structure")
            for filename, content in files_dict.items():
                # Infer language from filename extension
                ext = Path(filename).suffix.lower()
                language = self._get_language_from_extension(ext)
                
                code_blocks.append({
                    'language': language,
                    'filename': filename,
                    'content': content
                })
            return code_blocks
        
        # Fallback: Pattern to match fenced code blocks with optional filename
        # Supports: ```python, ```python:filename.py, ```filename.py
        # More flexible pattern that handles:
        # - Optional whitespace after ```
        # - Optional newline after language/filename
        # - Language identifiers with hyphens (e.g., dockerfile, yaml)
        # Use non-greedy matching to handle multiple code blocks
        pattern = r'```\s*(?:(\w+(?:-\w+)*)(?::\s*([^\n]+))?)?\s*\n?(.*?)\n?```'
        
        matches = list(re.finditer(pattern, text, re.DOTALL | re.MULTILINE))
        logger.debug(f"parse_code_blocks: Found {len(matches)} potential code blocks with regex pattern")
        
        # If we found code blocks but extract_file_structure didn't, it means they're not in "File:" format
        # Try to infer filenames from context (look for "File:" markers before code blocks)
        if matches and not code_blocks:
            logger.debug("parse_code_blocks: Code blocks found but not in File: format, trying to infer filenames from context")
            # Look for "File: filename" patterns that might be near code blocks
            file_markers = list(re.finditer(r'File:\s+([^\n]+)', text, re.IGNORECASE))
            for i, match in enumerate(matches):
                language = (match.group(1) or 'text').strip()
                filename_from_block = match.group(2).strip() if match.group(2) else None
                content = (match.group(3) or '').strip()
                
                if not content:
                    continue
                
                # If filename is in the code block header, use it
                if filename_from_block:
                    filename = filename_from_block
                else:
                    # Try to find a "File:" marker before this code block
                    block_start = match.start()
                    filename = None
                    for file_marker in file_markers:
                        if file_marker.end() < block_start and (block_start - file_marker.end()) < 200:
                            # Found a File: marker close before this code block
                            filename = file_marker.group(1).strip()
                            logger.debug(f"parse_code_blocks: Inferred filename '{filename}' from File: marker before code block")
                            break
                    
                    if not filename:
                        filename = self._infer_filename(content, language)
                
                code_blocks.append({
                    'language': language,
                    'filename': filename,
                    'content': content
                })
            
            if code_blocks:
                logger.debug(f"parse_code_blocks: Successfully parsed {len(code_blocks)} code blocks with inferred filenames")
                return code_blocks
        
        for match in matches:
            language = (match.group(1) or 'text').strip()
            filename = match.group(2).strip() if match.group(2) else None
            content = (match.group(3) or '').strip()
            
            # Skip empty code blocks
            if not content:
                logger.debug(f"parse_code_blocks: Skipping empty code block (language: {language}, filename: {filename})")
                continue
            
            # Try to infer filename from content if not specified
            if not filename:
                filename = self._infer_filename(content, language)
            
            code_blocks.append({
                'language': language,
                'filename': filename,
                'content': content
            })
        
        logger.debug(f"parse_code_blocks: Returning {len(code_blocks)} code blocks")
        return code_blocks
    
    def _get_language_from_extension(self, ext: str) -> str:
        """Get language name from file extension"""
        ext_to_lang = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'tsx',
            '.jsx': 'jsx',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sql': 'sql',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.json': 'json',
            '.xml': 'xml',
            '.md': 'markdown',
            '.sh': 'bash',
        }
        return ext_to_lang.get(ext, 'text')
    
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
            # Log a snippet of the response for debugging
            text_preview = text[:500] if len(text) > 500 else text
            logger.warning(
                f"No code blocks found in response for task {task_id} (agent: {agent_role})\n"
                f"Response preview (first 500 chars):\n{text_preview}\n"
                f"Response length: {len(text)} characters"
            )
            # Also check if there are any code block markers at all
            if '```' in text:
                logger.debug(f"Found backticks in response but parsing failed. Full response:\n{text}")
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
        logger.debug(f"extract_file_structure: Processing text of length {len(text)}")
        
        # Pattern 1: ```language:filename format
        # This handles: ```markdown:analysis/file.md
        # Need to handle nested code blocks, so we manually parse
        # More flexible: allow optional whitespace and language with hyphens
        pattern_colon = r'```\s*(?:\w+(?:-\w+)*):\s*([^\n]+)\s*\n?'
        matches = list(re.finditer(pattern_colon, text, re.DOTALL))
        
        if matches:
            for i, match in enumerate(matches):
                filename = self._sanitize_filename(match.group(1))
                start_pos = match.end()
                
                # Find the matching closing ``` by counting backticks
                # Look for the next file marker or end of text
                if i + 1 < len(matches):
                    end_search = matches[i + 1].start()
                else:
                    end_search = len(text)
                
                # Find the closing ``` before the next file marker
                remaining_text = text[start_pos:end_search]
                # Look for closing ``` - need to handle nested code blocks
                # Count opening ``` markers and find the matching closing one
                close_match = None
                backtick_depth = 1  # We already passed one opening ```
                
                # Find all ``` markers (both opening and closing)
                all_backtick_matches = list(re.finditer(r'(?:^|\n)\s*```', remaining_text, re.MULTILINE))
                
                for m in all_backtick_matches:
                    # Check what comes after the ``` to determine if it's opening or closing
                    match_end = m.end()
                    # Look at the rest of the line after ```
                    line_end = remaining_text.find('\n', match_end)
                    if line_end == -1:
                        line_end = len(remaining_text)
                    rest_of_line = remaining_text[match_end:line_end].strip()
                    
                    if rest_of_line and not rest_of_line.isspace():
                        # Has content after ``` (like ```python or ```markdown) - it's an opening
                        backtick_depth += 1
                    else:
                        # No content or just whitespace after ``` - it's a closing
                        backtick_depth -= 1
                        if backtick_depth == 0:
                            # Found the matching closing ```
                            close_match = m
                            break
                # Pattern 2: ``` at start of remaining_text or after newline
                if not close_match:
                    for m in re.finditer(r'^```\s*(?:\n|$)', remaining_text, re.MULTILINE):
                        close_match = m
                        break
                    # Pattern 3: Any ``` followed by whitespace or end (most permissive)
                    if not close_match:
                        for m in re.finditer(r'```\s*(?:\n|$)', remaining_text):
                            close_match = m
                            break
                
                if close_match:
                    content = remaining_text[:close_match.start()].strip()
                    files[filename] = content
        
        # If found files with colon format, only return if we successfully extracted all matches
        # Otherwise, fall through to Pattern 2 which handles "File: `filename`" format
        if files and len(files) == len(matches):
            return files
        # Don't return - let Pattern 2 try to extract the remaining files
        
        # Pattern 2: File: `filename` followed by ```language code block
        # This handles formats:
        # - File: `analysis/file.md` \n```markdown\n content \n```
        # - **File: `analysis/file.md`** \n```markdown\n content \n```
        
        # Try with bold first - use similar approach to handle nested blocks
        # More flexible: allow optional whitespace and newlines
        pattern_bold = r'\*\*File:\s*`([^`]+)`\*\*\s*\n?\s*```\s*(?:\w+(?:-\w+)*)?\s*\n?'
        matches = list(re.finditer(pattern_bold, text, re.DOTALL))
        
        if matches:
            for i, match in enumerate(matches):
                filename = self._sanitize_filename(match.group(1))
                start_pos = match.end()
                
                if i + 1 < len(matches):
                    end_search = matches[i + 1].start()
                else:
                    end_search = len(text)
                
                remaining_text = text[start_pos:end_search]
                # Use depth tracking for nested code blocks
                close_match = None
                backtick_depth = 1
                all_backtick_matches = list(re.finditer(r'(?:^|\n)\s*```', remaining_text, re.MULTILINE))
                
                for m in all_backtick_matches:
                    match_end = m.end()
                    line_end = remaining_text.find('\n', match_end)
                    if line_end == -1:
                        line_end = len(remaining_text)
                    rest_of_line = remaining_text[match_end:line_end].strip()
                    
                    if rest_of_line and not rest_of_line.isspace():
                        backtick_depth += 1
                    else:
                        backtick_depth -= 1
                        if backtick_depth == 0:
                            close_match = m
                            break
                
                if close_match:
                    content = remaining_text[:close_match.start()].strip()
                    files[filename] = content
        
        # If no matches with bold, try without bold (with backticks)
        # Always try this pattern even if files dict has entries from Pattern 1
        # (matches variable is from Pattern 2 bold section above)
        if not matches or len(matches) == 0:
            # More flexible: allow optional whitespace and newlines
            pattern_no_bold = r'File:\s*`([^`]+)`\s*\n?\s*```\s*(?:\w+(?:-\w+)*)?\s*\n?'
            matches = list(re.finditer(pattern_no_bold, text, re.DOTALL))
            
            if matches:
                for i, match in enumerate(matches):
                    filename = self._sanitize_filename(match.group(1))
                    start_pos = match.end()
                    
                    if i + 1 < len(matches):
                        end_search = matches[i + 1].start()
                    else:
                        end_search = len(text)
                    
                    remaining_text = text[start_pos:end_search]
                    # Use depth tracking for nested code blocks
                    close_match = None
                    backtick_depth = 1
                    all_backtick_matches = list(re.finditer(r'(?:^|\n)\s*```', remaining_text, re.MULTILINE))
                    
                    for m in all_backtick_matches:
                        match_end = m.end()
                        line_end = remaining_text.find('\n', match_end)
                        if line_end == -1:
                            line_end = len(remaining_text)
                        rest_of_line = remaining_text[match_end:line_end].strip()
                        
                        if rest_of_line and not rest_of_line.isspace():
                            backtick_depth += 1
                        else:
                            backtick_depth -= 1
                            if backtick_depth == 0:
                                close_match = m
                                break
                    
                    if close_match:
                        content = remaining_text[:close_match.start()].strip()
                        files[filename] = content
        
        # Pattern 3: File: path/to/file.py (without backticks)
        # Always try this pattern even if files dict has entries from previous patterns
        # More flexible: allow optional whitespace and newlines
        # This pattern matches: "File: filename\n```language\n" or "File: filename\n```\n"
        # The pattern requires at least one newline between "File:" and the code block
        pattern_no_backticks = r'File:\s+([^\n]+?)\s*\n+\s*```\s*(?:\w+(?:-\w+)*)?\s*\n?'
        matches = list(re.finditer(pattern_no_backticks, text, re.DOTALL))
        
        if matches:
                logger.debug(f"extract_file_structure: Found {len(matches)} matches with Pattern 3 (File: without backticks)")
                for i, match in enumerate(matches):
                    filename = self._sanitize_filename(match.group(1))
                    start_pos = match.end()
                    
                    if i + 1 < len(matches):
                        end_search = matches[i + 1].start()
                    else:
                        end_search = len(text)
                    
                    remaining_text = text[start_pos:end_search]
                    logger.debug(f"extract_file_structure: Pattern 3 - Processing file '{filename}', remaining text length: {len(remaining_text)}, preview: {remaining_text[:100]}")
                    
                    # Use depth tracking for nested code blocks
                    close_match = None
                    backtick_depth = 1
                    all_backtick_matches = list(re.finditer(r'(?:^|\n)\s*```', remaining_text, re.MULTILINE))
                    
                    for m in all_backtick_matches:
                        match_end = m.end()
                        line_end = remaining_text.find('\n', match_end)
                        if line_end == -1:
                            line_end = len(remaining_text)
                        rest_of_line = remaining_text[match_end:line_end].strip()
                        
                        if rest_of_line and not rest_of_line.isspace():
                            backtick_depth += 1
                        else:
                            backtick_depth -= 1
                            if backtick_depth == 0:
                                close_match = m
                                break
                    
                    if close_match:
                        content = remaining_text[:close_match.start()].strip()
                        if content:
                            files[filename] = content
                            logger.debug(f"extract_file_structure: Successfully extracted file '{filename}' with {len(content)} chars")
                        else:
                            logger.warning(f"extract_file_structure: Found closing ``` but content is empty for '{filename}'")
                    else:
                        logger.warning(f"extract_file_structure: Could not find closing ``` for '{filename}'. Remaining text preview: {remaining_text[:200]}")
                        # As a fallback, if we can't find closing ```, try to extract up to the next "File:" marker
                        # or use all remaining text if it's the last file
                        if i + 1 >= len(matches):
                            # Last file, use all remaining text
                            content = remaining_text.strip()
                            if content:
                                files[filename] = content
                                logger.debug(f"extract_file_structure: Using all remaining text for last file '{filename}' ({len(content)} chars)")
        
        # Return files if any patterns matched, otherwise return empty dict
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

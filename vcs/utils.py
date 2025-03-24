import fnmatch
import os
import re

def parse_gitignore(gitignore_content):
    """Parse gitignore content and return a list of patterns to ignore."""
    ignore_patterns = []
    
    # Add common patterns to always ignore (even if no .gitignore exists)
    common_ignores = [
        'node_modules/', '*/node_modules/*', 'node_modules',
        '.git/', '.git/**', '.git', '**/.git/**'
    ]
    ignore_patterns.extend(common_ignores)
    
    # If no gitignore content was provided, return the common patterns
    if not gitignore_content:
        return ignore_patterns
    
    for line in gitignore_content.decode('utf-8', errors='ignore').splitlines():
        # Skip comments and empty lines
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Handle negation with ! prefix (we'll just remove these patterns for simplicity)
        if line.startswith('!'):
            pattern_to_remove = line[1:].strip()  # Fix typo: 'trip' -> 'strip'
            if pattern_to_remove in ignore_patterns:
                ignore_patterns.remove(pattern_to_remove)
            continue
            
        # Add the pattern
        ignore_patterns.append(line)
    
    return ignore_patterns

def should_ignore_file(file_path, ignore_patterns):
    """Check if a file should be ignored based on gitignore patterns."""
    # Normalize path separator to forward slash
    file_path = file_path.replace('\\', '/')
    
    # Special case for node_modules and .git - always ignore
    path_parts = file_path.split('/')
    if 'node_modules' in path_parts or '.git' in path_parts:
        return True
    
    # Check if this is a git file (like .gitattributes, .gitmodules, etc.)
    if any(part.startswith('.git') for part in path_parts):
        return True
    
    for pattern in ignore_patterns:
        # Handle directory pattern (ending with /)
        is_dir_pattern = pattern.endswith('/')
        if is_dir_pattern:
            pattern = pattern[:-1]
            
        # Handle patterns with / to match specific paths
        if '/' in pattern:
            if fnmatch.fnmatch(file_path, pattern):
                return True
        else:
            # Match pattern against filename and all parent directories
            parts = file_path.split('/')
            for part in parts:
                if fnmatch.fnmatch(part, pattern):
                    return True
                    
        # Special case for directory patterns
        if is_dir_pattern and any(part == pattern for part in file_path.split('/')):
            return True
    
    return False
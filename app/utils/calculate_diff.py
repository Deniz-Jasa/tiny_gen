import difflib

def calculate_code_diff(original_code: str, suggested_changes: str) -> str:
    """
    Calculates the unified diff between the original code and the suggested changes.
    Only shows actual modifications.
    """
    try:
        # Parse files from both original and suggested code
        original_files = parse_files(original_code)
        suggested_files = parse_files(suggested_changes)
        
        all_diffs = []
        
        # Only process files that exist in both versions
        for file_path in suggested_files.keys():  # Only look at files the AI modified
            if file_path in original_files:
                original = original_files[file_path]
                suggested = suggested_files[file_path]
                
                # Only generate diff if there are actual changes
                if original != suggested:
                    diff = list(difflib.unified_diff(
                        original.splitlines(),
                        suggested.splitlines(),
                        fromfile=f'a/{file_path}',
                        tofile=f'b/{file_path}',
                        lineterm=''
                    ))
                    
                    if diff:  # If there are any changes
                        all_diffs.extend(diff)
        
        return '\n'.join(all_diffs)
    
    except Exception as e:
        print(f"Error calculating diff: {e}")
        raise

def parse_files(code_string: str) -> dict:
    """
    Parses a string containing multiple files into a dictionary of file paths and contents.
    Ignores any content that doesn't follow the 'File filename:' format.
    """
    files = {}
    current_file = None
    current_content = []
    
    lines = code_string.split('\n')
    for line in lines:
        if line.startswith('File ') and ':' in line:
            # Save previous file if exists
            if current_file:
                files[current_file] = '\n'.join(current_content).strip()
                current_content = []
            
            # Start new file
            current_file = line[5:line.index(':')].strip()
        elif current_file and line.startswith('File '):
            # If we hit another "File" line without proper format, ignore it
            continue
        elif current_file:
            current_content.append(line)
    
    # Save last file
    if current_file and current_content:
        files[current_file] = '\n'.join(current_content).strip()
    
    return files
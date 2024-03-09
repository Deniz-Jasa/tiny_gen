import difflib

def calculate_code_diff(original_code, suggested_changes):
    diff = difflib.unified_diff(original_code.splitlines(), suggested_changes.splitlines())
    
    # Join the diff lines into a single string
    diff_str = '\n'.join(diff)

    # Add the diff header
    print(diff_str)
    
    return diff_str
import difflib

def calculate_code_diff(original_code, suggested_changes, filename="src/main.py"):
    diff = difflib.unified_diff(original_code.splitlines(), suggested_changes.splitlines(), fromfile=filename, tofile=filename)
    
    # Join the diff lines into a single string
    diff_str = '\n'.join(diff)

    # Add the diff header
    header = f"diff --git a/{filename} b/{filename}\nindex 58d38b6..23b0827 100644\n"
    print(f"{header}\n{diff_str}")
    
    return f"{header}\n{diff_str}"
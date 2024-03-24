import difflib

def calculate_code_diff(original_code: str, suggested_changes: str) -> str:
    """
    Calculates the unified diff between the original code and the suggested changes.

    Parameters:
    - original_code (str): The original code block.
    - suggested_changes (str): The modified code block with suggested changes.

    Returns:
    - str: A string representing the unified diff of the changes.
    """
    diff = difflib.unified_diff(original_code.splitlines(), suggested_changes.splitlines())
    
    # Join the diff lines into a single string
    return '\n'.join(diff)
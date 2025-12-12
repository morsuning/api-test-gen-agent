import re
import json_repair

def robust_json_parse(json_str: str):
    """
    Parses a JSON string properly, even if it contains:
    1. Python-style string multiplication: "A" * 1000
    2. JS/TS-style string repetition: "A".repeat(1000)
    3. Missing commas or minor syntax errors (handled by json_repair)
    """
    
    # Pre-process: Handle String Multiplication/Repetition
    # Case 1: "char" * N (Python-style)
    # Regex explanation:
    # ((?:\"[^\"]*\"|'[^']*'))  -> Group 1: Match a string in double quotes OR single quotes.
    #                              [^\"]* means any char except double quote.
    # \s*\*\s*(\d+)             -> Match * followed by a number (Group 2)
    def replace_mul(match):
        full_str = match.group(1)
        # Remove surrounding quotes
        if full_str.startswith('"'):
            content = full_str[1:-1]
        else:
            content = full_str[1:-1]
            
        count = int(match.group(2))
        # Return new string with double quotes (standard JSON)
        return f'"{content * count}"'

    json_str = re.sub(r'((?:\"[^\"]*\"|\'[^\']*\'))\s*\*\s*(\d+)', replace_mul, json_str)

    # Case 2: "char".repeat(N) (JS-style)
    def replace_repeat(match):
        full_str = match.group(1)
        if full_str.startswith('"'):
            content = full_str[1:-1]
        else:
            content = full_str[1:-1]
            
        count = int(match.group(2))
        return f'"{content * count}"'
    
    json_str = re.sub(r'((?:\"[^\"]*\"|\'[^\']*\'))\.repeat\((\d+)\)', replace_repeat, json_str)

    # Use json_repair to handle structural issues (missing commas, unclosed brackets, etc.)
    try:
        data = json_repair.loads(json_str)
        return data
    except Exception as e:
        # Fallback diagnostics
        raise ValueError(f"Failed to parse JSON even with repair: {e}")

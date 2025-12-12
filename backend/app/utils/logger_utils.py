import json
from typing import Any, Dict, List, Union

def recursive_decode_json(data: Any) -> Any:
    """
    Recursively traverse complex data structures.
    If a string value encounters a valid JSON string, decode it and recurse.
    """
    if isinstance(data, dict):
        return {k: recursive_decode_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [recursive_decode_json(v) for v in data]
    elif isinstance(data, str):
        try:
            # Attempt to parse string as JSON
            parsed = json.loads(data)
            # If successful, recurse on the parsed data (it might contain more nested JSON strings)
            # handle case where json.loads returns primitive types that shouldn't be expanded if they look like simple strings
            if isinstance(parsed, (dict, list)):
                 return recursive_decode_json(parsed)
            return parsed
        except (json.JSONDecodeError, TypeError):
            return data
    else:
        return data

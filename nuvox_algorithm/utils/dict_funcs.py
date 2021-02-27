from typing import Dict, Any, Union


def ranked_keys(a_dict: Dict[Any, Union[float, int]]) -> list:
    """Returns list of keys ranked by value (highest first)."""
    return [k for k, v in sorted(a_dict.items(), key=lambda item: item[1], reverse=True)]


def reverse_dict(a_dict: dict) -> dict:
    return {v: k for k, v in a_dict.items()}

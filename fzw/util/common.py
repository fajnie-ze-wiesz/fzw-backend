from typing import Any, Optional

_TRUTHY_VALUES = {"t", "true", "1"}
_FALSY_VALUES = {"f", "false", "0"}


def smart_bool_or_none(value: Any) -> Optional[bool]:
    if isinstance(value, str):
        normalized_value = value.lower()
        if normalized_value in _TRUTHY_VALUES:
            return True
        if normalized_value in _FALSY_VALUES:
            return False
        return None
    if value is None:
        return None
    return bool(value)


def smart_bool(value: Any) -> bool:
    return smart_bool_or_none(value) or False

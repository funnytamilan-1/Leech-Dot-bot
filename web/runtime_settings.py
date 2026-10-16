"""Atomic runtime overrides shared by the bot and web server processes."""
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

_ALLOWED = {
    "USE_HYPER": bool,
    "HYPER_THREADS": int,
    "HYPER_PIPELINE": int,
    "HYPER_CHUNK": int,
}
_LIMITS = {
    "HYPER_THREADS": (0, 64),
    "HYPER_PIPELINE": (4, 256),
    "HYPER_CHUNK": (65536, 16777216),
}


def _settings_path():
    return Path(os.getenv("LEECH_DOT_RUNTIME_SETTINGS", "runtime_settings.json"))


def _validate_value(key, value):
    kind = _ALLOWED[key]
    if kind is bool:
        if not isinstance(value, bool):
            raise ValueError(f"{key} must be boolean")
        return value
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{key} must be an integer")
    low, high = _LIMITS[key]
    return max(low, min(value, high))


def read_runtime_overrides():
    try:
        with _settings_path().open("r", encoding="utf-8") as stream:
            data = json.load(stream)
        if not isinstance(data, dict):
            return {}
        result = {}
        for key, value in data.items():
            if key in _ALLOWED:
                try:
                    result[key] = _validate_value(key, value)
                except ValueError:
                    continue
        return result
    except (OSError, ValueError, TypeError):
        return {}


def write_runtime_overrides(values):
    if not isinstance(values, dict) or any(key not in _ALLOWED for key in values):
        raise ValueError("Unsupported runtime setting")
    current = read_runtime_overrides()
    for key, value in values.items():
        current[key] = _validate_value(key, value)
    path = _settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with NamedTemporaryFile("w", encoding="utf-8", dir=str(path.parent), delete=False) as stream:
            json.dump(current, stream, separators=(",", ":"))
            temp_name = stream.name
        os.replace(temp_name, path)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)
    return current

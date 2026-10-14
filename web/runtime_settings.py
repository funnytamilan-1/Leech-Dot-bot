"""Atomic runtime overrides shared by the bot and web server processes."""
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

_ALLOWED = {"START_SHORTENER_REQUIRED": bool, "START_SHORTENER_LINK_TTL": int, "START_SHORTENER_SESSION_TTL": int}


def _settings_path():
    return Path(os.getenv("LEECH_DOT_RUNTIME_SETTINGS", "runtime_settings.json"))


def read_runtime_overrides():
    try:
        with _settings_path().open("r", encoding="utf-8") as stream:
            data = json.load(stream)
        if not isinstance(data, dict):
            return {}
        result = {}
        for key, kind in _ALLOWED.items():
            value = data.get(key)
            if kind is bool and isinstance(value, bool):
                result[key] = value
            elif kind is int and isinstance(value, int) and not isinstance(value, bool):
                result[key] = max(60, min(value, 86400))
        return result
    except (OSError, ValueError, TypeError):
        return {}


def write_runtime_overrides(values):
    if not isinstance(values, dict) or any(key not in _ALLOWED for key in values):
        raise ValueError("Unsupported runtime setting")
    current = read_runtime_overrides()
    for key, value in values.items():
        kind = _ALLOWED[key]
        if kind is bool:
            if not isinstance(value, bool):
                raise ValueError(f"{key} must be boolean")
        elif isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{key} must be an integer")
        else:
            value = max(60, min(value, 86400))
        current[key] = value
    path = _settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", dir=str(path.parent), delete=False) as stream:
        json.dump(current, stream, separators=(",", ":"))
        temp_name = stream.name
    os.replace(temp_name, path)
    return current

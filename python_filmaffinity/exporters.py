"""Export helpers for FilmAffinity results."""

import csv
import io
import json


def _as_plain(value):
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "dict") and callable(value.dict):
        return value.dict()
    if isinstance(value, list):
        return [_as_plain(item) for item in value]
    if isinstance(value, tuple):
        return [_as_plain(item) for item in value]
    if isinstance(value, dict):
        return {key: _as_plain(item) for key, item in value.items()}
    return value


def _rows(data):
    plain = _as_plain(data)
    if plain is None:
        return []
    if isinstance(plain, list):
        return plain
    return [plain]


def _stringify_cell(value):
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    if value is None:
        return ""
    return str(value)


def _write_or_return(content, path):
    if path is None:
        return content
    with open(path, "w", encoding="utf-8", newline="") as file_handle:
        file_handle.write(content)
    return content


def to_json(data, path=None):
    """Export a movie or movie list as formatted JSON."""
    content = json.dumps(_as_plain(data), ensure_ascii=False, indent=2)
    return _write_or_return(content, path)


def to_csv(data, path):
    """Export a movie or movie list to CSV."""
    rows = _rows(data)
    fieldnames = sorted({key for row in rows if isinstance(row, dict) for key in row})
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow({key: _stringify_cell(row.get(key)) for key in fieldnames})
    return _write_or_return(buffer.getvalue(), path)


def to_markdown(data, path=None):
    """Export a movie or movie list as a Markdown table."""
    rows = _rows(data)
    fieldnames = sorted({key for row in rows if isinstance(row, dict) for key in row})
    if not fieldnames:
        return _write_or_return("", path)
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join(["---"] * len(fieldnames)) + " |",
    ]
    for row in rows:
        lines.append(
            "| " + " | ".join(_stringify_cell(row.get(key)) for key in fieldnames) + " |"
        )
    return _write_or_return("\n".join(lines) + "\n", path)

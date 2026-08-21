from __future__ import annotations

import csv
import json
import sys
from collections.abc import Iterable
from typing import Any


def emit(payload: Any, output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(_to_data(payload), ensure_ascii=False, indent=2))
        return
    if output_format == "jsonl":
        items = payload if isinstance(payload, list) else [payload]
        for item in items:
            print(json.dumps(_to_data(item), ensure_ascii=False))
        return
    if output_format == "csv":
        _emit_csv(payload)
        return
    if output_format == "markdown":
        _emit_markdown(payload)
        return
    raise ValueError(f"unsupported format: {output_format}")


def _to_data(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()
    if isinstance(value, list):
        return [_to_data(item) for item in value]
    return value


def _rows_from_payload(payload: Any) -> list[dict[str, Any]]:
    data = _to_data(payload)
    if isinstance(data, dict) and isinstance(data.get("data"), dict):
        if isinstance(data["data"].get("items"), list):
            return [item for item in data["data"]["items"] if isinstance(item, dict)]
        return [data["data"]]
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def _emit_csv(payload: Any) -> None:
    rows = _rows_from_payload(payload)
    if not rows:
        return
    fieldnames = sorted({key for row in rows for key in row.keys()})
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


def _emit_markdown(payload: Any) -> None:
    data = _to_data(payload)
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"- `{key}`: {value}")
        return
    if isinstance(data, Iterable):
        for item in data:
            print(f"- {item}")


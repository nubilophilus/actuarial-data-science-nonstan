import json
from pathlib import Path
from typing import Any, Dict


def ensure_directories(paths: list[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def write_json(payload: Dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    if denominator in (0, None):
        return default
    return numerator / denominator


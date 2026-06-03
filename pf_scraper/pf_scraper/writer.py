# pf_scraper/writer.py
from __future__ import annotations

import json
import os
from typing import Iterable, Dict, Any, Optional


def write_jsonl(path: str, rows: Iterable[Dict[str, Any]], mode: str = "a") -> int:
    """
    Write rows to a JSONL file.

    mode:
      - "a" append (default): safe for resume/checkpoints
      - "w" overwrite: start fresh
    """
    if mode not in ("a", "w"):
        raise ValueError("mode must be 'a' or 'w'")

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    n = 0
    with open(path, mode, encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    return n

# pf_scraper/writer.py
import json
import os
from typing import Dict, Iterable, Set, Optional


def _ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)


def _load_existing_ids(path: str) -> Set[str]:
    """
    If file already exists, load IDs so subsequent runs are append-safe and still dedup.
    This is streaming-friendly: it reads line by line.
    """
    seen: Set[str] = set()
    if not os.path.exists(path):
        return seen

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                pid = obj.get("id")
                if pid is not None:
                    seen.add(str(pid))
            except Exception:
                # ignore malformed lines
                continue
    return seen


def write_jsonl(path: str, rows: Iterable[Dict], dedup_by_id: bool = True) -> int:
    """
    Streaming writer:
    - Accepts generator/iterable (no len() needed)
    - Creates parent dir
    - Dedups by 'id' across:
        (a) rows in this run
        (b) rows already written in the file (append-safe)
    Returns number of rows newly written.
    """
    _ensure_parent_dir(path)

    seen: Set[str] = set()
    if dedup_by_id:
        seen = _load_existing_ids(path)

    written = 0
    with open(path, "a", encoding="utf-8") as f:
        for row in rows:
            if not isinstance(row, dict):
                continue

            if dedup_by_id:
                pid = row.get("id")
                if pid is None:
                    continue
                pid = str(pid)
                if pid in seen:
                    continue
                seen.add(pid)

            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            written += 1

    return written

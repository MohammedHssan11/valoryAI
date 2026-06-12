# pf_scraper/checkpoint.py
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class Checkpoint:
    category: str
    next_page: int = 1
    country: Optional[str] = None  # ✅ NEW

    @staticmethod
    def load(path: str) -> Optional["Checkpoint"]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                d = json.load(f)

            return Checkpoint(
                category=d.get("category"),
                next_page=int(d.get("next_page", 1)),
                country=d.get("country"),  # may be None (old checkpoints)
            )
        except FileNotFoundError:
            return None
        except Exception:
            return None

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "category": self.category,
                    "next_page": self.next_page,
                    "country": self.country,  # ✅ stored
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

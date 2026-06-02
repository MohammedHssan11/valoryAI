import os
import json
import logging
from typing import Set, Tuple

logger = logging.getLogger(__name__)

class ExposureRegistry:
    def __init__(self):
        self.compounds: Set[str] = set()
        self.h3_hexes: Set[str] = set()
        self._load()

    def _load(self):
        file_path = os.path.join(os.path.dirname(__file__), "exposure_registry.json")
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                self.compounds = set(data.get("compounds", []))
                self.h3_hexes = set(data.get("h3_res9", []))
            logger.info(f"ExposureRegistry loaded {len(self.compounds)} compounds and {len(self.h3_hexes)} H3 hexes.")
        except Exception as e:
            logger.error(f"Failed to load exposure registry: {e}")

    def is_unseen_compound(self, compound_name: str | None) -> bool:
        if not compound_name or compound_name.upper() == 'UNKNOWN':
            return False
        return compound_name not in self.compounds

    def is_unseen_h3(self, h3_index: str | None) -> bool:
        if not h3_index or h3_index.upper() == 'UNKNOWN':
            return False
        return h3_index not in self.h3_hexes

    def get_exposure_metrics(self, compound_name: str | None, h3_index: str | None) -> Tuple[bool, bool, float]:
        unseen_comp = self.is_unseen_compound(compound_name)
        unseen_h3 = self.is_unseen_h3(h3_index)
        
        # Exposure score: 1.0 (fully seen), 0.5 (partially seen), 0.0 (completely unseen)
        score = 0.0
        if not unseen_comp: score += 0.5
        if not unseen_h3: score += 0.5
        
        return unseen_comp, unseen_h3, score

exposure_registry = ExposureRegistry()

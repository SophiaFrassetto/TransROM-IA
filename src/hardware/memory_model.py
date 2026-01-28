from dataclasses import dataclass
from typing import Optional


@dataclass
class MemoryModel:
    address_space_ids: list[str]  # refs para AddressSpace
    mirrored: bool
    banked: bool
    notes: Optional[str] = None
    confidence: Optional[float] = None  # 0.0–1.0
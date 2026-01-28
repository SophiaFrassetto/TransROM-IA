from dataclasses import dataclass
from typing import Optional


@dataclass
class PointerModel:
    common_widths: list[int]  # [16, 24, 32]
    relative_supported: bool
    banked: bool
    default_schema_id: Optional[str] = None
    notes:Optional[str] = None
    confidence: Optional[float] = None  # 0.0–1.0
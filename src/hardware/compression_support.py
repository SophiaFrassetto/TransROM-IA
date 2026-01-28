from dataclasses import dataclass
from typing import List, Optional

from constants import CompressionType


@dataclass
class CompressionSupport:
    supported: bool
    common_types: List[CompressionType]  # CompressionType.value
    hardware_assisted: bool
    notes: Optional[str] = None
    confidence: Optional[float] = None  # 0.0–1.0

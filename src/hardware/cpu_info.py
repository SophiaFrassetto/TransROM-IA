from dataclasses import dataclass
from typing import List, Optional

from constants import ByteOrder


@dataclass
class CPUInfo:
    id: str  # "arm7tdmi", "65c816", "m68000"
    name: str
    bitness: int  # 8 / 16 / 32
    byte_order: ByteOrder
    supports_thumb: Optional[bool] = None
    supports_modes: Optional[List[str]] = None  # ex: ["native", "emulation"]
    notes: Optional[str] = None
    confidence: Optional[float] = None  # 0.0–1.0
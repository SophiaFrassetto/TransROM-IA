from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CartridgeHardware:
    """
    Describes optional hardware embedded in cartridges.
    """
    extra_cpu: bool
    coprocessors: List[str]
    rtc: bool
    sensors: List[str]
    rumble: bool
    notes: Optional[str] = None
    confidence: Optional[float] = None  # 0.0–1.0

from dataclasses import dataclass
from typing import List, Optional
from core.bytes_region import BytesRegion
from hardware.cartridge_hardware import CartridgeHardware


@dataclass
class Rom:
    id: str
    name: str
    path: str
    extension: str
    size: int
    raw_bytes: bytes
    family_id: Optional[str] = None
    layouts: Optional[List[str]] = None
    regions: Optional[List[BytesRegion]] = None
    cartridge_hardware_override: Optional[CartridgeHardware] = None
    notes: Optional[str] = None

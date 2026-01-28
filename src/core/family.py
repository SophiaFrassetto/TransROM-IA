from dataclasses import dataclass
from typing import List, Optional

from core.bytes_region import BytesLayout
from hardware.cartridge_hardware import CartridgeHardware
from hardware.family_hardware import FamilyHardware


@dataclass
class Family:
    id: str
    name: str
    extensions: List[str]
    hardware: FamilyHardware
    default_cartridge_hardware: CartridgeHardware
    layouts: Optional[List[BytesLayout]] = None
    notes: Optional[str] = None

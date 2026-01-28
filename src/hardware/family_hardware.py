from dataclasses import dataclass
from typing import Optional

from hardware.banking_model import BankingModel
from hardware.compression_support import CompressionSupport
from hardware.cpu_info import CPUInfo
from hardware.memory_model import MemoryModel
from hardware.pointer_model import PointerModel



@dataclass
class FamilyHardware:
    """
    Describes the built-in hardware characteristics of a console family.
    """

    cpu: CPUInfo
    pointer_model: PointerModel
    memory_model: MemoryModel
    banking_model: BankingModel
    compression_support: CompressionSupport
    notes: Optional[str] = None
    confidence: Optional[float] = None  # 0.0–1.0

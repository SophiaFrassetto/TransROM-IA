from dataclasses import dataclass
from typing import List, Optional


@dataclass
class BankingModel:
    supported: bool
    types: List[str]  # "LoROM", "HiROM", "Linear"
    bank_size: Optional[int] = None
    notes: Optional[str] = None
    confidence: Optional[float] = None  # 0.0–1.0
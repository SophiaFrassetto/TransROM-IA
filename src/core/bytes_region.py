from dataclasses import dataclass

from typing import List, Optional
from constants import ByteOrder, Encoding, Kind, Origin, Tag


@dataclass
class MappedDefaultValue:
    id: str
    raw: bytes
    meaning: str
    origin: Optional[Origin] = None
    confidence: Optional[float] = None  # 0.0–1.0


@dataclass
class BytesRegion:
    """
    Represents a semantically meaningful region of bytes
    inside a ROM file or address space.
    """

    id: str
    name: str
    kind: Kind
    origin: Origin
    offset: int
    size: int
    required: bool = False
    encoding: Optional[Encoding] = None
    byte_order: Optional[ByteOrder] = None
    address_space: Optional[str] = None  # e.g. "ROM", "WRAM"
    bank: Optional[int] = None  # logical bank number
    tags: Optional[List[Tag]] = None
    default_value_mapped: Optional[List[MappedDefaultValue]] = None
    confidence: Optional[float] = None  # 0.0–1.0
    notes: Optional[str] = None
    
    def copy_with_offset_delta(self, delta: int) -> "BytesRegion":
        return BytesRegion(
            id=self.id,
            name=self.name,
            address_space=self.address_space,
            kind=self.kind,
            origin=self.origin,
            offset=self.offset + delta,
            size=self.size,
            required=self.required,
            tags=self.tags,
            encoding=self.encoding,
            confidence=self.confidence,
            notes=self.notes,
            default_value_mapped=self.default_value_mapped,
        )


@dataclass
class BytesLayout:
    id: str  # "snes.header.lorom"
    name: str  # "SNES Header (LoROM)"
    origin: Origin  # spec | observed
    canonical_offset: int
    address_space: str
    regions: List[BytesRegion]
    tags: Optional[List[Tag]] = None
    notes: Optional[str] = None
    confidence: Optional[float] | None = None  # 0.0–1.0

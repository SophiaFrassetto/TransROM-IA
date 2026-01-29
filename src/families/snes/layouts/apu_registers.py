"""
SNES APU I/O Register Map
"""

from constants import Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion

__all__ = ["SNES_APU_REGISTERS"]


SNES_APU_REGISTERS = BytesLayout(
    id="snes.system.apu_registers",
    name="SNES APU Registers",
    origin=Origin.spec,
    confidence=1.0,
    canonical_offset=0x2140,
    address_space="snes.cpu",
    tags=[Tag.execution, Tag.structural],
    notes="Audio Processing Unit I/O registers.",

    regions=[
        BytesRegion(
            id="snes.apu.io",
            name="APU I/O Registers",
            address_space="snes.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0x2140,
            size=0x04,
            required=True,
            tags=[Tag.execution],
        ),
    ],
)

"""
SNES PPU Register Map
"""

from constants import Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion

__all__ = ["SNES_PPU_REGISTERS"]


SNES_PPU_REGISTERS = BytesLayout(
    id="snes.system.ppu_registers",
    name="SNES PPU Registers",
    origin=Origin.spec,
    confidence=1.0,
    canonical_offset=0x2100,
    address_space="snes.cpu",
    tags=[Tag.execution, Tag.structural],
    notes="Picture Processing Unit registers.",

    regions=[
        BytesRegion(
            id="snes.ppu.registers",
            name="PPU Registers",
            address_space="snes.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0x2100,
            size=0x40,
            required=True,
            tags=[Tag.execution],
        ),
    ],
)

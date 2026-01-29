"""
SNES Address Map – HiROM
"""

from constants import Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion

__all__ = ["SNES_ADDRESS_MAP_HIROM"]


SNES_ADDRESS_MAP_HIROM = BytesLayout(
    id="snes.address_map.hirom",
    name="SNES Address Map (HiROM)",
    origin=Origin.spec,
    confidence=1.0,
    canonical_offset=0x000000,
    address_space="snes.cpu",
    tags=[Tag.structural],
    notes="Logical memory map for HiROM cartridges.",

    regions=[
        BytesRegion(
            id="snes.map.hirom.rom",
            name="ROM (banks C0–FF)",
            address_space="snes.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0xC00000,
            size=0x400000,
            required=True,
            tags=[Tag.structural],
        ),
        BytesRegion(
            id="snes.map.hirom.wram",
            name="Work RAM",
            address_space="snes.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0x7E0000,
            size=0x020000,
            required=True,
            tags=[Tag.structural],
        ),
    ],
)

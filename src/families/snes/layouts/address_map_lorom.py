"""
SNES Address Map – LoROM
"""

from constants import Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion

__all__ = ["SNES_ADDRESS_MAP_LOROM"]


SNES_ADDRESS_MAP_LOROM = BytesLayout(
    id="snes.address_map.lorom",
    name="SNES Address Map (LoROM)",
    origin=Origin.spec,
    confidence=1.0,
    canonical_offset=0x000000,
    address_space="snes.cpu",
    tags=[Tag.structural],
    notes="Logical memory map for LoROM cartridges.",
    provides=["address_map"],
    requires=["snes.header.lorom"],
    excludes=["snes.address_map.hirom"],
    applies_to={"mapper": "lorom"},
    regions=[
        BytesRegion(
            id="snes.map.lorom.rom_low",
            name="ROM (banks 00–3F)",
            address_space="snes.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0x008000,
            size=0x8000,
            required=True,
            tags=[Tag.structural],
        ),
        BytesRegion(
            id="snes.map.lorom.wram",
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

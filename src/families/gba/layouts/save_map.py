"""
GBA Cartridge Save Memory Map

These address ranges are standardized but the actual save type
used by a game (SRAM, FLASH, EEPROM) is not guaranteed and
often must be inferred.
"""

from constants import Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion

__all__ = ["GBA_SAVE_MAP_LAYOUT"]


GBA_SAVE_MAP_LAYOUT = BytesLayout(
    id="gba.cartridge.save_map",
    name="GBA Save Memory Address Windows",
    origin=Origin.observed,
    confidence=0.9,
    canonical_offset=0x00000000,
    address_space="gba.cpu",
    tags=[Tag.structural],
    notes="Standardized save memory windows used by commercial cartridges.",
    regions=[
        BytesRegion(
            id="gba.save.sram",
            name="SRAM Save Area",
            address_space="gba.cpu",
            kind=Kind.mapping,
            origin=Origin.observed,
            offset=0x0E000000,
            size=0x00010000,
            required=False,
            tags=[Tag.structural, Tag.optional],
            notes="64KB SRAM window (used by SRAM and FLASH emulation).",
        ),
        BytesRegion(
            id="gba.save.eeprom",
            name="EEPROM Save Interface",
            address_space="gba.cpu",
            kind=Kind.mapping,
            origin=Origin.observed,
            offset=0x0D000000,
            size=0x00002000,
            required=False,
            tags=[Tag.structural, Tag.optional],
            notes="EEPROM interface (addressed via serial protocol).",
        ),
    ],
)

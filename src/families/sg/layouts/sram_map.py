"""
Sega Genesis / Mega Drive – Cartridge SRAM Window
"""

from constants import Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion

__all__ = ["SG_SRAM_MAP_LAYOUT"]


SG_SRAM_MAP_LAYOUT = BytesLayout(
    id="sg.cartridge.sram_map",
    name="SG/MD Cartridge SRAM Window",
    origin=Origin.observed,
    confidence=0.9,
    canonical_offset=0x000000,
    address_space="sg.cpu",
    tags=[Tag.structural, Tag.optional],
    notes="Commonly used address window for battery-backed SRAM.",

    regions=[
        BytesRegion(
            id="sg.sram.window",
            name="SRAM Window",
            address_space="sg.cpu",
            kind=Kind.mapping,
            origin=Origin.observed,
            offset=0x200000,
            size=0x010000,
            required=False,
            tags=[Tag.structural, Tag.optional],
            notes="Typical 64KB SRAM window.",
        ),
    ],
)

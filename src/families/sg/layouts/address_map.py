"""
Sega Genesis / Mega Drive – Address Map
"""

from constants import Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion

__all__ = ["SG_ADDRESS_MAP_LAYOUT"]


SG_ADDRESS_MAP_LAYOUT = BytesLayout(
    id="sg.address_map.standard",
    name="SG/MD Address Map",
    origin=Origin.spec,
    confidence=1.0,
    canonical_offset=0x000000,
    address_space="sg.cpu",
    tags=[Tag.structural],
    notes="Logical memory map of the Mega Drive.",
    provides=[
        "address_map",
        "cpu_memory_view",
    ],
    requires=None,
    excludes=None,
    applies_to=None,

    regions=[
        BytesRegion(
            id="sg.map.rom",
            name="Cartridge ROM",
            address_space="sg.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0x000000,
            size=0x400000,
            required=True,
            tags=[Tag.structural],
            notes="Up to 4MB of ROM space.",
        ),
        BytesRegion(
            id="sg.map.ram",
            name="Main Work RAM",
            address_space="sg.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0xFF0000,
            size=0x010000,
            required=True,
            tags=[Tag.structural],
            notes="64KB system RAM.",
        ),
    ],
)

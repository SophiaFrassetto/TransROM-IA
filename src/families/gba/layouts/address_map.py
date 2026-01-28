"""
GBA Address Map Layout

Describes how the GBA CPU maps different memory regions.
These regions are fixed and independent of the ROM content.
"""

from constants import Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion

__all__ = ["GBA_ADDRESS_MAP_LAYOUT"]


GBA_ADDRESS_MAP_LAYOUT = BytesLayout(
    # Identity
    id="gba.address_map.standard",
    name="GBA Address Map",
    origin=Origin.spec,
    confidence=1.0,
    # Location
    canonical_offset=0x00000000,
    address_space="gba.cpu",

    # Tags
    tags=[Tag.structural],
    notes="Fixed memory map of the Game Boy Advance CPU.",

    # Applicability
    applies_to = None,

    # Relationships
    provides=["address_map", "cpu_memory_view"],
    requires=None,
    excludes=None,
    replaces=None,

    # Regions
    regions=[
        BytesRegion(
            # Identity
            id="gba.map.rom",
            name="Game Pak ROM",
            kind=Kind.mapping,
            origin=Origin.spec,

            # Location (file-based)
            offset=0x08000000,
            size=0x02000000,

            # Interpretation
            encoding=None,
            byte_order=None,
            alignment=None,
            signed=None,

            # Context
            address_space="gba.cpu",
            bank=None,
            mirror_of=None,
            tags=[Tag.structural],

            # Relationships
            points_to=None,
            referenced_by=None,

            # Validation
            required=True,
            default_value_mapped=None,

            # Discovery metadata
            confidence=1.0,
            notes="Up to 32MB of ROM space.",
        ),
        BytesRegion(
            id="gba.map.wram_board",
            name="External WRAM",
            address_space="gba.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0x02000000,
            size=0x00040000,
            required=True,
            tags=[Tag.structural],
            notes="256KB external work RAM.",
        ),
        BytesRegion(
            id="gba.map.wram_chip",
            name="Internal WRAM",
            address_space="gba.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0x03000000,
            size=0x00008000,
            required=True,
            tags=[Tag.structural],
            notes="32KB internal work RAM.",
        ),
        BytesRegion(
            id="gba.map.vram",
            name="Video RAM",
            address_space="gba.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0x06000000,
            size=0x00018000,
            required=True,
            tags=[Tag.structural],
        ),
        BytesRegion(
            id="gba.map.oam",
            name="Object Attribute Memory",
            address_space="gba.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0x07000000,
            size=0x00000400,
            required=True,
            tags=[Tag.structural],
        ),
        BytesRegion(
            id="gba.map.palette",
            name="Palette RAM",
            address_space="gba.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0x05000000,
            size=0x00000400,
            required=True,
            tags=[Tag.structural],
        ),
    ],
)

"""
Sega Genesis / Mega Drive – Z80 Subsystem Map
"""

from constants import Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion

__all__ = ["SG_Z80_MAP_LAYOUT"]


SG_Z80_MAP_LAYOUT = BytesLayout(
    id="sg.system.z80_map",
    name="SG/MD Z80 Subsystem Map",
    origin=Origin.spec,
    confidence=1.0,
    canonical_offset=0xA00000,
    address_space="sg.cpu",
    tags=[Tag.execution, Tag.structural],
    notes="Z80 RAM and bus control registers.",

    regions=[
        BytesRegion(
            id="sg.z80.ram",
            name="Z80 RAM",
            address_space="sg.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0xA00000,
            size=0x2000,
            required=True,
            tags=[Tag.execution],
        ),
        BytesRegion(
            id="sg.z80.bus_request",
            name="Z80 Bus Request",
            address_space="sg.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0xA11100,
            size=2,
            required=True,
            tags=[Tag.execution],
        ),
        BytesRegion(
            id="sg.z80.reset",
            name="Z80 Reset",
            address_space="sg.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0xA11200,
            size=2,
            required=True,
            tags=[Tag.execution],
        ),
    ],
)

"""
Sega Genesis / Mega Drive – VDP Register Map
"""

from constants import Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion

__all__ = ["SG_VDP_REGISTERS_LAYOUT"]


SG_VDP_REGISTERS_LAYOUT = BytesLayout(
    id="sg.system.vdp_registers",
    name="SG/MD VDP Registers",
    origin=Origin.spec,
    confidence=1.0,
    canonical_offset=0xC00000,
    address_space="sg.cpu",
    tags=[Tag.execution, Tag.structural],
    notes="Video Display Processor memory-mapped registers.",
    provides=[
        "video_system",
        "vdp_registers",
    ],
    requires=[
        "sg.address_map.standard",
    ],
    excludes=None,
    applies_to=None,
    regions=[
        BytesRegion(
            id="sg.vdp.data_port",
            name="VDP Data Port",
            address_space="sg.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0xC00000,
            size=2,
            required=True,
            tags=[Tag.execution],
        ),
        BytesRegion(
            id="sg.vdp.control_port",
            name="VDP Control Port",
            address_space="sg.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0xC00004,
            size=2,
            required=True,
            tags=[Tag.execution],
        ),
    ],
)

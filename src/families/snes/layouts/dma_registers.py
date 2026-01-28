"""
SNES DMA / HDMA Register Map
"""

from constants import Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion

__all__ = ["SNES_DMA_REGISTERS"]


SNES_DMA_REGISTERS = BytesLayout(
    id="snes.system.dma_registers",
    name="SNES DMA / HDMA Registers",
    origin=Origin.spec,
    confidence=1.0,
    canonical_offset=0x4300,
    address_space="snes.cpu",
    tags=[Tag.execution, Tag.structural],
    notes="DMA and HDMA channel registers.",
    provides=[
        "dma_system",
    ],

    requires=[
        "snes.address_map.lorom",
        "snes.address_map.hirom",
    ],

    excludes=None,
    applies_to=None,

    regions=[
        BytesRegion(
            id="snes.dma.channel0",
            name="DMA Channel 0 Registers",
            address_space="snes.cpu",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0x4300,
            size=0x10,
            required=True,
            tags=[Tag.execution],
        ),
        # Channels 1–7 are identical
    ],
)

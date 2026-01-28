"""
SNES CPU Vectors – HiROM
"""

from constants import Origin, Tag
from core.bytes_region import BytesLayout
from families.snes.layouts.vectors_lorom import SNES_VECTORS_LOROM

__all__ = ["SNES_VECTORS_HIROM"]


SNES_VECTORS_HIROM = BytesLayout(
    id="snes.vectors.hirom",
    name="SNES CPU Vectors (HiROM)",
    origin=Origin.spec,
    confidence=1.0,
    canonical_offset=0xFFE0,
    address_space="snes.rom",
    tags=[Tag.execution, Tag.structural],
    notes="CPU exception and reset vectors for HiROM cartridges.",
    provides=[
        "execution_vectors",
        "execution_entry",
    ],

    requires=[
        "snes.header.hirom",
        "snes.address_map.hirom",
    ],

    excludes=[
        "snes.vectors.lorom",
    ],

    applies_to={
        "mapper": ["hirom", "exhirom"],
    },
    regions=[
        r.copy_with_offset_delta(0x8000)
        for r in SNES_VECTORS_LOROM.regions
    ],
)

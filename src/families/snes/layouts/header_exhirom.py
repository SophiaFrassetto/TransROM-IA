from constants import Origin, Tag
from core.bytes_region import BytesLayout
from families.snes.layouts.header_lorom import SNES_HEADER_LOROM_LAYOUT

__all__ = ["SNES_HEADER_EXHIROM_LAYOUT"]


SNES_HEADER_EXHIROM_LAYOUT = BytesLayout(
    id="snes.header.exhirom",
    name="SNES Internal Header (ExHiROM)",
    origin=Origin.observed,
    confidence=0.9,
    canonical_offset=0x40FFC0,
    address_space="snes.rom",
    tags=[Tag.structural, Tag.experimental],
    notes="Extended HiROM header for very large cartridges.",

    regions=[r.copy_with_offset_delta(0x400000) for r in SNES_HEADER_LOROM_LAYOUT.regions],
)
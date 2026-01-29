from constants import Origin, Tag
from core.bytes_region import BytesLayout
from families.snes.layouts.header_lorom import SNES_HEADER_LOROM_LAYOUT

__all__ = ["SNES_HEADER_HIROM_LAYOUT"]


SNES_HEADER_HIROM_LAYOUT = BytesLayout(
    id="snes.header.hirom",
    name="SNES Internal Header (HiROM)",
    origin=Origin.spec,
    confidence=1.0,
    canonical_offset=0xFFC0,
    address_space="snes.rom",
    tags=[Tag.structural],
    notes="Canonical HiROM header layout.",
    regions=[r.copy_with_offset_delta(0x8000) for r in SNES_HEADER_LOROM_LAYOUT.regions],
)
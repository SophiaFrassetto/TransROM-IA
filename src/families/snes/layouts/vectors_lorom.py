"""
SNES CPU Vectors – LoROM

CPU vectors for 65C816 processor in LoROM mapping.
Offsets are file offsets corresponding to CPU address space.
"""

from constants import Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion

__all__ = ["SNES_VECTORS_LOROM"]


SNES_VECTORS_LOROM = BytesLayout(
    id="snes.vectors.lorom",
    name="SNES CPU Vectors (LoROM)",
    origin=Origin.spec,
    confidence=1.0,
    canonical_offset=0x7FE0,
    address_space="snes.rom",
    tags=[Tag.execution, Tag.structural],
    notes="CPU exception and reset vectors for LoROM cartridges.",
    provides=["execution_vectors"],
    requires=["snes.header.lorom"],
    excludes=["snes.vectors.hirom"],
    applies_to={"mapper": "lorom"},
    regions=[
        # --- Emulation mode ---
        BytesRegion(
            id="snes.vector.emu.reset",
            name="Emulation Reset Vector",
            address_space="snes.rom",
            kind=Kind.code,
            origin=Origin.spec,
            offset=0x7FFC,
            size=2,
            required=True,
            tags=[Tag.execution, Tag.validation],
        ),
        BytesRegion(
            id="snes.vector.emu.nmi",
            name="Emulation NMI Vector",
            address_space="snes.rom",
            kind=Kind.code,
            origin=Origin.spec,
            offset=0x7FFA,
            size=2,
            required=True,
            tags=[Tag.execution],
        ),
        BytesRegion(
            id="snes.vector.emu.irq",
            name="Emulation IRQ Vector",
            address_space="snes.rom",
            kind=Kind.code,
            origin=Origin.spec,
            offset=0x7FFE,
            size=2,
            required=True,
            tags=[Tag.execution],
        ),

        # --- Native mode ---
        BytesRegion(
            id="snes.vector.native.reset",
            name="Native Reset Vector",
            address_space="snes.rom",
            kind=Kind.code,
            origin=Origin.spec,
            offset=0x7FF4,
            size=2,
            required=True,
            tags=[Tag.execution],
        ),
        BytesRegion(
            id="snes.vector.native.nmi",
            name="Native NMI Vector",
            address_space="snes.rom",
            kind=Kind.code,
            origin=Origin.spec,
            offset=0x7FEA,
            size=2,
            required=True,
            tags=[Tag.execution],
        ),
        BytesRegion(
            id="snes.vector.native.irq",
            name="Native IRQ Vector",
            address_space="snes.rom",
            kind=Kind.code,
            origin=Origin.spec,
            offset=0x7FEE,
            size=2,
            required=True,
            tags=[Tag.execution],
        ),
    ],
)

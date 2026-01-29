"""
GBA Execution Vectors Layout

This layout describes the ARM exception vector table present
at the beginning of every GBA ROM image.

Offsets are fixed and independent of cartridge size.
"""

from constants import Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion

__all__ = ["GBA_VECTORS_LAYOUT"]


GBA_VECTORS_LAYOUT = BytesLayout(
    id="gba.vectors.standard",
    name="GBA ARM Exception Vectors",
    origin=Origin.spec,
    confidence=1.0,
    canonical_offset=0x00000000,
    address_space="gba.rom",
    tags=[Tag.execution, Tag.structural],
    notes=(
        "ARM exception vector table.\n"
        "Most vectors contain a branch instruction to actual handlers.\n"
        "Only the reset vector is strictly required for execution."
    ),
    regions=[
        BytesRegion(
            id="gba.vector.reset",
            name="Reset Vector",
            address_space="gba.rom",
            kind=Kind.code,
            origin=Origin.spec,
            offset=0x00,
            size=4,
            required=True,
            tags=[Tag.execution, Tag.validation],
            notes="Executed immediately after BIOS initialization.",
        ),
        BytesRegion(
            id="gba.vector.undefined_instruction",
            name="Undefined Instruction Vector",
            address_space="gba.rom",
            kind=Kind.code,
            origin=Origin.spec,
            offset=0x04,
            size=4,
            required=True,
            tags=[Tag.execution],
        ),
        BytesRegion(
            id="gba.vector.software_interrupt",
            name="Software Interrupt (SWI) Vector",
            address_space="gba.rom",
            kind=Kind.code,
            origin=Origin.spec,
            offset=0x08,
            size=4,
            required=True,
            tags=[Tag.execution],
        ),
        BytesRegion(
            id="gba.vector.prefetch_abort",
            name="Prefetch Abort Vector",
            address_space="gba.rom",
            kind=Kind.code,
            origin=Origin.spec,
            offset=0x0C,
            size=4,
            required=True,
            tags=[Tag.execution],
        ),
        BytesRegion(
            id="gba.vector.data_abort",
            name="Data Abort Vector",
            address_space="gba.rom",
            kind=Kind.code,
            origin=Origin.spec,
            offset=0x10,
            size=4,
            required=True,
            tags=[Tag.execution],
        ),
        BytesRegion(
            id="gba.vector.reserved",
            name="Reserved Vector",
            address_space="gba.rom",
            kind=Kind.reserved,
            origin=Origin.spec,
            offset=0x14,
            size=4,
            required=True,
            tags=[Tag.structural],
            notes="Reserved; typically unused.",
        ),
        BytesRegion(
            id="gba.vector.irq",
            name="IRQ Vector",
            address_space="gba.rom",
            kind=Kind.code,
            origin=Origin.spec,
            offset=0x18,
            size=4,
            required=True,
            tags=[Tag.execution],
        ),
        BytesRegion(
            id="gba.vector.fiq",
            name="FIQ Vector",
            address_space="gba.rom",
            kind=Kind.code,
            origin=Origin.spec,
            offset=0x1C,
            size=4,
            required=True,
            tags=[Tag.execution],
        ),
    ],
)

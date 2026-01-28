"""
Sega Genesis / Mega Drive – CPU Vector Table

Motorola 68000 exception and interrupt vector table.
Located at the beginning of the ROM image.
"""

from constants import Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion

__all__ = ["SG_VECTORS_LAYOUT"]


SG_VECTORS_LAYOUT = BytesLayout(
    id="sg.vectors.standard",
    name="SG/MD CPU Vectors (68000)",
    origin=Origin.spec,
    confidence=1.0,
    canonical_offset=0x000000,
    address_space="sg.rom",
    tags=[Tag.execution, Tag.structural],
    provides=[
        "execution_vectors",
        "execution_entry",
    ],
    requires=None,
    excludes=None,
    applies_to=None,
    notes=(
        "Motorola 68000 vector table.\n"
        "Vector 0 contains the initial stack pointer.\n"
        "Vector 1 contains the initial program counter."
    ),
    regions=[
        BytesRegion(
            id="sg.vector.initial_stack_pointer",
            name="Initial Stack Pointer",
            address_space="sg.rom",
            kind=Kind.data,
            origin=Origin.spec,
            offset=0x000000,
            size=4,
            required=True,
            tags=[Tag.execution, Tag.validation],
            notes="Loaded into A7 on reset.",
        ),
        BytesRegion(
            id="sg.vector.initial_program_counter",
            name="Initial Program Counter",
            address_space="sg.rom",
            kind=Kind.code,
            origin=Origin.spec,
            offset=0x000004,
            size=4,
            required=True,
            tags=[Tag.execution, Tag.validation],
            notes="Execution starts here after reset.",
        ),
        BytesRegion(
            id="sg.vector.exception_table",
            name="Exception Vector Table",
            address_space="sg.rom",
            kind=Kind.mapping,
            origin=Origin.spec,
            offset=0x000008,
            size=0x3F8,
            required=True,
            tags=[Tag.execution, Tag.structural],
            notes="Remaining exception and interrupt vectors.",
        ),
    ],
)

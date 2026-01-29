# ============================================================
# GBA MULTIBOOT HEADER EXTENSION (OPTIONAL)
#
# Used only for slave/multiboot programs.
# Not required for normal cartridges.
# ============================================================

from constants import ByteOrder, Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion, MappedDefaultValue

__all__ = ["GBA_MULTIBOOT_LAYOUT"]


GBA_MULTIBOOT_LAYOUT = BytesLayout(
    id="gba.header.multiboot",
    name="GBA Multiboot Extension",
    origin=Origin.spec,
    confidence=1.0,
    canonical_offset=0x0C0,
    address_space="gba.rom",
    tags=[Tag.optional, Tag.execution],
    notes="Optional multiboot extension for Normal, Multiplay and Joybus modes.",
    regions=[
        BytesRegion(
            id="gba.header.multiboot.ram_entry_point",
            address_space="gba.rom",
            name="RAM Entry Point",
            kind=Kind.code,
            origin=Origin.spec,
            byte_order=ByteOrder.little,
            confidence=1.0,
            offset=0xC0,
            size=4,
            required=False,
            tags=[Tag.execution, Tag.optional],
        ),
        BytesRegion(
            id="gba.header.multiboot.boot_mode",
            address_space="gba.rom",
            name="Boot Mode",
            kind=Kind.data,
            origin=Origin.spec,
            byte_order=ByteOrder.little,
            confidence=1.0,
            offset=0xC4,
            size=1,
            required=False,
            default_value_mapped=[
                MappedDefaultValue(
                    raw=b"\x00",
                    meaning="Init as 00h - BIOS overwrites this value",
                    origin=Origin.spec,
                    confidence=1.0,
                    id="gba.header.multiboot.boot_mode.init_zero",
                ),
                MappedDefaultValue(
                    raw=b"\x01",
                    meaning="01h: Joybus mode",
                    origin=Origin.spec,
                    confidence=1.0,
                    id="gba.header.multiboot.boot_mode.joybus",
                ),
                MappedDefaultValue(
                    raw=b"\x02",
                    meaning="02h: Normal mode",
                    origin=Origin.spec,
                    confidence=1.0,
                    id="gba.header.multiboot.boot_mode.normal",
                ),
                MappedDefaultValue(
                    raw=b"\x03",
                    meaning="03h: Multiplay mode",
                    origin=Origin.spec,
                    confidence=1.0,
                    id="gba.header.multiboot.boot_mode.multiplay",
                ),
            ],
            tags=[Tag.execution, Tag.optional],
        ),
        BytesRegion(
            id="gba.header.multiboot.slave_id_number",
            address_space="gba.rom",
            name="Slave ID Number",
            kind=Kind.data,
            origin=Origin.spec,
            byte_order=ByteOrder.little,
            confidence=1.0,
            offset=0xC5,
            size=1,
            required=False,
            default_value_mapped=[
                MappedDefaultValue(
                    raw=b"\x00",
                    meaning="Init as 00h - BIOS overwrites this value",
                    origin=Origin.spec,
                    confidence=1.0,
                    id="gba.header.multiboot.slave_id_number.init_zero",
                ),
                MappedDefaultValue(
                    raw=b"\x01",
                    meaning="01h: Slave #1",
                    origin=Origin.spec,
                    confidence=1.0,
                    id="gba.header.multiboot.slave_id_number.slave_1",
                ),
                MappedDefaultValue(
                    raw=b"\x02",
                    meaning="02h: Slave #2",
                    origin=Origin.spec,
                    confidence=1.0,
                    id="gba.header.multiboot.slave_id_number.slave_2",
                ),
                MappedDefaultValue(
                    raw=b"\x03",
                    meaning="03h: Slave #3",
                    origin=Origin.spec,
                    confidence=1.0,
                    id="gba.header.multiboot.slave_id_number.slave_3",
                ),
            ],
            tags=[Tag.execution, Tag.optional],
        ),
        BytesRegion(
            id="gba.header.multiboot.not_used",
            address_space="gba.rom",
            name="Not used",
            kind=Kind.reserved,
            origin=Origin.spec,
            byte_order=ByteOrder.little,
            confidence=1.0,
            offset=0xC6,
            size=26,
            required=False,
            default_value_mapped=[
                MappedDefaultValue(
                    raw=b"\x00" * 26,
                    meaning="Should be zero-filled",
                    origin=Origin.spec,
                    confidence=1.0,
                    id="gba.header.multiboot.not_used.zero_filled",
                )
            ],
            tags=[Tag.structural, Tag.deprecated],
        ),
        BytesRegion(
            id="gba.header.multiboot.joybus_entry_point",
            address_space="gba.rom",
            name="JOYBUS Entry Point",
            kind=Kind.code,
            origin=Origin.spec,
            byte_order=ByteOrder.little,
            confidence=1.0,
            offset=0xE0,
            size=4,
            required=False,
            tags=[Tag.execution, Tag.optional],
        ),
    ],
)

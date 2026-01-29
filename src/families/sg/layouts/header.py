# ============================================================
# SEGA GENESIS / MEGA DRIVE ROM HEADER (0x100–0x1FF)
# ============================================================

from constants import Encoding, Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion, MappedDefaultValue

__all__ = ["SG_HEADER_LAYOUT"]


SG_HEADER_LAYOUT = BytesLayout(
    id="sg.header.standard",
    name="Sega Genesis / Mega Drive Header",
    origin=Origin.spec,
    confidence=1.0,
    canonical_offset=0x100,
    address_space="sg.rom",
    tags=[Tag.structural],
    notes="Single fixed header layout for all standard cartridges.",

    regions=[
        # ------------------------------------------------------------
        # Console Name
        # ------------------------------------------------------------
        BytesRegion(
            id="sg.header.console_name",
            name="Console Name",
            address_space="sg.rom",
            kind=Kind.text,
            origin=Origin.spec,
            encoding=Encoding.ascii,
            offset=0x100,
            size=16,
            required=True,
            tags=[Tag.validation, Tag.informational],
            default_value_mapped=[
                MappedDefaultValue(
                    b"SEGA MEGA DRIVE", "Mega Drive", Origin.observed, 0.95
                ),
                MappedDefaultValue(
                    b"SEGA GENESIS   ", "Genesis", Origin.observed, 0.95
                ),
            ],
            notes="Used by emulators for informal validation.",
        ),
        # ------------------------------------------------------------
        # Copyright
        # ------------------------------------------------------------
        BytesRegion(
            id="sg.header.copyright",
            name="Copyright",
            address_space="sg.rom",
            kind=Kind.text,
            origin=Origin.spec,
            encoding=Encoding.ascii,
            offset=0x110,
            size=16,
            required=True,
            tags=[Tag.informational],
        ),
        # ------------------------------------------------------------
        # Domestic Title (JP)
        # ------------------------------------------------------------
        BytesRegion(
            id="sg.header.domestic_title",
            name="Domestic Title",
            address_space="sg.rom",
            kind=Kind.text,
            origin=Origin.spec,
            encoding=Encoding.ascii,
            offset=0x120,
            size=48,
            required=True,
            tags=[Tag.informational],
        ),
        # ------------------------------------------------------------
        # Overseas Title
        # ------------------------------------------------------------
        BytesRegion(
            id="sg.header.overseas_title",
            name="Overseas Title",
            address_space="sg.rom",
            kind=Kind.text,
            origin=Origin.spec,
            encoding=Encoding.ascii,
            offset=0x150,
            size=48,
            required=True,
            tags=[Tag.informational],
        ),
        # ------------------------------------------------------------
        # Product Code
        # ------------------------------------------------------------
        BytesRegion(
            id="sg.header.product_code",
            name="Product Code",
            address_space="sg.rom",
            kind=Kind.text,
            origin=Origin.spec,
            encoding=Encoding.ascii,
            offset=0x180,
            size=14,
            required=True,
            tags=[Tag.structural, Tag.informational],
            notes="Internal Sega identifier (GM XXXXX-XX).",
        ),
        # ------------------------------------------------------------
        # Product Version
        # ------------------------------------------------------------
        BytesRegion(
            id="sg.header.product_version",
            name="Product Version",
            address_space="sg.rom",
            kind=Kind.text,
            origin=Origin.spec,
            encoding=Encoding.ascii,
            offset=0x18E,
            size=2,
            required=True,
            tags=[Tag.informational],
        ),
        # ------------------------------------------------------------
        # ROM Checksum
        # ------------------------------------------------------------
        BytesRegion(
            id="sg.header.checksum",
            name="ROM Checksum",
            address_space="sg.rom",
            kind=Kind.data,
            origin=Origin.spec,
            offset=0x190,
            size=2,
            required=True,
            tags=[Tag.validation],
            notes="Often incorrect even in official cartridges.",
        ),
        # ------------------------------------------------------------
        # I/O Support
        # ------------------------------------------------------------
        BytesRegion(
            id="sg.header.io_support",
            name="I/O Support",
            address_space="sg.rom",
            kind=Kind.text,
            origin=Origin.spec,
            encoding=Encoding.ascii,
            offset=0x192,
            size=16,
            required=True,
            tags=[Tag.informational],
            notes="Peripheral support hints (often unreliable).",
        ),
        # ------------------------------------------------------------
        # ROM Address Range
        # ------------------------------------------------------------
        BytesRegion(
            id="sg.header.rom_start",
            name="ROM Start Address",
            address_space="sg.rom",
            kind=Kind.data,
            origin=Origin.spec,
            offset=0x1A0,
            size=4,
            required=True,
            tags=[Tag.structural],
            default_value_mapped=[
                MappedDefaultValue(
                    b"\x00\x00\x00\x00", "ROM base", Origin.observed, 0.9
                ),
            ],
        ),
        BytesRegion(
            id="sg.header.rom_end",
            name="ROM End Address",
            address_space="sg.rom",
            kind=Kind.data,
            origin=Origin.spec,
            offset=0x1A4,
            size=4,
            required=True,
            tags=[Tag.structural],
        ),
        # ------------------------------------------------------------
        # External RAM
        # ------------------------------------------------------------
        BytesRegion(
            id="sg.header.ram_start",
            name="RAM Start Address",
            address_space="sg.rom",
            kind=Kind.data,
            origin=Origin.spec,
            offset=0x1A8,
            size=4,
            required=True,
            tags=[Tag.structural],
        ),
        BytesRegion(
            id="sg.header.ram_end",
            name="RAM End Address",
            address_space="sg.rom",
            kind=Kind.data,
            origin=Origin.spec,
            offset=0x1AC,
            size=4,
            required=True,
            tags=[Tag.structural],
        ),
        # ------------------------------------------------------------
        # Backup RAM Info
        # ------------------------------------------------------------
        BytesRegion(
            id="sg.header.backup_ram_id",
            name="Backup RAM ID",
            address_space="sg.rom",
            kind=Kind.text,
            origin=Origin.spec,
            encoding=Encoding.ascii,
            offset=0x1B0,
            size=12,
            required=True,
            tags=[Tag.structural, Tag.informational],
            notes="Indicates presence/type of battery-backed RAM.",
        ),
        BytesRegion(
            id="sg.header.backup_ram_start",
            name="Backup RAM Start",
            address_space="sg.rom",
            kind=Kind.data,
            origin=Origin.spec,
            offset=0x1BC,
            size=4,
            required=True,
            tags=[Tag.structural],
        ),
        BytesRegion(
            id="sg.header.backup_ram_end",
            name="Backup RAM End",
            address_space="sg.rom",
            kind=Kind.data,
            origin=Origin.spec,
            offset=0x1C0,
            size=4,
            required=True,
            tags=[Tag.structural],
        ),
        # ------------------------------------------------------------
        # Modem / Network Info (RARE)
        # ------------------------------------------------------------
        BytesRegion(
            id="sg.header.modem_info",
            name="Modem Info",
            address_space="sg.rom",
            kind=Kind.text,
            origin=Origin.spec,
            encoding=Encoding.ascii,
            offset=0x1C4,
            size=12,
            required=True,
            tags=[Tag.experimental, Tag.informational],
            notes="Used by Sega Meganet titles.",
        ),
        # ------------------------------------------------------------
        # Region Code
        # ------------------------------------------------------------
        BytesRegion(
            id="sg.header.region_code",
            name="Region Code",
            address_space="sg.rom",
            kind=Kind.text,
            origin=Origin.spec,
            encoding=Encoding.ascii,
            offset=0x1F0,
            size=16,
            required=True,
            tags=[Tag.informational],
            default_value_mapped=[
                MappedDefaultValue(b"J", "Japan", Origin.observed, 0.9),
                MappedDefaultValue(b"U", "USA", Origin.observed, 0.9),
                MappedDefaultValue(b"E", "Europe", Origin.observed, 0.9),
                MappedDefaultValue(b"JUE", "Multi-region", Origin.observed, 0.95),
            ],
        ),
    ],
)

# ============================================================
# SNES INTERNAL ROM HEADER – LOGICAL STRUCTURE (32 BYTES)
#
# Offset (relative to header base):
# 00h 21  Game Title
# 15h 1   Map Mode
# 16h 1   ROM Type
# 17h 1   ROM Size
# 18h 1   SRAM Size
# 19h 1   Country Code
# 1Ah 1   Licensee Code
# 1Bh 1   Version
# 1Ch 2   Checksum Complement
# 1Eh 2   Checksum
#
# NOTE:
# SNES does NOT store:
# - Explicit game code (like GBA)
# - Explicit publisher string
# - Explicit mapper ID
#
# These are inferred via Map Mode, ROM Type, and ROM Size.
# ============================================================

from constants import Encoding, Kind, Origin, Tag
from core.bytes_region import BytesLayout, BytesRegion, MappedDefaultValue

__all__ = ["SNES_HEADER_LOROM_LAYOUT"]


SNES_HEADER_LOROM_LAYOUT = BytesLayout(
    id="snes.header.lorom",
    name="SNES Internal Header (LoROM)",
    origin=Origin.spec,
    confidence=1.0,
    canonical_offset=0x7FC0,
    address_space="snes.rom",
    tags=[Tag.structural],
    notes="Canonical LoROM header layout.",
    provides=["header", "identity", "mapper:lorom"],
    requires=[
        "snes.vectors.lorom",
        "snes.address_map.lorom",
    ],
    excludes=[
        "snes.header.hirom",
        "snes.header.exhirom",
    ],
    applies_to={"mapper": "lorom"},
    regions=[
    # ------------------------------------------------------------
    # Game Title
    # ------------------------------------------------------------
    BytesRegion(
        id="snes.header.game_title",
        address_space="snes.rom",
        name="Game Title",
        kind=Kind.text,
        origin=Origin.spec,
        encoding=Encoding.ascii,
        confidence=1.0,
        offset=0x7FC0,
        size=21,
        required=True,
        tags=[Tag.informational],
        notes=(
            "Uppercase ASCII title, padded with spaces. "
            "Used by tools and emulators; not required by hardware."
        ),
    ),

    # ------------------------------------------------------------
    # Map Mode (CRITICAL FIELD)
    # ------------------------------------------------------------
    BytesRegion(
        id="snes.header.map_mode",
        address_space="snes.rom",
        name="Map Mode",
        kind=Kind.data,
        origin=Origin.spec,
        confidence=1.0,
        offset=0x7FD5,
        size=1,
        required=True,
        default_value_mapped=[
            # Official / documented
            MappedDefaultValue(b"\x20", "Slow LoROM", Origin.spec, 1.0),
            MappedDefaultValue(b"\x30", "Fast LoROM", Origin.spec, 1.0),
            MappedDefaultValue(b"\x21", "Slow HiROM", Origin.spec, 1.0),
            MappedDefaultValue(b"\x31", "Fast HiROM", Origin.spec, 1.0),
            # Observed / extended
            MappedDefaultValue(b"\x25", "ExHiROM (observed)", Origin.observed, 0.9),
        ],
        tags=[Tag.structural, Tag.validation],
        notes=(
            "Determines memory mapping and access speed.\n"
            "Bit 7: FastROM flag\n"
            "Lower bits: mapping type (LoROM / HiROM / ExHiROM).\n"
            "This value is essential to locate the correct header."
        ),
    ),

    # ------------------------------------------------------------
    # ROM Type (chips / special hardware)
    # ------------------------------------------------------------
    BytesRegion(
        id="snes.header.rom_type",
        address_space="snes.rom",
        name="ROM Type",
        kind=Kind.data,
        origin=Origin.spec,
        confidence=1.0,
        offset=0x7FD6,
        size=1,
        required=True,
        default_value_mapped=[
            MappedDefaultValue(b"\x00", "ROM only", Origin.spec, 1.0),
            MappedDefaultValue(b"\x01", "ROM + RAM", Origin.spec, 1.0),
            MappedDefaultValue(b"\x02", "ROM + RAM + Battery", Origin.spec, 1.0),
            # Observed coprocessors
            MappedDefaultValue(b"\x03", "SuperFX", Origin.observed, 0.95),
            MappedDefaultValue(b"\x05", "SA-1", Origin.observed, 0.95),
            MappedDefaultValue(b"\x0A", "S-DD1", Origin.observed, 0.9),
        ],
        tags=[Tag.structural, Tag.informational],
        notes=(
            "Indicates presence of SRAM, battery, or coprocessors.\n"
            "Many advanced cartridges include additional CPUs or logic."
        ),
    ),

    # ------------------------------------------------------------
    # ROM Size
    # ------------------------------------------------------------
    BytesRegion(
        id="snes.header.rom_size",
        address_space="snes.rom",
        name="ROM Size",
        kind=Kind.data,
        origin=Origin.spec,
        confidence=1.0,
        offset=0x7FD7,
        size=1,
        required=True,
        tags=[Tag.structural, Tag.informational],
        notes=(
            "Encoded as power-of-two size.\n"
            "Value N represents ROM size = 2^(N+10) bytes.\n"
            "Some ROMs lie about this value; file size is authoritative."
        ),
    ),

    # ------------------------------------------------------------
    # SRAM Size
    # ------------------------------------------------------------
    BytesRegion(
        id="snes.header.sram_size",
        address_space="snes.rom",
        name="SRAM Size",
        kind=Kind.data,
        origin=Origin.spec,
        confidence=1.0,
        offset=0x7FD8,
        size=1,
        required=True,
        tags=[Tag.structural, Tag.informational],
        notes="0 indicates no SRAM. Otherwise encoded similarly to ROM size.",
    ),

    # ------------------------------------------------------------
    # Country / Region
    # ------------------------------------------------------------
    BytesRegion(
        id="snes.header.country",
        address_space="snes.rom",
        name="Country Code",
        kind=Kind.data,
        origin=Origin.spec,
        confidence=1.0,
        offset=0x7FD9,
        size=1,
        required=True,
        default_value_mapped=[
            MappedDefaultValue(b"\x00", "Japan", Origin.spec, 1.0),
            MappedDefaultValue(b"\x01", "USA", Origin.spec, 1.0),
            MappedDefaultValue(b"\x02", "Europe", Origin.spec, 1.0),
        ],
        tags=[Tag.informational],
        notes="Used for regional lockout and video mode assumptions.",
    ),

    # ------------------------------------------------------------
    # Licensee Code
    # ------------------------------------------------------------
    BytesRegion(
        id="snes.header.licensee",
        address_space="snes.rom",
        name="Licensee Code",
        kind=Kind.data,
        origin=Origin.spec,
        confidence=1.0,
        offset=0x7FDA,
        size=1,
        required=True,
        tags=[Tag.informational, Tag.experimental],
        notes="Publisher/licensee identifier. Poorly standardized.",
    ),

    # ------------------------------------------------------------
    # Version
    # ------------------------------------------------------------
    BytesRegion(
        id="snes.header.version",
        address_space="snes.rom",
        name="ROM Version",
        kind=Kind.data,
        origin=Origin.spec,
        confidence=1.0,
        offset=0x7FDB,
        size=1,
        required=True,
        default_value_mapped=[
            MappedDefaultValue(b"\x00", "Initial version", Origin.spec, 1.0),
        ],
        tags=[Tag.informational],
    ),

    # ------------------------------------------------------------
    # Checksum Complement
    # ------------------------------------------------------------
    BytesRegion(
        id="snes.header.checksum_complement",
        address_space="snes.rom",
        name="Checksum Complement",
        kind=Kind.data,
        origin=Origin.spec,
        confidence=1.0,
        offset=0x7FDC,
        size=2,
        required=True,
        tags=[Tag.validation],
        notes="Bitwise complement of the checksum.",
    ),

    # ------------------------------------------------------------
    # Checksum
    # ------------------------------------------------------------
    BytesRegion(
        id="snes.header.checksum",
        address_space="snes.rom",
        name="Checksum",
        kind=Kind.data,
        origin=Origin.spec,
        confidence=1.0,
        offset=0x7FDE,
        size=2,
        required=True,
        tags=[Tag.validation],
        notes=(
            "16-bit checksum of the entire ROM.\n"
            "Frequently incorrect in homebrew and modified ROMs.\n"
            "Used mainly by tools, not by the console itself."
        ),
    ),
],
)
"""
Game Boy Advance (GBA) family specification.

This module defines:
- GBA hardware characteristics
- Cartridge hardware defaults
- Standard cartridge header layout
- Optional multiboot / Joybus extensions

The GBA has a FIXED header location at offset 0x000.
All commercial cartridges must contain a valid header.

Sources:
- GBATEK: https://problemkaputt.de/gbatek.htm
"""

from constants import ByteOrder, CompressionType
from core.family import Family
from families.gba.layouts.address_map import GBA_ADDRESS_MAP_LAYOUT
from families.gba.layouts.header import GBA_HEADER_LAYOUT
from families.gba.layouts.multiboot_header import GBA_MULTIBOOT_LAYOUT
from families.gba.layouts.save_map import GBA_SAVE_MAP_LAYOUT
from families.gba.layouts.vectors import GBA_VECTORS_LAYOUT
from hardware.banking_model import BankingModel
from hardware.cartridge_hardware import CartridgeHardware
from hardware.compression_support import CompressionSupport
from hardware.cpu_info import CPUInfo
from hardware.family_hardware import FamilyHardware
from hardware.memory_model import MemoryModel
from hardware.pointer_model import PointerModel

__all__ = ["GBA_Family"]


# ============================================================
# HARDWARE DESCRIPTION
# ============================================================

gba_family_hardware = (
    FamilyHardware(
        cpu=CPUInfo(
            id="arm7tdmi",
            name="ARM7TDMI",
            bitness=32,
            byte_order=ByteOrder.little,
            supports_thumb=True,
            supports_modes=["arm", "thumb"],
            notes="ARM7TDMI CPU used in GBA, supports ARM and Thumb states",
        ),
        pointer_model=PointerModel(
            common_widths=[32],
            relative_supported=False,
            banked=False,
            default_schema_id="gba.ptr.absolute32",
        ),
        memory_model=MemoryModel(
            address_space_ids=[
                "gba.rom",
                "gba.wram",
                "gba.iram",
                "gba.vram",
                "gba.sram",
            ],
            mirrored=False,
            banked=False,
        ),
        banking_model=BankingModel(
            supported=False,
            types="none",
            bank_size=None,
            notes="GBA cartridges typically do not use bank switching",
        ),
        compression_support=CompressionSupport(
            supported=True,
            common_types=[
                CompressionType.lz77.value,
                CompressionType.huffman.value,
                CompressionType.rle.value,
            ],
            hardware_assisted=True,
            notes="BIOS provides decompression routines",
        ),
    ),
)

gba_cartridge_hardware = (
    CartridgeHardware(
        extra_cpu=False,
        coprocessors=[],
        rtc=False,
        sensors=[],
        rumble=False,
    ),
)

# ============================================================
# FAMILY DEFINITION
# ============================================================

GBA_Family = Family(
    id="gba",
    name="Game Boy Advance",
    extensions=[".gba"],
    hardware=gba_family_hardware,
    default_cartridge_hardware=gba_cartridge_hardware,
    layouts=[
        GBA_HEADER_LAYOUT,
        GBA_MULTIBOOT_LAYOUT,
        GBA_ADDRESS_MAP_LAYOUT,
        GBA_VECTORS_LAYOUT,
        GBA_SAVE_MAP_LAYOUT,
    ],
)

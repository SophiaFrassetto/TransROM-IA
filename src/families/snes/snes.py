"""
Super Nintendo Entertainment System (SNES) family specification.

This module defines:
- SNES hardware characteristics
- Cartridge hardware defaults
- Internal ROM Header layouts (LoROM, HiROM, ExHiROM)

IMPORTANT:
The SNES does NOT have a single fixed header location.
The internal ROM header appears at different file offsets depending on
the cartridge memory mapping type.

Known header locations:
- LoROM   : 0x7FC0
- HiROM   : 0xFFC0
- ExHiROM : 0x40FFC0 (extended, observed in large ROMs)

The header content is semantically identical across layouts;
only the physical file offset differs.

Sources:
- https://snes.nesdev.org/wiki/ROM_header
- https://problemkaputt.de/fullsnes.htm
- Community reverse-engineering (bsnes, ImHex patterns)
"""

from core.family import Family
from families.snes.layouts.address_map_hirom import SNES_ADDRESS_MAP_HIROM
from families.snes.layouts.address_map_lorom import SNES_ADDRESS_MAP_LOROM
from families.snes.layouts.apu_registers import SNES_APU_REGISTERS
from families.snes.layouts.dma_registers import SNES_DMA_REGISTERS
from families.snes.layouts.header_exhirom import SNES_HEADER_EXHIROM_LAYOUT
from families.snes.layouts.header_hirom import SNES_HEADER_HIROM_LAYOUT
from families.snes.layouts.header_lorom import SNES_HEADER_LOROM_LAYOUT
from families.snes.layouts.ppu_registers import SNES_PPU_REGISTERS
from families.snes.layouts.vectors_hirom import SNES_VECTORS_HIROM
from families.snes.layouts.vectors_lorom import SNES_VECTORS_LOROM
from hardware.family_hardware import FamilyHardware
from hardware.cpu_info import CPUInfo
from hardware.pointer_model import PointerModel
from hardware.memory_model import MemoryModel
from hardware.banking_model import BankingModel
from hardware.compression_support import CompressionSupport
from hardware.cartridge_hardware import CartridgeHardware
from constants import ByteOrder

__all__ = ["SNES_Family"]


# ============================================================
# SNES HARDWARE DESCRIPTION
# ============================================================

snes_family_hardware = FamilyHardware(
    cpu=CPUInfo(
        id="65c816",
        name="Ricoh 5A22 (65C816)",
        bitness=16,
        byte_order=ByteOrder.little,
        supports_thumb=None,
        supports_modes=["native", "emulation"],
        notes="65C816-compatible CPU with banked addressing.",
    ),
    pointer_model=PointerModel(
        common_widths=[16, 24],
        relative_supported=True,
        banked=True,
        default_schema_id="snes.ptr.banked",
    ),
    memory_model=MemoryModel(
        address_space_ids=["snes.rom", "snes.wram", "snes.vram", "snes.sram"],
        mirrored=True,
        banked=True,
    ),
    banking_model=BankingModel(
        supported=True,
        types=["LoROM", "HiROM"],
        bank_size=0x8000,
        notes="Bank size and decoding depend on mapping type.",
    ),
    compression_support=CompressionSupport(
        supported=True,
        common_types=["custom", "sdd1"],
        hardware_assisted=True,
        notes="Some cartridges include hardware-assisted decompression.",
    ),
)

snes_cartridge_hardware = CartridgeHardware(
    extra_cpu=True,
    coprocessors=["SuperFX", "SA-1", "DSP", "S-DD1"],
    rtc=False,
    sensors=[],
    rumble=False,
)

# ============================================================
# FAMILY DEFINITION
# ============================================================

SNES_Family = Family(
    id="snes",
    name="Super Nintendo Entertainment System",
    extensions=[".sfc", ".smc"],
    hardware=snes_family_hardware,
    default_cartridge_hardware=snes_cartridge_hardware,
    layouts=[
        SNES_HEADER_LOROM_LAYOUT,
        SNES_HEADER_HIROM_LAYOUT,
        SNES_HEADER_EXHIROM_LAYOUT,
        SNES_VECTORS_LOROM,
        SNES_VECTORS_HIROM,
        SNES_ADDRESS_MAP_LOROM,
        SNES_ADDRESS_MAP_HIROM,
        SNES_DMA_REGISTERS,
        SNES_PPU_REGISTERS,
        SNES_APU_REGISTERS,
    ],
    minimal_layouts=[
        "snes.header.lorom",
        "snes.vectors.lorom",
        "snes.address_map.lorom",
    ],

    layout_domains={
        "header": [
            "snes.header.lorom",
            "snes.header.hirom",
            "snes.header.exhirom",
        ],
        "execution": [
            "snes.vectors.lorom",
            "snes.vectors.hirom",
        ],
        "memory": [
            "snes.address_map.lorom",
            "snes.address_map.hirom",
        ],
        "system": [
            "snes.system.ppu_registers",
            "snes.system.apu_registers",
            "snes.system.dma_registers",
        ],
    },
)

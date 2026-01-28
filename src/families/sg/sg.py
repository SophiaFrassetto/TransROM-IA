"""
Sega Genesis / Mega Drive (SG/MD) family specification.

Header notes:
- Header is located at file offset 0x100–0x1FF
- NOT validated by hardware
- NOT required for execution
- Used by emulators, tools and region-lock code

Sources:
- Sega Retro
- Exodus Emulator Technical Docs
"""

from constants import ByteOrder
from core.family import Family
from families.sg.layouts.address_map import SG_ADDRESS_MAP_LAYOUT
from families.sg.layouts.header import SG_HEADER_LAYOUT
from families.sg.layouts.sram_map import SG_SRAM_MAP_LAYOUT
from families.sg.layouts.vdp_registers import SG_VDP_REGISTERS_LAYOUT
from families.sg.layouts.vectors import SG_VECTORS_LAYOUT
from families.sg.layouts.z80_map import SG_Z80_MAP_LAYOUT
from hardware.family_hardware import FamilyHardware
from hardware.cpu_info import CPUInfo
from hardware.pointer_model import PointerModel
from hardware.memory_model import MemoryModel
from hardware.banking_model import BankingModel
from hardware.compression_support import CompressionSupport
from hardware.cartridge_hardware import CartridgeHardware

__all__ = ["SG_Family"]


# ============================================================
# HARDWARE DESCRIPTION
# ============================================================

sg_family_hardware = FamilyHardware(
    cpu=CPUInfo(
        id="m68000",
        name="Motorola 68000",
        bitness=16,
        byte_order=ByteOrder.big,
        supports_thumb=False,
        supports_modes=[],
        notes="Main CPU used for game logic and execution.",
    ),
    pointer_model=PointerModel(
        common_widths=[24],
        relative_supported=False,
        banked=False,
    ),
    memory_model=MemoryModel(
        address_space_ids=["sg.rom", "sg.ram", "sg.vram"],
        mirrored=True,
        banked=False,
    ),
    banking_model=BankingModel(
        supported=False,
        types=[],
    ),
    compression_support=CompressionSupport(
        supported=False,
        notes="No standard hardware compression.",
    ),
)

sg_cartridge_hardware = CartridgeHardware(
    extra_cpu=False,
    coprocessors=[],
    rtc=False,
    sensors=[],
    rumble=False,
)

# ============================================================
# FAMILY DEFINITION
# ============================================================

SG_Family = Family(
    id="sg",
    name="Sega Genesis / Mega Drive",
    extensions=[".bin", ".gen", ".md"],
    hardware=sg_family_hardware,
    default_cartridge_hardware=sg_cartridge_hardware,
    layouts=[
        SG_HEADER_LAYOUT,
        SG_ADDRESS_MAP_LAYOUT,
        SG_VECTORS_LAYOUT,
        SG_VDP_REGISTERS_LAYOUT,
        SG_Z80_MAP_LAYOUT,
        SG_SRAM_MAP_LAYOUT,
    ],
    minimal_layouts = [
        "sg.vectors.standard",
        "sg.address_map.standard"
    ],
    layout_domains={
        "execution": [
            "sg.vectors.standard",
        ],
        "memory": [
            "sg.address_map.standard",
            "sg.cartridge.sram_map",
        ],
        "system": [
            "sg.system.vdp_registers",
            "sg.system.z80_map",
        ],
        "header": [
            "sg.header.standard",
        ],
    },
)

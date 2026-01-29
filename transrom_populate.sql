-- ============================================================
-- POPULATING DATABASE FROM transrom_legacy_full_export_validated.json
-- Created: 2026-01-28
-- ============================================================

-- ============================================================
-- INSERT FAMILIES
-- ============================================================

INSERT INTO families (id, name, extensions, notes) VALUES
('gba', 'Game Boy Advance', '.gba', NULL),
('snes', 'Super Nintendo Entertainment System', '.sfc,.smc', E'\nSNES cartridge header is not used by the console hardware at runtime; it is metadata for development tools and emulators.'),
('sg', 'Sega Genesis / Mega Drive', '.bin,.gen,.md', NULL);

-- ============================================================
-- INSERT GBA HARDWARE
-- ============================================================

INSERT INTO hardware (id, family_id, cpu_id, cpu_name, cpu_bitness, cpu_byte_order, supports_thumb, supports_modes, pointer_common_widths, pointer_relative_supported, pointer_banked, memory_address_spaces, memory_mirrored, memory_banked, banking_supported, banking_types, compression_supported, compression_types, compression_hardware_assisted, notes, confidence)
VALUES
('gba.hw.default', 'gba', 'arm7tdmi', 'ARM7TDMI', 32, 'little', true, 'arm,thumb', '32', false, false, 'gba.rom,gba.wram,gba.iram,gba.vram,gba.sram', false, false, false, 'none', true, 'lz77,huffman,rle', true, 'ARM7TDMI CPU used in GBA, supports ARM and Thumb states', NULL);

INSERT INTO cartridge_hardware (id, family_id, extra_cpu, coprocessors, rtc, sensors, rumble, notes, confidence)
VALUES
('gba.cartridge.default', 'gba', false, '', false, '', false, NULL, NULL);

-- ============================================================
-- INSERT SNES HARDWARE
-- ============================================================

INSERT INTO hardware (id, family_id, cpu_id, cpu_name, cpu_bitness, cpu_byte_order, supports_thumb, supports_modes, pointer_common_widths, pointer_relative_supported, pointer_banked, memory_address_spaces, memory_mirrored, memory_banked, banking_supported, banking_types, compression_supported, compression_types, compression_hardware_assisted, notes, confidence)
VALUES
('snes.hw.default', 'snes', '65c816', 'Ricoh 5A22 (65C816)', 16, 'little', NULL, 'native,emulation', '16,24', true, true, 'snes.rom,snes.wram,snes.vram,snes.sram', true, true, true, 'LoROM,HiROM', true, 'custom,sdd1', true, '65C816-compatible CPU with banked addressing.', NULL);

INSERT INTO cartridge_hardware (id, family_id, extra_cpu, coprocessors, rtc, sensors, rumble, notes, confidence)
VALUES
('snes.cartridge.default', 'snes', true, 'SuperFX,SA-1,DSP,S-DD1', false, '', false, NULL, NULL);

-- ============================================================
-- INSERT SEGA GENESIS / MEGA DRIVE HARDWARE
-- ============================================================

INSERT INTO hardware (id, family_id, cpu_id, cpu_name, cpu_bitness, cpu_byte_order, supports_thumb, supports_modes, pointer_common_widths, pointer_relative_supported, pointer_banked, memory_address_spaces, memory_mirrored, memory_banked, banking_supported, banking_types, compression_supported, compression_types, compression_hardware_assisted, notes, confidence)
VALUES
('sg.hw.default', 'sg', 'm68000', 'Motorola 68000', 16, 'big', false, '', '24', false, false, 'sg.rom,sg.ram,sg.vram', true, false, false, '', false, '', false, 'Main CPU used for game logic and execution.', NULL);

INSERT INTO cartridge_hardware (id, family_id, extra_cpu, coprocessors, rtc, sensors, rumble, notes, confidence)
VALUES
('sg.cartridge.default', 'sg', false, '', false, '', false, NULL, NULL);

-- ============================================================
-- INSERT GBA LAYOUTS
-- ============================================================

INSERT INTO layouts (id, family_id, name, address_space, origin, confidence, canonical_offset, tags, notes) VALUES
('gba.header.standard', 'gba', 'GBA Cartridge Header', 'gba.rom', 'spec', 1.0, '0x0', 'structural', 'Standard fixed GBA cartridge header.'),
('gba.header.multiboot', 'gba', 'GBA Multiboot Extension', 'gba.rom', 'spec', 1.0, '0xc0', 'optional,execution', 'Optional multiboot extension for Normal, Multiplay and Joybus modes.'),
('gba.address_map.standard', 'gba', 'GBA Address Map', 'gba.cpu', 'spec', 1.0, '0x0', 'structural', 'Fixed memory map of the Game Boy Advance CPU.'),
('gba.vectors.standard', 'gba', 'GBA ARM Exception Vectors', 'gba.rom', 'spec', 1.0, '0x0', 'execution,structural', 'ARM exception vector table. Most vectors contain a branch instruction to actual handlers. Only the reset vector is strictly required for execution.'),
('gba.cartridge.save_map', 'gba', 'GBA Save Memory Address Windows', 'gba.cpu', 'observed', 0.9, '0x0', 'structural', 'Standardized save memory windows used by commercial cartridges. EEPROM uses a serial protocol; actual size varies (512B–8KB). Mapped window represents CPU-visible address range, not physical size.');

-- ============================================================
-- INSERT GBA REGIONS FOR gba.header.standard
-- ============================================================

INSERT INTO regions (id, layout_id, name, address_space, kind, origin, confidence, offset, size, required, tags, encoding, byte_order, bank, notes) VALUES
('gba.header', 'gba.header.standard', 'GBA Cartridge Header', 'gba.rom', 'header', 'spec', 1.0, '0x0', 192, true, 'structural', NULL, 'little', NULL, 'Standard fixed GBA cartridge header located at the beginning of the ROM.'),
('gba.header.entry_point', 'gba.header.standard', 'ROM Entry Point', 'gba.rom', 'code', 'spec', 1.0, '0x0', 4, true, 'execution,validation', NULL, 'little', NULL, '32-bit ARM branch instruction'),
('gba.header.nintendo_logo', 'gba.header.standard', 'Nintendo Logo', 'gba.rom', 'reserved', 'spec', 1.0, '0x4', 156, true, 'validation', NULL, 'little', NULL, 'Compressed bitmap, must match official logo'),
('gba.header.game_title', 'gba.header.standard', 'Game Title', 'gba.rom', 'text', 'spec', 1.0, '0xa0', 12, true, 'informational', 'ascii', 'little', NULL, NULL),
('gba.header.game_code', 'gba.header.standard', 'Game Code', 'gba.rom', 'text', 'spec', 1.0, '0xac', 4, true, 'informational,structural', 'ascii', 'little', NULL, NULL),
('gba.header.game_code.unique', 'gba.header.standard', 'Game Code – Unique ID', 'gba.rom', 'text', 'spec', 1.0, '0xac', 1, true, 'informational,structural', 'ascii', 'little', NULL, NULL),
('gba.header.game_code.short_title', 'gba.header.standard', 'Game Code – Short Title', 'gba.rom', 'text', 'spec', 1.0, '0xad', 2, true, 'informational', 'ascii', 'little', NULL, NULL),
('gba.header.game_code.region', 'gba.header.standard', 'Game Code – Region', 'gba.rom', 'text', 'spec', 1.0, '0xaf', 1, true, 'informational', 'ascii', 'little', NULL, NULL),
('gba.header.maker_code', 'gba.header.standard', 'Maker Code', 'gba.rom', 'text', 'spec', 1.0, '0xb0', 2, true, 'informational', 'ascii', 'little', NULL, NULL),
('gba.header.fixed_value', 'gba.header.standard', 'Fixed Value (0x96)', 'gba.rom', 'reserved', 'spec', 1.0, '0xb2', 1, true, 'validation', NULL, 'little', NULL, NULL),
('gba.header.main_unit_code', 'gba.header.standard', 'Main Unit Code', 'gba.rom', 'data', 'spec', 1.0, '0xb3', 1, true, 'validation,structural', NULL, 'little', NULL, '00h for standard GBA'),
('gba.header.device_type', 'gba.header.standard', 'Device Type', 'gba.rom', 'data', 'spec', 1.0, '0xb4', 1, true, 'validation', NULL, 'little', NULL, NULL),
('gba.header.reserved_1', 'gba.header.standard', 'Reserved Area', 'gba.rom', 'reserved', 'spec', 1.0, '0xb5', 7, true, 'validation,deprecated', NULL, 'little', NULL, NULL),
('gba.header.software_version', 'gba.header.standard', 'Software Version', 'gba.rom', 'data', 'spec', 1.0, '0xbc', 1, true, 'informational', NULL, 'little', NULL, NULL),
('gba.header.checksum', 'gba.header.standard', 'Header Checksum', 'gba.rom', 'data', 'spec', 1.0, '0xbd', 1, true, 'validation', NULL, 'little', NULL, 'Complement check of bytes 0xA0–0xBC'),
('gba.header.reserved_2', 'gba.header.standard', 'Reserved Area', 'gba.rom', 'reserved', 'spec', 1.0, '0xbe', 2, true, 'validation,deprecated', NULL, 'little', NULL, NULL);

-- ============================================================
-- INSERT GBA REGIONS FOR gba.header.multiboot
-- ============================================================

INSERT INTO regions (id, layout_id, name, address_space, kind, origin, confidence, offset, size, required, tags, encoding, byte_order, bank, notes) VALUES
('gba.header.multiboot.ram_entry_point', 'gba.header.multiboot', 'RAM Entry Point', 'gba.rom', 'code', 'spec', 1.0, '0xc0', 4, false, 'execution,optional', NULL, 'little', NULL, NULL),
('gba.header.multiboot.boot_mode', 'gba.header.multiboot', 'Boot Mode', 'gba.rom', 'data', 'spec', 1.0, '0xc4', 1, false, 'execution,optional', NULL, 'little', NULL, NULL),
('gba.header.multiboot.slave_id_number', 'gba.header.multiboot', 'Slave ID Number', 'gba.rom', 'data', 'spec', 1.0, '0xc5', 1, false, 'execution,optional', NULL, 'little', NULL, NULL),
('gba.header.multiboot.not_used', 'gba.header.multiboot', 'Not used', 'gba.rom', 'reserved', 'spec', 1.0, '0xc6', 26, false, 'structural,deprecated', NULL, 'little', NULL, NULL),
('gba.header.multiboot.joybus_entry_point', 'gba.header.multiboot', 'JOYBUS Entry Point', 'gba.rom', 'code', 'spec', 1.0, '0xe0', 4, false, 'execution,optional', NULL, 'little', NULL, NULL);

-- ============================================================
-- INSERT GBA REGIONS FOR gba.address_map.standard
-- ============================================================

INSERT INTO regions (id, layout_id, name, address_space, kind, origin, confidence, offset, size, required, tags, encoding, byte_order, bank, notes) VALUES
('gba.map.rom', 'gba.address_map.standard', 'Game Pak ROM', 'gba.cpu', 'mapping', 'spec', 1.0, '0x8000000', 33554432, true, 'structural', NULL, NULL, NULL, 'Up to 32MB of ROM space.'),
('gba.map.wram_board', 'gba.address_map.standard', 'External WRAM', 'gba.cpu', 'mapping', 'spec', NULL, '0x2000000', 262144, true, 'structural', NULL, NULL, NULL, '256KB external work RAM.'),
('gba.map.wram_chip', 'gba.address_map.standard', 'Internal WRAM', 'gba.cpu', 'mapping', 'spec', NULL, '0x3000000', 32768, true, 'structural', NULL, NULL, NULL, '32KB internal work RAM.'),
('gba.map.vram', 'gba.address_map.standard', 'Video RAM', 'gba.cpu', 'mapping', 'spec', NULL, '0x6000000', 98304, true, 'structural', NULL, NULL, NULL, NULL),
('gba.map.oam', 'gba.address_map.standard', 'Object Attribute Memory', 'gba.cpu', 'mapping', 'spec', NULL, '0x7000000', 1024, true, 'structural', NULL, NULL, NULL, NULL),
('gba.map.palette', 'gba.address_map.standard', 'Palette RAM', 'gba.cpu', 'mapping', 'spec', NULL, '0x5000000', 1024, true, 'structural', NULL, NULL, NULL, NULL);

-- ============================================================
-- INSERT GBA REGIONS FOR gba.vectors.standard
-- ============================================================

INSERT INTO regions (id, layout_id, name, address_space, kind, origin, confidence, offset, size, required, tags, encoding, byte_order, bank, notes) VALUES
('gba.vector.reset', 'gba.vectors.standard', 'Reset Vector', 'gba.rom', 'code', 'spec', NULL, '0x0', 4, true, 'execution,validation', NULL, NULL, NULL, 'Executed immediately after BIOS initialization.'),
('gba.vector.undefined_instruction', 'gba.vectors.standard', 'Undefined Instruction Vector', 'gba.rom', 'code', 'spec', NULL, '0x4', 4, true, 'execution', NULL, NULL, NULL, NULL),
('gba.vector.software_interrupt', 'gba.vectors.standard', 'Software Interrupt (SWI) Vector', 'gba.rom', 'code', 'spec', NULL, '0x8', 4, true, 'execution', NULL, NULL, NULL, NULL),
('gba.vector.prefetch_abort', 'gba.vectors.standard', 'Prefetch Abort Vector', 'gba.rom', 'code', 'spec', NULL, '0xc', 4, true, 'execution', NULL, NULL, NULL, NULL),
('gba.vector.data_abort', 'gba.vectors.standard', 'Data Abort Vector', 'gba.rom', 'code', 'spec', NULL, '0x10', 4, true, 'execution', NULL, NULL, NULL, NULL),
('gba.vector.reserved', 'gba.vectors.standard', 'Reserved Vector', 'gba.rom', 'reserved', 'spec', NULL, '0x14', 4, true, 'structural', NULL, NULL, NULL, 'Reserved; typically unused.'),
('gba.vector.irq', 'gba.vectors.standard', 'IRQ Vector', 'gba.rom', 'code', 'spec', NULL, '0x18', 4, true, 'execution', NULL, NULL, NULL, NULL),
('gba.vector.fiq', 'gba.vectors.standard', 'FIQ Vector', 'gba.rom', 'code', 'spec', NULL, '0x1c', 4, true, 'execution', NULL, NULL, NULL, NULL);

-- ============================================================
-- INSERT GBA REGIONS FOR gba.cartridge.save_map
-- ============================================================

INSERT INTO regions (id, layout_id, name, address_space, kind, origin, confidence, offset, size, required, tags, encoding, byte_order, bank, notes) VALUES
('gba.save.sram', 'gba.cartridge.save_map', 'SRAM Save Area', 'gba.cpu', 'mapping', 'observed', NULL, '0xe000000', 65536, false, 'structural,optional', NULL, NULL, NULL, '64KB SRAM window (used by SRAM and FLASH emulation).'),
('gba.save.eeprom', 'gba.cartridge.save_map', 'EEPROM Save Interface', 'gba.cpu', 'mapping', 'observed', NULL, '0xd000000', 8192, false, 'structural,optional', NULL, NULL, NULL, 'EEPROM interface (addressed via serial protocol).');

-- ============================================================
-- INSERT SNES LAYOUTS
-- ============================================================

INSERT INTO layouts (id, family_id, name, address_space, origin, confidence, canonical_offset, tags, notes) VALUES
('snes.header.lorom', 'snes', 'SNES Internal Header (LoROM)', 'snes.rom', 'spec', 1.0, '0x7fc0', 'structural', 'Canonical LoROM header layout.'),
('snes.header.hirom', 'snes', 'SNES Internal Header (HiROM)', 'snes.rom', 'spec', 1.0, '0xffc0', 'structural', 'Canonical HiROM header layout.'),
('snes.header.exhirom', 'snes', 'SNES Internal Header (ExHiROM)', 'snes.rom', 'observed', 0.9, '0x40ffc0', 'structural,experimental', 'Extended HiROM header for very large cartridges.'),
('snes.vectors.lorom', 'snes', 'SNES CPU Vectors (LoROM)', 'snes.rom', 'spec', 1.0, '0x7fe0', 'execution,structural', 'CPU exception and reset vectors for LoROM cartridges.'),
('snes.vectors.hirom', 'snes', 'SNES CPU Vectors (HiROM)', 'snes.rom', 'spec', 1.0, '0xffe0', 'execution,structural', 'CPU exception and reset vectors for HiROM cartridges.'),
('snes.address_map.lorom', 'snes', 'SNES Address Map (LoROM)', 'snes.cpu', 'spec', 1.0, '0x0', 'structural,logical', 'Logical memory map for LoROM cartridges. This address map is a logical representation of the SNES memory model. Actual physical mapping is banked and depends on mapper.'),
('snes.address_map.hirom', 'snes', 'SNES Address Map (HiROM)', 'snes.cpu', 'spec', 1.0, '0x0', 'structural,logical', 'Logical memory map for HiROM cartridges. This address map is a logical representation of the SNES memory model. Actual physical mapping is banked and depends on mapper.'),
('snes.system.dma_registers', 'snes', 'SNES DMA / HDMA Registers', 'snes.cpu', 'spec', 1.0, '0x4300', 'execution,structural', 'DMA and HDMA channel registers.'),
('snes.system.ppu_registers', 'snes', 'SNES PPU Registers', 'snes.cpu', 'spec', 1.0, '0x2100', 'execution,structural', 'Picture Processing Unit registers.'),
('snes.system.apu_registers', 'snes', 'SNES APU Registers', 'snes.cpu', 'spec', 1.0, '0x2140', 'execution,structural', 'Audio Processing Unit I/O registers.');

-- ============================================================
-- INSERT SNES REGIONS FOR snes.header.lorom
-- ============================================================

INSERT INTO regions (id, layout_id, name, address_space, kind, origin, confidence, offset, size, required, tags, encoding, byte_order, bank, notes) VALUES
('snes.lorom.game_title', 'snes.header.lorom', 'Game Title', 'snes.rom', 'text', 'spec', 1.0, '0x7fc0', 21, true, 'informational', 'ascii', NULL, NULL, 'Uppercase ASCII title, padded with spaces. Used by tools and emulators; not required by hardware.'),
('snes.lorom.map_mode', 'snes.header.lorom', 'Map Mode', 'snes.rom', 'data', 'spec', 1.0, '0x7fd5', 1, true, 'structural,validation', NULL, NULL, NULL, 'Determines memory mapping and access speed. Bit 7: FastROM flag. Lower bits: mapping type (LoROM / HiROM / ExHiROM). This value is essential to locate the correct header.'),
('snes.lorom.rom_type', 'snes.header.lorom', 'ROM Type', 'snes.rom', 'data', 'spec', 1.0, '0x7fd6', 1, true, 'structural,informational', NULL, NULL, NULL, 'Indicates presence of SRAM, battery, or coprocessors. Many advanced cartridges include additional CPUs or logic.'),
('snes.lorom.rom_size', 'snes.header.lorom', 'ROM Size', 'snes.rom', 'data', 'spec', 1.0, '0x7fd7', 1, true, 'structural,informational', NULL, NULL, NULL, 'Encoded as power-of-two size. Value N represents ROM size = 2^(N+10) bytes. Some ROMs lie about this value; file size is authoritative.'),
('snes.lorom.sram_size', 'snes.header.lorom', 'SRAM Size', 'snes.rom', 'data', 'spec', 1.0, '0x7fd8', 1, true, 'structural,informational', NULL, NULL, NULL, '0 indicates no SRAM. Otherwise encoded similarly to ROM size.'),
('snes.lorom.country', 'snes.header.lorom', 'Country Code', 'snes.rom', 'data', 'spec', 1.0, '0x7fd9', 1, true, 'informational', NULL, NULL, NULL, 'Used for regional lockout and video mode assumptions.'),
('snes.lorom.licensee', 'snes.header.lorom', 'Licensee Code', 'snes.rom', 'data', 'spec', 1.0, '0x7fda', 1, true, 'informational,experimental', NULL, NULL, NULL, 'Publisher/licensee identifier. Poorly standardized.'),
('snes.lorom.version', 'snes.header.lorom', 'ROM Version', 'snes.rom', 'data', 'spec', 1.0, '0x7fdb', 1, true, 'informational', NULL, NULL, NULL, NULL),
('snes.lorom.checksum_complement', 'snes.header.lorom', 'Checksum Complement', 'snes.rom', 'data', 'spec', 1.0, '0x7fdc', 2, true, 'validation', NULL, NULL, NULL, 'Bitwise complement of the checksum.'),
('snes.lorom.checksum', 'snes.header.lorom', 'Checksum', 'snes.rom', 'data', 'spec', 1.0, '0x7fde', 2, true, 'validation', NULL, NULL, NULL, '16-bit checksum of the entire ROM. Frequently incorrect in homebrew and modified ROMs. Used mainly by tools, not by the console itself.');

-- ============================================================
-- INSERT SNES REGIONS FOR snes.address_map.lorom
-- ============================================================

INSERT INTO regions (id, layout_id, name, address_space, kind, origin, confidence, offset, size, required, tags, encoding, byte_order, bank, notes) VALUES
('snes.map.lorom.rom_low', 'snes.address_map.lorom', 'ROM (banks 00–3F)', 'snes.cpu', 'mapping', 'spec', NULL, '0x8000', 32768, true, 'structural', NULL, NULL, NULL, NULL),
('snes.map.lorom.wram', 'snes.address_map.lorom', 'Work RAM', 'snes.cpu', 'mapping', 'spec', NULL, '0x7e0000', 131072, true, 'structural', NULL, NULL, NULL, NULL);

-- ============================================================
-- INSERT SNES REGIONS FOR snes.vectors.lorom
-- ============================================================

INSERT INTO regions (id, layout_id, name, address_space, kind, origin, confidence, offset, size, required, tags, encoding, byte_order, bank, notes) VALUES
('snes.lorom.vector.emu.reset', 'snes.vectors.lorom', 'Emulation Reset Vector', 'snes.rom', 'code', 'spec', NULL, '0x7ffc', 2, true, 'execution,validation', NULL, NULL, NULL, NULL),
('snes.lorom.vector.emu.nmi', 'snes.vectors.lorom', 'Emulation NMI Vector', 'snes.rom', 'code', 'spec', NULL, '0x7ffa', 2, true, 'execution', NULL, NULL, NULL, NULL),
('snes.lorom.vector.emu.irq', 'snes.vectors.lorom', 'Emulation IRQ Vector', 'snes.rom', 'code', 'spec', NULL, '0x7ffe', 2, true, 'execution', NULL, NULL, NULL, NULL),
('snes.lorom.vector.native.reset', 'snes.vectors.lorom', 'Native Reset Vector', 'snes.rom', 'code', 'spec', NULL, '0x7ff4', 2, true, 'execution', NULL, NULL, NULL, NULL),
('snes.lorom.vector.native.nmi', 'snes.vectors.lorom', 'Native NMI Vector', 'snes.rom', 'code', 'spec', NULL, '0x7fea', 2, true, 'execution', NULL, NULL, NULL, NULL),
('snes.lorom.vector.native.irq', 'snes.vectors.lorom', 'Native IRQ Vector', 'snes.rom', 'code', 'spec', NULL, '0x7fee', 2, true, 'execution', NULL, NULL, NULL, NULL);

-- ============================================================
-- INSERT SEGA GENESIS LAYOUTS
-- ============================================================

INSERT INTO layouts (id, family_id, name, address_space, origin, confidence, canonical_offset, tags, notes) VALUES
('sg.header.standard', 'sg', 'Sega Genesis / Mega Drive Header', 'sg.rom', 'spec', 1.0, '0x100', 'structural', 'Single fixed header layout for all standard cartridges. Checksum is frequently incorrect in commercial ROMs; many emulators ignore this field.'),
('sg.address_map.standard', 'sg', 'SG/MD Address Map', 'sg.cpu', 'spec', 1.0, '0x0', 'structural', 'Logical memory map of the Mega Drive.'),
('sg.vectors.standard', 'sg', 'SG/MD CPU Vectors (68000)', 'sg.rom', 'spec', 1.0, '0x0', 'execution,structural', 'Motorola 68000 vector table. Vector 0 contains the initial stack pointer. Vector 1 contains the initial program counter.'),
('sg.system.vdp_registers', 'sg', 'SG/MD VDP Registers', 'sg.cpu', 'spec', 1.0, '0xc00000', 'execution,structural', 'Video Display Processor memory-mapped registers.'),
('sg.system.z80_map', 'sg', 'SG/MD Z80 Subsystem Map', 'sg.cpu', 'spec', 1.0, '0xa00000', 'execution,structural', 'Z80 RAM and bus control registers.'),
('sg.cartridge.sram_map', 'sg', 'SG/MD Cartridge SRAM Window', 'sg.cpu', 'observed', 0.9, '0x0', 'structural,optional', 'Commonly used address window for battery-backed SRAM.');

-- ============================================================
-- INSERT SEGA GENESIS REGIONS FOR sg.header.standard
-- ============================================================

INSERT INTO regions (id, layout_id, name, address_space, kind, origin, confidence, offset, size, required, tags, encoding, byte_order, bank, notes) VALUES
('sg.header.console_name', 'sg.header.standard', 'Console Name', 'sg.rom', 'text', 'spec', NULL, '0x100', 16, true, 'validation,informational', 'ascii', NULL, NULL, 'Used by emulators for informal validation.'),
('sg.header.copyright', 'sg.header.standard', 'Copyright', 'sg.rom', 'text', 'spec', NULL, '0x110', 16, true, 'informational', 'ascii', NULL, NULL, NULL),
('sg.header.domestic_title', 'sg.header.standard', 'Domestic Title', 'sg.rom', 'text', 'spec', NULL, '0x120', 48, true, 'informational', 'ascii', NULL, NULL, NULL),
('sg.header.overseas_title', 'sg.header.standard', 'Overseas Title', 'sg.rom', 'text', 'spec', NULL, '0x150', 48, true, 'informational', 'ascii', NULL, NULL, NULL),
('sg.header.product_code', 'sg.header.standard', 'Product Code', 'sg.rom', 'text', 'spec', NULL, '0x180', 14, true, 'structural,informational', 'ascii', NULL, NULL, 'Internal Sega identifier (GM XXXXX-XX).'),
('sg.header.product_version', 'sg.header.standard', 'Product Version', 'sg.rom', 'text', 'spec', NULL, '0x18e', 2, true, 'informational', 'ascii', NULL, NULL, NULL),
('sg.header.checksum', 'sg.header.standard', 'ROM Checksum', 'sg.rom', 'data', 'spec', NULL, '0x190', 2, true, 'validation', NULL, NULL, NULL, 'Often incorrect even in official cartridges.'),
('sg.header.io_support', 'sg.header.standard', 'I/O Support', 'sg.rom', 'text', 'spec', NULL, '0x192', 16, true, 'informational', 'ascii', NULL, NULL, 'Peripheral support hints (often unreliable).'),
('sg.header.rom_start', 'sg.header.standard', 'ROM Start Address', 'sg.rom', 'data', 'spec', NULL, '0x1a0', 4, true, 'structural', NULL, NULL, NULL, NULL),
('sg.header.rom_end', 'sg.header.standard', 'ROM End Address', 'sg.rom', 'data', 'spec', NULL, '0x1a4', 4, true, 'structural', NULL, NULL, NULL, NULL),
('sg.header.ram_start', 'sg.header.standard', 'RAM Start Address', 'sg.rom', 'data', 'spec', NULL, '0x1a8', 4, true, 'structural', NULL, NULL, NULL, NULL),
('sg.header.ram_end', 'sg.header.standard', 'RAM End Address', 'sg.rom', 'data', 'spec', NULL, '0x1ac', 4, true, 'structural', NULL, NULL, NULL, NULL),
('sg.header.backup_ram_id', 'sg.header.standard', 'Backup RAM ID', 'sg.rom', 'text', 'spec', NULL, '0x1b0', 12, true, 'structural,informational', 'ascii', NULL, NULL, 'Indicates presence/type of battery-backed RAM.'),
('sg.header.backup_ram_start', 'sg.header.standard', 'Backup RAM Start', 'sg.rom', 'data', 'spec', NULL, '0x1bc', 4, true, 'structural', NULL, NULL, NULL, NULL),
('sg.header.backup_ram_end', 'sg.header.standard', 'Backup RAM End', 'sg.rom', 'data', 'spec', NULL, '0x1c0', 4, true, 'structural', NULL, NULL, NULL, NULL),
('sg.header.modem_info', 'sg.header.standard', 'Modem Info', 'sg.rom', 'text', 'spec', NULL, '0x1c4', 12, true, 'experimental,informational', 'ascii', NULL, NULL, 'Used by Sega Meganet titles.'),
('sg.header.region_code', 'sg.header.standard', 'Region Code', 'sg.rom', 'text', 'spec', NULL, '0x1f0', 16, true, 'informational', 'ascii', NULL, NULL, NULL);

-- ============================================================
-- INSERT SEGA GENESIS REGIONS FOR sg.address_map.standard
-- ============================================================

INSERT INTO regions (id, layout_id, name, address_space, kind, origin, confidence, offset, size, required, tags, encoding, byte_order, bank, notes) VALUES
('sg.map.rom', 'sg.address_map.standard', 'Cartridge ROM', 'sg.cpu', 'mapping', 'spec', NULL, '0x0', 4194304, true, 'structural', NULL, NULL, NULL, 'Up to 4MB of ROM space.'),
('sg.map.ram', 'sg.address_map.standard', 'Main Work RAM', 'sg.cpu', 'mapping', 'spec', NULL, '0xff0000', 65536, true, 'structural', NULL, NULL, NULL, '64KB system RAM.');

-- ============================================================
-- INSERT SEGA GENESIS REGIONS FOR sg.vectors.standard
-- ============================================================

INSERT INTO regions (id, layout_id, name, address_space, kind, origin, confidence, offset, size, required, tags, encoding, byte_order, bank, notes) VALUES
('sg.vector.initial_stack_pointer', 'sg.vectors.standard', 'Initial Stack Pointer', 'sg.rom', 'data', 'spec', NULL, '0x0', 4, true, 'execution,validation', NULL, NULL, NULL, 'Loaded into A7 on reset.'),
('sg.vector.initial_program_counter', 'sg.vectors.standard', 'Initial Program Counter', 'sg.rom', 'code', 'spec', NULL, '0x4', 4, true, 'execution,validation', NULL, NULL, NULL, 'Execution starts here after reset.'),
('sg.vector.exception_table', 'sg.vectors.standard', 'Exception Vector Table', 'sg.rom', 'mapping', 'spec', NULL, '0x8', 1016, true, 'execution,structural', NULL, NULL, NULL, 'Remaining exception and interrupt vectors.');

-- ============================================================
-- INSERT SEGA GENESIS REGIONS FOR sg.system.vdp_registers
-- ============================================================

INSERT INTO regions (id, layout_id, name, address_space, kind, origin, confidence, offset, size, required, tags, encoding, byte_order, bank, notes) VALUES
('sg.vdp.data_port', 'sg.system.vdp_registers', 'VDP Data Port', 'sg.cpu', 'mapping', 'spec', NULL, '0xc00000', 2, true, 'execution', NULL, NULL, NULL, NULL),
('sg.vdp.control_port', 'sg.system.vdp_registers', 'VDP Control Port', 'sg.cpu', 'mapping', 'spec', NULL, '0xc00004', 2, true, 'execution', NULL, NULL, NULL, NULL);

-- ============================================================
-- INSERT SEGA GENESIS REGIONS FOR sg.system.z80_map
-- ============================================================

INSERT INTO regions (id, layout_id, name, address_space, kind, origin, confidence, offset, size, required, tags, encoding, byte_order, bank, notes) VALUES
('sg.z80.ram', 'sg.system.z80_map', 'Z80 RAM', 'sg.cpu', 'mapping', 'spec', NULL, '0xa00000', 8192, true, 'execution', NULL, NULL, NULL, NULL),
('sg.z80.bus_request', 'sg.system.z80_map', 'Z80 Bus Request', 'sg.cpu', 'mapping', 'spec', NULL, '0xa11100', 2, true, 'execution', NULL, NULL, NULL, NULL),
('sg.z80.reset', 'sg.system.z80_map', 'Z80 Reset', 'sg.cpu', 'mapping', 'spec', NULL, '0xa11200', 2, true, 'execution', NULL, NULL, NULL, NULL);

-- ============================================================
-- INSERT SEGA GENESIS REGIONS FOR sg.cartridge.sram_map
-- ============================================================

INSERT INTO regions (id, layout_id, name, address_space, kind, origin, confidence, offset, size, required, tags, encoding, byte_order, bank, notes) VALUES
('sg.sram.window', 'sg.cartridge.sram_map', 'SRAM Window', 'sg.cpu', 'mapping', 'observed', NULL, '0x200000', 65536, false, 'structural,optional', NULL, NULL, NULL, 'Typical 64KB SRAM window.');

-- ============================================================
-- INSERT GBA DEFAULT VALUES MAPPED
-- ============================================================

-- gba.header.game_code.unique
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('gba.header.game_code.unique.a', 'gba.header.game_code.unique', '0x41', 'Normal game; Older titles (mainly 2001..2003)', 'spec', 1.0),
('gba.header.game_code.unique.b', 'gba.header.game_code.unique', '0x42', 'Normal game; Newer titles (2003..)', 'spec', 1.0),
('gba.header.game_code.unique.c', 'gba.header.game_code.unique', '0x43', 'Normal game; Not used yet, but might be used for even newer titles', 'spec', 1.0),
('gba.header.game_code.unique.f', 'gba.header.game_code.unique', '0x46', 'Famicom/Classic NES Series (software emulated NES games)', 'spec', 1.0),
('gba.header.game_code.unique.k', 'gba.header.game_code.unique', '0x4b', 'Yoshi and Koro Koro Puzzle (acceleration sensor)', 'spec', 1.0),
('gba.header.game_code.unique.p', 'gba.header.game_code.unique', '0x50', 'e-Reader (dot-code scanner) (or NDS PassMe image when gamecode=''PASS'')', 'spec', 1.0),
('gba.header.game_code.unique.r', 'gba.header.game_code.unique', '0x52', 'Warioware Twisted (cartridge with rumble and z-axis gyro sensor)', 'spec', 1.0),
('gba.header.game_code.unique.u', 'gba.header.game_code.unique', '0x55', 'Boktai 1 and 2 (cartridge with RTC and solar sensor)', 'spec', 1.0),
('gba.header.game_code.unique.v', 'gba.header.game_code.unique', '0x56', 'Drill Dozer (cartridge with rumble)', 'spec', 1.0);

-- gba.header.game_code.region
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('gba.header.game_code.region.j', 'gba.header.game_code.region', '0x4a', 'Japan', 'spec', 1.0),
('gba.header.game_code.region.e', 'gba.header.game_code.region', '0x45', 'USA/English', 'spec', 1.0),
('gba.header.game_code.region.p', 'gba.header.game_code.region', '0x50', 'Europe/Elsewhere', 'spec', 1.0),
('gba.header.game_code.region.d', 'gba.header.game_code.region', '0x44', 'German', 'spec', 1.0),
('gba.header.game_code.region.f', 'gba.header.game_code.region', '0x46', 'French', 'spec', 1.0),
('gba.header.game_code.region.i', 'gba.header.game_code.region', '0x49', 'Italian', 'spec', 1.0),
('gba.header.game_code.region.s', 'gba.header.game_code.region', '0x53', 'Spanish', 'spec', 1.0);

-- gba.header.maker_code
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('gba.header.maker_code.nintendo', 'gba.header.maker_code', '0x3031', 'Nintendo', 'spec', 1.0),
('gba.header.maker_code.capcom', 'gba.header.maker_code', '0x3038', 'Capcom', 'observed', 0.95),
('gba.header.maker_code.ea', 'gba.header.maker_code', '0x3133', 'Electronic Arts', 'observed', 0.95),
('gba.header.maker_code.hudson', 'gba.header.maker_code', '0x3138', 'Hudson Soft', 'observed', 0.9),
('gba.header.maker_code.kemco', 'gba.header.maker_code', '0x3238', 'Kemco', 'observed', 0.9),
('gba.header.maker_code.bandai', 'gba.header.maker_code', '0x3332', 'Bandai', 'observed', 0.95),
('gba.header.maker_code.konami', 'gba.header.maker_code', '0x3334', 'Konami', 'observed', 0.95),
('gba.header.maker_code.ubisoft', 'gba.header.maker_code', '0x3431', 'Ubisoft', 'observed', 0.9),
('gba.header.maker_code.irem', 'gba.header.maker_code', '0x3439', 'Irem', 'observed', 0.85),
('gba.header.maker_code.absolute', 'gba.header.maker_code', '0x3530', 'Absolute Entertainment', 'observed', 0.85),
('gba.header.maker_code.activision', 'gba.header.maker_code', '0x3532', 'Activision', 'observed', 0.95),
('gba.header.maker_code.titus', 'gba.header.maker_code', '0x3630', 'Titus', 'observed', 0.85),
('gba.header.maker_code.lucasarts', 'gba.header.maker_code', '0x3634', 'LucasArts', 'observed', 0.9),
('gba.header.maker_code.infogrames', 'gba.header.maker_code', '0x3730', 'Infogrames', 'observed', 0.9);

-- gba.header.fixed_value
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('gba.header.fixed_value.0x96', 'gba.header.fixed_value', '0x96', 'Must be 0x96', 'spec', 1.0);

-- gba.header.main_unit_code
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('gba.header.main_unit_code.0x00', 'gba.header.main_unit_code', '0x00', '00h for current GBA models', 'spec', 1.0);

-- gba.header.device_type
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('gba.header.device_type.normal', 'gba.header.device_type', '0x00', 'Normal device type (usual default)', 'spec', 1.0);

-- gba.header.reserved_1
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('gba.header.reserved_1.zero_filled', 'gba.header.reserved_1', '0x00000000000000', 'Should be zero-filled', 'spec', 1.0);

-- gba.header.software_version
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('gba.header.software_version.zero', 'gba.header.software_version', '0x00', 'Usually zero (software version)', 'spec', 1.0);

-- gba.header.reserved_2
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('gba.header.reserved_2.zero_filled', 'gba.header.reserved_2', '0x0000', 'Should be zero-filled', 'spec', 1.0);

-- gba.header.multiboot.boot_mode
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('gba.header.multiboot.boot_mode.init_zero', 'gba.header.multiboot.boot_mode', '0x00', 'Init as 00h - BIOS overwrites this value', 'spec', 1.0),
('gba.header.multiboot.boot_mode.joybus', 'gba.header.multiboot.boot_mode', '0x01', '01h: Joybus mode', 'spec', 1.0),
('gba.header.multiboot.boot_mode.normal', 'gba.header.multiboot.boot_mode', '0x02', '02h: Normal mode', 'spec', 1.0),
('gba.header.multiboot.boot_mode.multiplay', 'gba.header.multiboot.boot_mode', '0x03', '03h: Multiplay mode', 'spec', 1.0);

-- gba.header.multiboot.slave_id_number
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('gba.header.multiboot.slave_id_number.init_zero', 'gba.header.multiboot.slave_id_number', '0x00', 'Init as 00h - BIOS overwrites this value', 'spec', 1.0),
('gba.header.multiboot.slave_id_number.slave_1', 'gba.header.multiboot.slave_id_number', '0x01', '01h: Slave #1', 'spec', 1.0),
('gba.header.multiboot.slave_id_number.slave_2', 'gba.header.multiboot.slave_id_number', '0x02', '02h: Slave #2', 'spec', 1.0),
('gba.header.multiboot.slave_id_number.slave_3', 'gba.header.multiboot.slave_id_number', '0x03', '03h: Slave #3', 'spec', 1.0);

-- gba.header.multiboot.not_used
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('gba.header.multiboot.not_used.zero_filled', 'gba.header.multiboot.not_used', '0x0000000000000000000000000000000000000000000000000000', 'Should be zero-filled', 'spec', 1.0);

-- ============================================================
-- INSERT SNES DEFAULT VALUES MAPPED
-- ============================================================

-- snes.header.lorom.map_mode and hirom variants
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('snes.lorom.map_mode.slow_lorom', 'snes.lorom.map_mode', '0x20', 'Slow LoROM', 'spec', 1.0),
('snes.lorom.map_mode.fast_lorom', 'snes.lorom.map_mode', '0x30', 'Fast LoROM', 'spec', 1.0),
('snes.lorom.map_mode.slow_hirom', 'snes.lorom.map_mode', '0x21', 'Slow HiROM', 'spec', 1.0),
('snes.lorom.map_mode.fast_hirom', 'snes.lorom.map_mode', '0x31', 'Fast HiROM', 'spec', 1.0),
('snes.lorom.map_mode.exhirom', 'snes.lorom.map_mode', '0x25', 'ExHiROM (observed)', 'observed', 0.9);

-- snes.lorom.rom_type
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('snes.lorom.rom_type.rom_only', 'snes.lorom.rom_type', '0x00', 'ROM only', 'spec', 1.0),
('snes.lorom.rom_type.rom_ram', 'snes.lorom.rom_type', '0x01', 'ROM + RAM', 'spec', 1.0),
('snes.lorom.rom_type.rom_ram_battery', 'snes.lorom.rom_type', '0x02', 'ROM + RAM + Battery', 'spec', 1.0),
('snes.lorom.rom_type.superfx', 'snes.lorom.rom_type', '0x03', 'SuperFX', 'observed', 0.95),
('snes.lorom.rom_type.sa1', 'snes.lorom.rom_type', '0x05', 'SA-1', 'observed', 0.95),
('snes.lorom.rom_type.sdd1', 'snes.lorom.rom_type', '0x0a', 'S-DD1', 'observed', 0.9);

-- snes.lorom.country
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('snes.lorom.country.japan', 'snes.lorom.country', '0x00', 'Japan', 'spec', 1.0),
('snes.lorom.country.usa', 'snes.lorom.country', '0x01', 'USA', 'spec', 1.0),
('snes.lorom.country.europe', 'snes.lorom.country', '0x02', 'Europe', 'spec', 1.0);

-- snes.lorom.version
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('snes.lorom.version.initial', 'snes.lorom.version', '0x00', 'Initial version', 'spec', 1.0);

-- ============================================================
-- INSERT SEGA GENESIS DEFAULT VALUES MAPPED
-- ============================================================

-- sg.header.console_name
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('sg.header.console_name.megadrive', 'sg.header.console_name', 'Mega Drive', 'Mega Drive console', 'observed', 0.95),
('sg.header.console_name.genesis', 'sg.header.console_name', 'Genesis', 'Genesis console', 'observed', 0.95);

-- sg.header.rom_start
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('sg.header.rom_start.base', 'sg.header.rom_start', '0x00000000', 'ROM base', 'observed', 0.9);

-- sg.header.region_code
INSERT INTO default_values_mapped (id, region_id, raw_value, meaning, origin, confidence) VALUES
('sg.header.region_code.japan', 'sg.header.region_code', '0x4a', 'Japan', 'observed', 0.9),
('sg.header.region_code.usa', 'sg.header.region_code', '0x55', 'USA', 'observed', 0.9),
('sg.header.region_code.europe', 'sg.header.region_code', '0x45', 'Europe', 'observed', 0.9),
('sg.header.region_code.multi', 'sg.header.region_code', '0x4a5545', 'Multi-region', 'observed', 0.95);

-- ============================================================
-- END OF POPULATION SCRIPT
-- ============================================================

COMMIT;

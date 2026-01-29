-- SQL Schema generated from transrom_legacy_full_export_validated.json
-- Created: 2026-01-28

-- ============================================================
-- TABLES CREATION
-- ============================================================

CREATE TABLE IF NOT EXISTS families (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    extensions VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hardware (
    id VARCHAR(255) PRIMARY KEY,
    family_id VARCHAR(255) NOT NULL,
    cpu_id VARCHAR(255),
    cpu_name VARCHAR(255),
    cpu_bitness INT,
    cpu_byte_order VARCHAR(50),
    supports_thumb BOOLEAN,
    supports_modes VARCHAR(255),
    pointer_common_widths VARCHAR(255),
    pointer_relative_supported BOOLEAN,
    pointer_banked BOOLEAN,
    memory_address_spaces TEXT,
    memory_mirrored BOOLEAN,
    memory_banked BOOLEAN,
    banking_supported BOOLEAN,
    banking_types VARCHAR(255),
    banking_bank_size VARCHAR(255),
    compression_supported BOOLEAN,
    compression_types TEXT,
    compression_hardware_assisted BOOLEAN,
    notes TEXT,
    confidence DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (family_id) REFERENCES families(id)
);

CREATE TABLE IF NOT EXISTS cartridge_hardware (
    id VARCHAR(255) PRIMARY KEY,
    family_id VARCHAR(255) NOT NULL,
    extra_cpu BOOLEAN,
    coprocessors TEXT,
    rtc BOOLEAN,
    sensors TEXT,
    rumble BOOLEAN,
    notes TEXT,
    confidence DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (family_id) REFERENCES families(id)
);

CREATE TABLE IF NOT EXISTS layouts (
    id VARCHAR(255) PRIMARY KEY,
    family_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    address_space VARCHAR(255),
    origin VARCHAR(100),
    confidence DECIMAL(3,2),
    canonical_offset VARCHAR(50),
    tags VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (family_id) REFERENCES families(id)
);

CREATE TABLE IF NOT EXISTS regions (
    id VARCHAR(255) PRIMARY KEY,
    layout_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    address_space VARCHAR(255),
    kind VARCHAR(100),
    origin VARCHAR(100),
    confidence DECIMAL(3,2),
    offset VARCHAR(50),
    size INT,
    required BOOLEAN,
    tags VARCHAR(255),
    encoding VARCHAR(255),
    byte_order VARCHAR(50),
    bank VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (layout_id) REFERENCES layouts(id)
);

CREATE TABLE IF NOT EXISTS default_values_mapped (
    id VARCHAR(255) PRIMARY KEY,
    region_id VARCHAR(255) NOT NULL,
    raw_value VARCHAR(255),
    meaning TEXT,
    origin VARCHAR(100),
    confidence DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (region_id) REFERENCES regions(id)
);

-- ============================================================
-- DATA INSERTION
-- ============================================================

-- Game Boy Advance
INSERT INTO families (id, name, extensions, notes) VALUES
('gba', 'Game Boy Advance', '.gba', NULL),
('snes', 'Super Nintendo Entertainment System', '.snes,.smc', NULL),
('sg', 'Sega Genesis / Mega Drive', '.bin,.md,.rom', NULL);

-- GBA Hardware
INSERT INTO hardware (id, family_id, cpu_id, cpu_name, cpu_bitness, cpu_byte_order, supports_thumb, supports_modes, pointer_common_widths, pointer_relative_supported, pointer_banked, memory_address_spaces, memory_mirrored, memory_banked, banking_supported, banking_types, compression_supported, compression_types, compression_hardware_assisted, notes, confidence)
VALUES
('gba.hw.default', 'gba', 'arm7tdmi', 'ARM7TDMI', 32, 'little', true, 'arm,thumb', '32', false, false, 'gba.rom,gba.wram,gba.iram,gba.vram,gba.sram', false, false, false, 'none', true, 'lz77,huffman,rle', true, 'ARM7TDMI CPU used in GBA, supports ARM and Thumb states. BIOS provides decompression routines', NULL);

-- GBA Cartridge Hardware
INSERT INTO cartridge_hardware (id, family_id, extra_cpu, coprocessors, rtc, sensors, rumble, notes, confidence)
VALUES
('gba.cartridge.default', 'gba', false, '', false, '', false, NULL, NULL);

-- GBA Layouts
INSERT INTO layouts (id, family_id, name, address_space, origin, confidence, canonical_offset, tags, notes)
VALUES
('gba.header.standard', 'gba', 'GBA Cartridge Header', 'gba.rom', 'spec', 1.0, '0x0', 'structural', 'Standard fixed GBA cartridge header.');

-- SNES (Generic entries - structure example)
INSERT INTO families (id, name, extensions, notes) VALUES
('snes', 'Super Nintendo Entertainment System', '.snes,.smc', NULL)
ON CONFLICT(id) DO NOTHING;

-- Sega Genesis / Mega Drive (Generic entries - structure example)
INSERT INTO families (id, name, extensions, notes) VALUES
('sg', 'Sega Genesis / Mega Drive', '.bin,.md,.rom', NULL)
ON CONFLICT(id) DO NOTHING;

-- ============================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_hardware_family ON hardware(family_id);
CREATE INDEX IF NOT EXISTS idx_cartridge_hardware_family ON cartridge_hardware(family_id);
CREATE INDEX IF NOT EXISTS idx_layouts_family ON layouts(family_id);
CREATE INDEX IF NOT EXISTS idx_regions_layout ON regions(layout_id);
CREATE INDEX IF NOT EXISTS idx_layouts_address_space ON layouts(address_space);
CREATE INDEX IF NOT EXISTS idx_regions_address_space ON regions(address_space);
CREATE INDEX IF NOT EXISTS idx_default_values_region ON default_values_mapped(region_id);

-- ============================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================

CREATE VIEW IF NOT EXISTS v_family_hardware_summary AS
SELECT 
    f.id as family_id,
    f.name as family_name,
    h.cpu_name,
    h.cpu_bitness,
    h.compression_supported,
    h.compression_types
FROM families f
LEFT JOIN hardware h ON f.id = h.family_id;

CREATE VIEW IF NOT EXISTS v_family_layouts_regions AS
SELECT 
    f.id as family_id,
    f.name as family_name,
    l.id as layout_id,
    l.name as layout_name,
    r.id as region_id,
    r.name as region_name,
    r.offset,
    r.size
FROM families f
LEFT JOIN layouts l ON f.id = l.family_id
LEFT JOIN regions r ON l.id = r.layout_id;

CREATE VIEW IF NOT EXISTS v_regions_with_default_values AS
SELECT 
    r.id as region_id,
    r.name as region_name,
    r.layout_id,
    dv.id as default_value_id,
    dv.raw_value,
    dv.meaning,
    dv.origin,
    dv.confidence
FROM regions r
LEFT JOIN default_values_mapped dv ON r.id = dv.region_id
ORDER BY r.id, dv.id;

-- ============================================================
-- END OF SCRIPT
-- ============================================================

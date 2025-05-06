# 📚 Game Boy Advance (GBA) - Technical Reference Guide

> **This document compiles essential information about the Game Boy Advance (GBA) hardware, memory, ROM structure, pointers, character tables, compression, and more, with a focus on ROM hacking, translation, and tool development.**

---

## Table of Contents

1. [Overview](#overview)
2. [Hardware](#hardware)
   - [CPU](#cpu)
   - [Memory](#memory)
   - [Memory Map](#memory-map)
   - [Graphics & Video](#graphics--video)
   - [Audio](#audio)
   - [Inputs & Peripherals](#inputs--peripherals)
3. [ROMs & Memory Space](#roms--memory-space)
   - [Maximum ROM Size](#maximum-rom-size)
   - [ROM Structure](#rom-structure)
4. [Pointers & Addressing](#pointers--addressing)
5. [Character Tables](#character-tables)
   - [ASCII, Shift-JIS, and Custom Tables](#ascii-shift-jis-and-custom-tables)
   - [How to Find and Build Tables](#how-to-find-and-build-tables)
6. [Compression & Decompression](#compression--decompression)
   - [Common Formats (LZ77, Huffman, etc.)](#common-formats-lz77-huffman-etc)
   - [Tools & Tips](#tools--tips)
7. [Technologies & Development Tools](#technologies--development-tools)
8. [Links & References](#links--references)

---

## Overview

The Game Boy Advance (GBA) is a handheld console released by Nintendo in 2001, featuring a 32-bit ARM7TDMI CPU. It is known for its flexible graphics, stereo sound, and large game library. The GBA is popular in the ROM hacking and homebrew communities due to its accessible architecture and extensive documentation.

---

## Hardware

### CPU
- **Processor:** ARM7TDMI (32-bit RISC)
- **Clock Speed:** 16.78 MHz
- **Instruction Sets:** ARM (32-bit), Thumb (16-bit)
- [ARM7TDMI Technical Reference](https://developer.arm.com/documentation/ddi0210/c/)

### Memory
- **WRAM (Work RAM):** 256 KB (external) + 32 KB (internal)
- **VRAM (Video RAM):** 96 KB
- **OAM (Object Attribute Memory):** 1 KB (for sprites)
- **Palette RAM:** 1 KB (512 bytes BG + 512 bytes OBJ)
- **ROM:** Up to 32 MB (256 Mbit)
- **SRAM/Flash/EEPROM:** Up to 64 KB (for save data, varies by cartridge)

### Memory Map

| Start Address | Size      | Description             |
|--------------|-----------|-------------------------|
| 0x00000000   | 32 KB     | BIOS                    |
| 0x02000000   | 256 KB    | External WRAM           |
| 0x03000000   | 32 KB     | Internal WRAM           |
| 0x04000000   | 1 KB      | I/O Registers           |
| 0x05000000   | 1 KB      | Palette RAM             |
| 0x06000000   | 96 KB     | VRAM                    |
| 0x07000000   | 1 KB      | OAM                     |
| 0x08000000   | up to 32 MB | Game Pak ROM/FlashROM |
| 0x0E000000   | 64 KB     | Game Pak SRAM           |

- [GBATEK - Memory Map](https://problemkaputt.de/gbatek.htm#gbamemorymap)

### Graphics & Video
- **Resolution:** 240x160 pixels
- **Color Depth:** 15-bit (BGR555), 32,768 possible colors, 512 on-screen
- **Graphics Modes:** 6 modes (0-5), combining tiled backgrounds and bitmaps
- **Sprites:** Up to 128, various sizes
- [Tonc - GBA Graphics Hardware](https://www.coranac.com/tonc/text/hardware.htm)

### Audio
- **Channels:** 6 (2 PSG, 2 Direct Sound, 2 Wave)
- **Stereo sound**
- **Hardware mixing**

### Inputs & Peripherals
- **Buttons:** A, B, L, R, Start, Select, D-Pad
- **Link Cable:** Serial communication between GBAs
- **Special Cartridges:** RTC, sensors, rumble, etc.

---

## ROMs & Memory Space

### Maximum ROM Size
- **Theoretical limit:** 32 MB (256 Mbit)
- **Common sizes:** 4 MB, 8 MB, 16 MB

### ROM Structure
- **Header:** Game info, Nintendo logo, checksum, etc.
- **Game Data:** Code, graphics, text, tables, scripts, etc.
- [GBATEK - Game Pak ROM](https://problemkaputt.de/gbatek.htm#gbacartridges)

---

## Pointers & Addressing
- **Pointers** are values (usually 3 or 4 bytes) that indicate addresses in ROM or RAM.
- **Absolute addressing:** Pointers that point to fixed addresses (e.g., 0x08000000 + offset)
- **Relative addressing:** Pointers that use an offset from a known base.
- **Endianness:** GBA uses little-endian (e.g., pointer 0x12 0x34 0x56 0x08 → address 0x08563412)

---

## Character Tables

### ASCII, Shift-JIS, and Custom Tables
- **ASCII:** Used in Western games, 1 byte per character.
- **Shift-JIS:** Used in Japanese games, 1-2 bytes per character.
- **Custom tables:** Games may use their own mappings (e.g., 0x80 = 'A', 0x81 = 'B', etc.)

### How to Find and Build Tables
- **Tools:** WindHex, MadEdit, Cartographer, Atlas, Hex Workshop
- **Process:** Locate text in the ROM, identify patterns, create a .tbl file mapping bytes to characters.
- [Table Tutorial](http://www.loirak.com/gameboy/gbatutor.php)

---

## Compression & Decompression

### Common Formats (LZ77, Huffman, etc.)
- **LZ77:** Widely used in GBA (e.g., graphics, compressed text)
- **Huffman:** Used in some games for text
- **RLE, LZSS, LZ78:** Other possible formats

### Tools & Tips
- **Tools:** GBA Graphics Editor, Nintenlord's NLZ-GBA Advance, GBA Tool Advance, unLZ-GBA
- **Tip:** LZ77 blocks often start with 0x10

---

## Technologies & Development Tools
- **Compilers:** [devkitARM](https://devkitpro.org/), [gba-toolchain](https://github.com/devkitPro/gba-toolchain)
- **Emulators:** [mGBA](https://mgba.io/), [No$GBA](https://problemkaputt.de/gba.htm), [NanoBoyAdvance](https://github.com/nba-emu/NanoBoyAdvance)
- **Toolkits:** [Butano](https://github.com/GValiente/Butano), [libtonc](https://www.coranac.com/tonc/)
- **Documentation:** [GBATEK](https://problemkaputt.de/gbatek.htm), [Tonc](https://www.coranac.com/tonc/)
- **Community:** [GBAdev Discord](https://discord.gg/gbadev), [GBAdev Forum](https://forum.gbadev.net/)
- **Resource lists:** [awesome-gbadev](https://github.com/gbadev-org/awesome-gbadev)

---

## Links & References
- [awesome-gbadev (curated resources)](https://github.com/gbadev-org/awesome-gbadev)
- [Blog do Chrono - GBA Programming Intro (PT-BR)](https://blogdochrono.blogspot.com/2017/11/introducao-programacao-de-game-boy.html)
- [Loirak - GBA ROM Hacking Tutorials (PT-BR)](http://www.loirak.com/gameboy/gbatutor.php)
- [Tonc - GBA Tutorials & Docs](https://www.coranac.com/tonc/text/asm.htm)
- [GBATEK - Complete Technical Reference](https://problemkaputt.de/gbatek.htm)
- [ARM7TDMI Technical Reference](https://developer.arm.com/documentation/ddi0210/c/)
- [Tonc - GBA Hardware](https://www.coranac.com/tonc/text/hardware.htm)
- [GBAdev.net](https://www.gbadev.net/)

---

## 🛠️ Reverse Engineering Workflow Overview

1. **ROM Acquisition:** Obtain a clean GBA ROM dump.
2. **Header Parsing:** Read and interpret the ROM header to get metadata and entry points.
3. **Pointer Table Detection:** Scan for pointer tables (usually 32-bit little-endian values in the 0x08xxxxxx range).
4. **Text Block Identification:** Locate text blocks (plain, encoded, or compressed).
5. **Compression Detection:** Identify and decompress data blocks (e.g., LZ77, Huffman).
6. **Asset Extraction:** Extract graphics, palettes, and other assets.
7. **Editing & Repacking:** Modify extracted data and repack into the ROM.
8. **Testing:** Run the modified ROM in an emulator or on real hardware.

---

## 🧩 ROM Header Deep Dive

- **Header Offset:** 0x00000000 - 0x000000BC
- **Fields:**
  - Entry Point (0x00-0x03)
  - Nintendo Logo (0x04-0x9F)
  - Game Title (0xA0-0xAB)
  - Game Code (0xAC-0xAF)
  - Maker Code (0xB0-0xB1)
  - Fixed Value (0xB2)
  - Main Unit Code (0xB3)
  - Device Type (0xB4)
  - Reserved (0xB5-0xB9)
  - Software Version (0xBC)
  - Complement Check (0xBD)

**Python Example:**
```python
with open('game.gba', 'rb') as f:
    header = f.read(0xC0)
    game_title = header[0xA0:0xAC].decode('ascii')
    game_code = header[0xAC:0xB0].decode('ascii')
    print(f"Title: {game_title}, Code: {game_code}")
```
- [GBATEK - ROM Header](https://problemkaputt.de/gbatek.htm#gbacartridgeheader)

---

## 🧩 Pointer Table Detection and Extraction

**Summary:**
GBA games use little-endian 32-bit pointers, usually pointing to addresses in the 0x08xxxxxx range (ROM). Pointer tables are often contiguous blocks of such values.

**Algorithm (Python):**
```python
import struct

def find_pointers(rom_bytes, base=0x08000000):
    pointers = []
    for i in range(0, len(rom_bytes) - 4, 4):
        val = struct.unpack('<I', rom_bytes[i:i+4])[0]
        if base <= val < base + len(rom_bytes):
            pointers.append((i, val))
    return pointers
```
- **Heuristic:** Look for sequences of 4-byte values where most point to valid ROM addresses.

---

## 📝 Text Extraction and Encoding

- **Text Storage:**
  - Plain ASCII/Shift-JIS
  - Custom encoding (table-based)
  - Compressed (often LZ77)
- **Detection:**
  - Look for readable ASCII/Shift-JIS blocks
  - Use table files for custom encodings

**Example: Extracting ASCII text**
```python
import re
with open('game.gba', 'rb') as f:
    data = f.read()
    for match in re.finditer(rb'[\x20-\x7E]{4,}', data):
        print(f"Offset {match.start():08X}: {match.group().decode('ascii')}")
```

**Table-based Decoding:**
- Build a `.tbl` file mapping bytes to characters
- Use it to decode text blocks

---

## 🗂️ Character Table (TBL) Handling

- **Format Example:**
  - `80=A`
  - `81=B`
  - `82=C`
- **Python Example:**
```python
def load_tbl(path):
    tbl = {}
    with open(path) as f:
        for line in f:
            if '=' in line:
                k, v = line.strip().split('=')
                tbl[int(k, 16)] = v
    return tbl
```

---

## 🗜️ Compression & Decompression

### LZ77 (GBA)
- **Header:** 0x10 (1 byte), followed by 3 bytes for decompressed size
- **Block:** [0x10][size][compressed data]
- **Detection:** Look for 0x10 at the start of a block

**Python Example (LZ77 decompression):**
- See [GBATEK LZ77](https://problemkaputt.de/gbatek.htm#biosdecompressionfunctions)
- [Python LZ77 Example (external)](https://github.com/pleonex/tinke/blob/master/tinke/formats/lz77.py)

**C Example:**
- [Tonc LZ77 C Implementation](https://www.coranac.com/tonc/text/asm.htm#sec-lz77)

---

## 🎨 Graphics and Asset Extraction

- **Tiles:** 8x8 pixels, 4bpp or 8bpp
- **Palettes:** 15-bit BGR555
- **Maps:** Tilemaps for backgrounds
- **Extraction:**
  - Read VRAM-like structures from ROM
  - Convert to PNG using Python (e.g., Pillow) or C/C++ for speed

---

## 💾 Save Data (SRAM/EEPROM/Flash)
- **SRAM:** 0x0E000000, up to 64 KB
- **EEPROM/Flash:** Special handling, see [GBATEK Save Types](https://problemkaputt.de/gbatek.htm#gbacartbackupflashsramandeeprom)
- **Reading/Writing:**
  - For patching, locate and modify save blocks

---

## 🚀 Action Plan for Custom Tool Development

1. **Core in Python:**
   - ROM parsing, pointer scanning, text extraction, patching
2. **Performance Modules in C/C++/C#:**
   - Compression/decompression, graphics conversion
3. **Modular Design:**
   - Separate modules for each console/format
   - Easy to add new extractors/patchers
4. **Example Project Structure:**
   - `/core` (Python): parsing, extraction, patching
   - `/native` (C/C++/C#): performance-critical code
   - `/tables`: character tables
   - `/docs`: technical documentation

---

## 📑 Appendix: Patterns, Magic Numbers, and Gotchas

- **LZ77 block:** Starts with 0x10
- **Pointer base:** 0x08000000
- **ASCII text:** 0x20-0x7E
- **Shift-JIS:** 0x81-0x9F, 0xE0-0xFC (lead bytes)
- **Header magic:** Nintendo logo at 0x04
- **Pitfalls:**
  - Overlapping/compressed pointer tables
  - Mixed encodings
  - Bank switching in some games

---

## 🔗 References (see main list above)
- [GBATEK](https://problemkaputt.de/gbatek.htm)
- [Tonc](https://www.coranac.com/tonc/)
- [awesome-gbadev](https://github.com/gbadev-org/awesome-gbadev)
